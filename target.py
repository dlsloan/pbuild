from __future__ import annotations
from pathlib import Path
from typing import Dict, Type

_src_dir = Path(__file__).absolute().parent

class Target:
    _initialized: bool = False
    _targets: Dict[str, Type[Target]] = {}

    @classmethod
    def get_targ(cls, proj: 'Project', file: Path, path: Path) -> Target:
        if cls._targets is None:
            cls._targets = {}
            for src in (_src_dir / 'targets').iterdir():
                if src.is_file() and src.suffix.lower() == ".py":
                    __import__(src)
        ext = path.suffix.lower()
        if ext not in cls._targets:
            raise ValueError(f"Unrecognized target {ext}")
        return cls._targets[ext](file, path)

    @classmethod
    def load(cls, proj: 'Project', file: Path):
        rel_file, path = cls.find(proj, file)
        if path is None:
            raise FileNotFoundError(rel_file)
        return Target.get_targ(proj, file, path)

    @classmethod
    def find(cls, proj: 'Project', file: Path):
        file = file.resolve(strict=False)
        if proj.path not in file.parents:
            return file, None
        file = file.relative_to(proj.path)
        if (proj.path / file).is_file():
            return file, proj.path / file
        pdir = proj.path / '.lib'
        if pdir.is_dir():
            for d in pdir.iterdir():
                if (d / file).is_file():
                    return file, d / file
        return file, None