"""Package Git-visible runnable source; environments/raw/review stay local."""
import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--include-office',action='store_true',help='Include existing local Office snapshots; do not regenerate them.')
    parser.add_argument('--mirror',type=Path,help='Optional local destination for ZIP/checksum.')
    args=parser.parse_args()
    files=set()
    def add(p):
        p=p.resolve();p.relative_to(ROOT)
        if p.is_file():files.add(p)
    if (ROOT/'.git').exists():
        listing=subprocess.run(['git','ls-files','-z','--cached','--others','--exclude-standard'],cwd=ROOT,capture_output=True,check=True)
        for name in listing.stdout.split(b'\0'):
            if name:add(ROOT/name.decode('utf-8'))
    else:
        # An extracted package has no Git metadata: reconstruct the same runnable core.
        for folder in ['src','scripts','archive','docs','web','.vscode','artifacts/models/v1','artifacts/market','artifacts/geography','artifacts/etl/etl_v4','artifacts/figures','data/raw/geography']:
            for p in (ROOT/folder).rglob('*'):
                if any(x in ['__pycache__','node_modules','.next'] for x in p.parts):continue
                if p.suffix in ['.pyc','.crc'] or p.name in ['tsconfig.tsbuildinfo','.env.local']:continue
                add(p)
        for name in ['data/demo_manifest.json','data/README.md','data/raw/oceanng/manifest.json','data/raw/oceanng/DATASET_CARD.md','data/processed/core_v1/manifest.json','data/processed/core_v1/excluded_review_ids.json']:add(ROOT/name)
        for pattern in ['*.md','requirements*.txt','.gitignore','.gitattributes']:
            for p in ROOT.glob(pattern):add(p)
    if args.include_office:
        for p in (ROOT/'deliverables').glob('*'):
            if p.suffix in ['.docx','.pptx','.md']:add(p)
    forbidden={'.venv','.runtime','.cache','node_modules','.next','__pycache__','.git'}
    for p in files:
        rel=p.relative_to(ROOT)
        if forbidden.intersection(rel.parts):raise ValueError('Local runtime in package: '+str(rel))
        if p.name.startswith('.env') and p.name!='.env.example':raise ValueError('Private env in package')
    manifest={'version':'handoff-2026-10-14-github-ready','dataset_revision':'6f68fe87be7577afb03e38c535bd882d242ba26d',
              'data':'core_v1','models':'v1','raw_dataset_included':False,'environment_included':False,
              'office_documents':'Existing pre-V4 snapshots included.' if args.include_office else 'Excluded by default; deferred by user.',
              'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]}
    target=ROOT/'deliverables/DO_AN_BIGDATA_NHOM18_BAN_GIAO.zip';target.parent.mkdir(exist_ok=True)
    temporary=target.with_suffix('.zip.part')
    with zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(files):z.write(p,p.relative_to(ROOT).as_posix())
        z.writestr('HANDOFF_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2))
    with zipfile.ZipFile(temporary) as z:
        assert z.testzip() is None
        for entry in manifest['files']:assert hashlib.sha256(z.read(entry['path'])).hexdigest()==entry['sha256']
        assert 'web/package-lock.json' in z.namelist() and 'data/demo_manifest.json' in z.namelist()
    temporary.replace(target)
    fingerprint={'file':target.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size,'files':len(files),'verified':True}
    checksum=target.parent/'GOI_BAN_GIAO_SHA256.json';checksum.write_text(json.dumps(fingerprint,indent=2),encoding='utf-8')
    if args.mirror:
        args.mirror.mkdir(parents=True,exist_ok=True)
        shutil.copy2(target,args.mirror/target.name);shutil.copy2(checksum,args.mirror/checksum.name)
    print(json.dumps(fingerprint,indent=2))

if __name__=='__main__':main()
