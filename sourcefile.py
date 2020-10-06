import os
import shlex

from enum import Enum
from pathlib import Path
from pbuildcommands import PBuildCommands

__filetypes = None

def _filetypes():
    global __filetypes
    if not __filetypes:
        __filetypes = {
            '.cpp': __import__('cppsource').CppSource,
            '.c': __import__('csource').CSource,
            '.h': __import__('hsource').HSource,
        }
    return __filetypes

class BuildMode(Enum):
    release = 0
    debug = 1

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(cls, s):
        try:
            return cls[s]
        except KeyError:
            raise ValueError()

class SourceFile:
    def __init__(self, filename):
        self.sources = None
        self.filename = Path(filename)
        self.path = filename
        if not self.path.is_file():
            path = SourceFile.find_source(self.path)
            if not path:
                raise FileNotFoundError(self.path)
            self.path = path
        for token in self.build_tokens():
            cmd = shlex.split(token)
            if cmd[0].startswith('pbuild') and len(cmd) > 1:
                if cmd[1] in PBuildCommands:
                    PBuildCommands[cmd[1]](cmd)
        self.deps = set(self.dependencies())

    def _dependencies(self):
        raise NotImplementedError()

    def dependencies(self):
        for d in self._dependencies():
            try:
                r = d.relative_to(os.getcwd())
                if not r.is_absolute() and not '..' in r:
                    yield d
            except ValueError:
                pass

    def comments(self):
        raise NotImplementedError()

    def build_tokens(self):
        token = ''
        for t in self.comments():
            if t.endswith('\\'):
                token += t[:-1]
            else:
                yield token + t
                token = ''
        if len(token) > 0:
            yield token

    def out_of_date(self):
        return True

    def build(self, mode=BuildMode.release):
        for prjsrc in self.sources:
            if self.sources[prjsrc].out_of_date():
                self.sources[prjsrc].build_inner(mode=mode)

    def build_inner(self, mode):
        return '.obj' / self.path.relative_to(os.getcwd())

    def inner(self):
        return None

    @classmethod
    def as_project(cls, filename):
        filename = Path(filename)
        inst = _filetypes()[filename.suffix](filename)
        inst.deps.add(filename)
        inst.sources = {str(filename): inst}
        for p in inst.deps:
            if str(p) in inst.sources:
                inst.sources[str(p)] = _filetypes()[p.suffix](filename)
        return inst

    @classmethod
    def find_source(cls, filepath):
        dirs = (d for d in Path('./').iterdir() if d.is_dir())
        for d in dirs:
            (d / filepath).is_file()
            return d / filepath
        return None
