"""Record installed versions for the dependency graph of each runtime manifest."""
from pathlib import Path
from importlib import metadata
from packaging.requirements import Requirement

ROOT=Path(__file__).resolve().parents[1]

def inputs(path):
    for line in path.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line or line.startswith('#'):continue
        if line.startswith('-r '):yield from inputs(path.parent/line[3:].strip())
        else:yield Requirement(line).name

def main():
    for stem in ['requirements-bootstrap','requirements-api']:
        todo=list(inputs(ROOT/(stem+'.txt')));seen=set()
        while todo:
            name=todo.pop().lower().replace('_','-')
            if name in seen:continue
            seen.add(name)
            for text in metadata.requires(name) or []:
                requirement=Requirement(text)
                if requirement.marker is None or requirement.marker.evaluate({'extra':''}):todo.append(requirement.name)
        (ROOT/(stem+'.lock.txt')).write_text(''.join(name+'=='+metadata.version(name)+'\n' for name in sorted(seen)),encoding='utf-8')
        print(stem,len(seen),'runtime packages; QA dependencies excluded')

if __name__=='__main__':main()
