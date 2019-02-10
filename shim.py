#!/usr/bin/env python3

import os
import pathlib
import subprocess
import sys


def exit_missing_file(path):
    print('File not found: {}'.format(path))
    print('Run `dump-path.bat` from the desired "Tools Command Prompt".')
    print('(You probably want "x64 Native Tools Command Prompt for VS 2017")')
    exit(1)


try:
    dump_file = pathlib.Path(__file__).parent / '.msvc-path.txt'
    data = dump_file.read_text()

except FileNotFoundError:
    import traceback
    traceback.print_exc()
    exit_missing_file(cl_path)


data = [x for x in data.split('\n') if x]
(INCLUDE, LIB, cl_path) = data

CL_ENV = dict(os.environ)
try:
    CL_ENV['INCLUDE'] += ';' + INCLUDE
except KeyError:
    CL_ENV['INCLUDE'] = INCLUDE

try:
    CL_ENV['LIB'] += ';' + LIB
except KeyError:
    CL_ENV['LIB'] = LIB


def shim_and_exit(args):
    bin_path = pathlib.PurePath(args[0])
    bin_path = pathlib.Path(cl_path).parent / bin_path.name
    args[0] = str(bin_path)

    try:
        p = subprocess.run(args, env=CL_ENV)
    except FileNotFoundError:
        exit_missing_file(args[0])

    exit(p.returncode)


if __name__ == '__main__':
    (_, *args) = sys.argv
    shim_and_exit(args)
