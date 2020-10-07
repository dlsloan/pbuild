from cparse import CCmntParse, CIncludeParce
from sourcefile import SourceFile

class CSource(SourceFile):
    def __init__(self, filename):
        super().__init__(filename)

    def comments(self):
        return CCmntParse(self.path)

    def _dependencies(self):
        return CIncludeParce(self.path)

    def inner(self):
        return self.path + ".obj"
