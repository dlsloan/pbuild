#!/usr/bin/env python3

#Copyright (C) 2020 David Sloan

#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.

#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the GNU
#Lesser General Public License for more details.

#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, see <http://www.gnu.org/licenses/>.

import os

from argparse import ArgumentParser
from pathlib import Path
from sourcefile import BuildMode, SourceFile

if __name__ == '__main__':
    parser = ArgumentParser(description='Project Builder')
    parser.add_argument('target')
    parser.add_argument('--mode', '-m', default=BuildMode.release, type=BuildMode, choices=list(BuildMode))

    args = parser.parse_args()

    prjBase = Path(args.target)
    prj = SourceFile.as_project(prjBase)
    prj.build(mode=args.mode)
