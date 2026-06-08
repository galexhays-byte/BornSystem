import py_compile
from pathlib import Path

base = Path('backend/src')
files = list(base.rglob('*.py'))
for path in files:
    py_compile.compile(str(path), doraise=True)
print('compiled', len(files), 'files')
