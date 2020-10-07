import subprocess as sp

from cparse import CCmntParse, CIncludeParce
from pathlib import Path
from sourcefile import SourceFile, BuildMode

#need to rethink this a bit, classes should be build targets with auto_scan dependancies and new target conversions when at top level
# ...C++ build only needs includes found by this souce... keep it simple

class CppSource(SourceFile):
    def __init__(self, filename):
        super().__init__(filename)

    def attach_project(self, project):
        project.add_target(ObjTarget(self.inner()))

    def comments(self):
        return CCmntParse(self.path)

    def _dependencies(self):
        return CIncludeParce(self.path)

    def inner(self):
        return Path(str(self.path) + ".obj")

    def build_inner(self, mode, incpaths=None):
        innerpath = self.inner()
        for i in range(len(innerpath.parents) - 1):
            if not innerpath.parents[i].is_dir():
                innerpath.parents[i].mkdir()
        if not incpaths:
            incpaths = []
        opts = ['-std=c++14', '-Wall', '-Werror', '-c']
        for i in incpaths:
            opts += ['-I' + str(i)]
        if mode == BuildMode.debug:
            opts += ['-Og', '-g']
        else:
            opts += ['-O3']
        sp.run(['g++', self.path, '-o', self.inner()] + opts)
                
