from __future__ import annotations
from pathlib import Path
from target import Target

class Project:
    def __init__(self, main: Path):
        if main.is_dir():
            main = main / '.pbuild'
        if not main.is_file():
            raise FileNotFoundError(main)
        self.path = main.parent
        self.main = self.load(main)

    def load(self, file: Path) -> Target:
        return Target(file)