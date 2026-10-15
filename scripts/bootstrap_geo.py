"""Download pinned administrative reference and historical map geometry."""
import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/raw/geography"
ADMIN_REV = "fc33b7411ec4e3697817fab8118718a8d39ef090"
BOUNDARY_REV = "9469f09"
SOURCES = {
    "admin_2025_03.json": f"https://raw.githubusercontent.com/ThangLeQuoc/vietnamese-provinces-database/{ADMIN_REV}/json/vn_only_simplified_json_generated_data_vn_units.json",
    "admin_LICENSE.txt": f"https://raw.githubusercontent.com/ThangLeQuoc/vietnamese-provinces-database/{ADMIN_REV}/LICENSE",
    "districts_2020_simplified.geojson": f"https://raw.githubusercontent.com/wmgeolab/geoBoundaries/{BOUNDARY_REV}/releaseData/gbOpen/VNM/ADM2/geoBoundaries-VNM-ADM2_simplified.geojson",
    "districts_2020_metadata.json": f"https://raw.githubusercontent.com/wmgeolab/geoBoundaries/{BOUNDARY_REV}/releaseData/gbOpen/VNM/ADM2/geoBoundaries-VNM-ADM2-metaData.json",
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    old = json.loads((OUT / "manifest.json").read_text()) if (OUT / "manifest.json").exists() else None
    files = []
    for name, url in SOURCES.items():
        target = OUT / name
        if not target.exists():
            request = urllib.request.Request(url, headers={"User-Agent": "HUIT-BigData-course-project"})
            payload = urllib.request.urlopen(request, timeout=90).read()
            if payload.startswith(b"version https://git-lfs.github.com/spec/v1"):
                expected_lfs = payload.decode().split("oid sha256:")[1].splitlines()[0]
                media_url = url.replace("https://raw.githubusercontent.com/", "https://media.githubusercontent.com/media/")
                payload = urllib.request.urlopen(urllib.request.Request(media_url, headers={"User-Agent":"HUIT-BigData-course-project"}), timeout=90).read()
                if hashlib.sha256(payload).hexdigest() != expected_lfs:
                    raise ValueError("Git LFS object fingerprint mismatch")
            if name.endswith(("json", "geojson")):
                json.loads(payload)
            temporary = target.with_suffix(target.suffix + ".part")
            temporary.write_bytes(payload)
            temporary.replace(target)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if old:
            expected = next(f["sha256"] for f in old["files"] if f["file"] == name)
            if digest != expected:
                raise ValueError(f"Local geographic source checksum mismatch: {name}")
        files.append({"file": name, "url": url, "bytes": target.stat().st_size, "sha256": digest})
        print(f"Verified {name}: {target.stat().st_size} bytes")
    manifest = {"administrative_reference": "v2.4.1, cutoff before July 2025 reform", "admin_revision": ADMIN_REV,
                "map_reference": "geoBoundaries VNM-ADM2-81297802, year represented 2020; simplified geometry",
                "boundary_revision": BOUNDARY_REV, "files": files,
                "attribution": ["Administrative reference: Thang Le Quoc, MIT license (local license retained)",
                                "Boundaries: OCHA ROAP / Government of Viet Nam via geoBoundaries, CC BY 3.0 IGO"],
                "limitations": ["Historical boundaries, not current legal boundaries or property coordinates.",
                                "Dataset names may mix administrative vintages; keep raw fields and report match status."]}
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
