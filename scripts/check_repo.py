"""Check the small demo bundle using only Python's standard library."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    manifest_path=ROOT/'data/demo_manifest.json'
    if not manifest_path.exists():raise SystemExit('Missing data/demo_manifest.json: clone the complete repository.')
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    problems=[]
    for item in manifest['files']:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT):raise SystemExit('Invalid demo manifest path')
        if not path.is_file():problems.append('Missing: '+item['path']);continue
        if hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:problems.append('Changed: '+item['path'])
    if problems:raise SystemExit('\n'.join(problems)+'\nRestore demo artifacts from Git; do not use GitHub source pages to download individual model files.')
    print(f"PASS: {len(manifest['files'])} demo files verified; no raw download or retraining needed.")

if __name__=='__main__':main()
