import subprocess as sp

from pathlib import Path

def _git(*cmd):
    giturl = cmd[3]
    libname = giturl.split('/')[-1].split('.')[0]
    libpath = Path('.lib')
    if not libpath.is_dir():
        libpath.mkdir()
    sp.run(['git', 'clone', giturl, str(libpath / libname)])

PBuildCommands = {
    'git': _git
}
