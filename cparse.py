import re
import sourcefile

from pathlib import Path
from sourcefile import SourceFile

_open = re.compile('\\/\\*|\\/\\/|\'|"')
_new_line = re.compile('\n')
_block_close = re.compile('\\*\\/')
_single_close = re.compile("'|\\.")
_double_close = re.compile('"|\\.')

def CCmntParse(filepath):
    with filepath.open() as f:
        i = 0
        filecontents = f.read()
        while i < len(filecontents):
            m = _open.search(filecontents, i)
            if m is None:
                return
            i = m.end()
            if m.group() == '"':
                m = _single_close.search(filecontents, i)
                while i < len(filecontents) and m and m.group() != "'":
                    i = m.end()
            elif m.group() == "'":
                m = _double_close.search(filecontents, i)
                while i < len(filecontents) and m and m.group() != '"':
                    i = m.end()
            elif m.group() == '//':
                m = _new_line.search(filecontents, i)
                if m is None:
                    yield filecontents[i:]
                else:
                    yield filecontents[i:m.end()]
            else:
                assert m.group() == '/*'
                m = _block_close.search(filecontents, i)
                if m is None:
                    yield filecontents[i:]
                else:
                    yield filecontents[i:m.start()]
            i = m.end() if m else len(filecontents)

_include_open = re.compile('#\\s*include\\s*"')

def _CIncludeParce(filepath):
    with filepath.open() as f:
        for l in f:
            m = _include_open.search(l)
            if m:
                m2 = re.search('"', l, m.end())
                if m2:
                    yield l[m.end():m2.start()]

def CIncludeParce(filepath):
    for t in _CIncludeParce(filepath):
        path = SourceFile.find_source(Path(t))
        if path:
            yield t

