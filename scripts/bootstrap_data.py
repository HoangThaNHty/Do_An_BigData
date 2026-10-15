"""Download a pinned dataset and a verified portable JDK without global changes."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPO = "oceanNG/vietnam-real-estates"


def fetch_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "RealEstateBigData/1.0"}), timeout=60) as r:
        return json.load(r)


def download(url, target, size=None):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and (size is None or target.stat().st_size == size):
        return target
    partial = target.with_suffix(target.suffix + ".part")
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "RealEstateBigData/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r, partial.open("wb") as f:
                while chunk := r.read(1024 * 1024):
                    f.write(chunk)
            if size is not None and partial.stat().st_size != size:
                raise ValueError(f"Unexpected size for {target.name}")
            os.replace(partial, target)
            print(f"Downloaded {target.name}: {target.stat().st_size:,} bytes", flush=True)
            return target
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


def install_jdk():
    home_file = ROOT / ".runtime/java_home.txt"
    if home_file.exists() and (Path(home_file.read_text().strip()) / "bin/java.exe").exists():
        return
    release = fetch_json("https://api.github.com/repos/adoptium/temurin17-binaries/releases/latest")
    asset = next(a for a in release["assets"] if "jdk_x64_windows_hotspot" in a["name"] and a["name"].endswith(".zip"))
    checksum_asset = next(a for a in release["assets"] if a["name"] == asset["name"] + ".sha256.txt")
    archive = download(asset["browser_download_url"], ROOT / ".runtime" / asset["name"], asset["size"])
    with urllib.request.urlopen(checksum_asset["browser_download_url"], timeout=60) as r:
        expected = r.read().decode().split()[0]
    with archive.open("rb") as f:
        actual = hashlib.file_digest(f, "sha256").hexdigest()
    if actual != expected:
        raise ValueError("JDK SHA256 mismatch")
    destination = (ROOT / ".runtime/jdk17").resolve()
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for item in z.infolist():
            resolved = (destination / item.filename).resolve()
            if not resolved.is_relative_to(destination):
                raise ValueError("Unsafe zip path")
        z.extractall(destination)
    java = next(destination.glob("*/bin/java.exe"))
    home_file.write_text(str(java.parents[1]), encoding="utf-8")
    (ROOT / ".runtime/jdk_manifest.json").write_text(json.dumps({"release": release["tag_name"], "url": asset["browser_download_url"], "sha256": actual}, indent=2), encoding="utf-8")
    print(f"Java home: {java.parents[1]}", flush=True)


def dataset(limit=None):
    folder = ROOT / "data/raw/oceanng"
    folder.mkdir(parents=True, exist_ok=True)
    manifest_path = folder / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        info = fetch_json(f"https://huggingface.co/api/datasets/{REPO}")
        revision = info["sha"]
        entries = fetch_json(f"https://huggingface.co/api/datasets/{REPO}/tree/{revision}?recursive=true")
        files = [{"path": e["path"], "size": e["size"], "lfs": e.get("lfs")} for e in entries if e["path"].endswith(".parquet")]
        manifest = {"repository": REPO, "revision": revision, "files": files}
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    files = manifest["files"][:limit] if limit else manifest["files"]
    def one(entry):
        path = download(f"https://huggingface.co/datasets/{REPO}/resolve/{manifest['revision']}/{entry['path']}?download=true", folder / entry["path"], entry["size"])
        expected = (entry.get("lfs") or {}).get("oid")
        if expected:
            with path.open("rb") as f:
                actual = hashlib.file_digest(f, "sha256").hexdigest()
            if actual != expected:
                raise ValueError(f"Dataset checksum mismatch: {path.name}")
        return path
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for _ in pool.map(one, files):
            pass
    download(f"https://huggingface.co/datasets/{REPO}/resolve/{manifest['revision']}/README.md", folder / "DATASET_CARD.md")
    print(f"Verified {len(files)} shards at revision {manifest['revision']}", flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--jdk", action="store_true")
    p.add_argument("--dataset", action="store_true")
    p.add_argument("--limit", type=int)
    args = p.parse_args()
    if args.jdk:
        install_jdk()
    if args.dataset:
        dataset(args.limit)
