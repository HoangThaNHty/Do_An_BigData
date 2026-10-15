"""Audit Git candidates without printing credentials or raw listing contents."""
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FORBIDDEN={'.venv','.runtime','.cache','node_modules','.next','__pycache__'}
PATTERNS=[re.compile(rb'(?:sk-(?:proj-)?[A-Za-z0-9_-]{24,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})'),
          re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')]

def main():
    result=subprocess.run(['git','ls-files','-z','--cached','--others','--exclude-standard'],cwd=ROOT,capture_output=True,check=True)
    names=sorted(set(x.decode('utf-8') for x in result.stdout.split(b'\0') if x))
    problems=[];total=0;largest=[]
    for name in names:
        path=ROOT/name
        if not path.is_file():problems.append('Missing Git file: '+name);continue
        size=path.stat().st_size;total+=size;largest.append((size,name))
        if set(Path(name).parts)&FORBIDDEN:problems.append('Local environment/build included: '+name)
        if size>45*1024*1024:problems.append('File exceeds project 45 MiB policy: '+name)
        if name.startswith(('artifacts/review/','artifacts/profile/','data/processed/etl_')) or (name.startswith('data/raw/oceanng/') and name.endswith('.parquet')):problems.append('Research raw/review included: '+name)
        if path.name.startswith('.env') and path.name!='.env.example':problems.append('Private environment file included: '+name)
        if path.suffix.lower() in {'.py','.ps1','.cjs','.ts','.tsx','.md','.json','.txt','.toml','.yaml','.yml',''} and size<8*1024*1024:
            payload=path.read_bytes()
            if any(p.search(payload) for p in PATTERNS):problems.append('Possible credential/private key in: '+name)
    report={'passed':not problems,'files':len(names),'bytes':total,'largest_files':[{'path':n,'bytes':s} for s,n in sorted(largest,reverse=True)[:5]],'problems':problems,
            'scope':'High-signal token/private-key scan and repo inclusion checks; not an exhaustive security audit.'}
    out=ROOT/'.runtime/github_audit.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if problems:raise SystemExit(1)

if __name__=='__main__':main()
