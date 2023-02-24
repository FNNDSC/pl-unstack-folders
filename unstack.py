#!/usr/bin/env python
import shutil
import sys
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter

from chris_plugin import chris_plugin

__version__ = '1.0.0'

DISPLAY_TITLE = r"""
       _                        _             _            __      _     _               
      | |                      | |           | |          / _|    | |   | |              
 _ __ | |______ _   _ _ __  ___| |_ __ _  ___| | ________| |_ ___ | | __| | ___ _ __ ___ 
| '_ \| |______| | | | '_ \/ __| __/ _` |/ __| |/ /______|  _/ _ \| |/ _` |/ _ \ '__/ __|
| |_) | |      | |_| | | | \__ \ || (_| | (__|   <       | || (_) | | (_| |  __/ |  \__ \
| .__/|_|       \__,_|_| |_|___/\__\__,_|\___|_|\_\      |_| \___/|_|\__,_|\___|_|  |___/
| |                                                                                      
|_|                                                                                      
"""


parser = ArgumentParser(description='Copy deeply nested paths to the top-level.',
                        formatter_class=ArgumentDefaultsHelpFormatter)


@chris_plugin(
    parser=parser,
    title='Unstack Folders',
    category='',                 # ref. https://chrisstore.co/plugins
    min_memory_limit='100Mi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(_options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE, file=sys.stderr, flush=True)
    nested = find_nested(inputdir)

    if nested.is_dir():
        target = outputdir
        copy_func = lambda a, b: shutil.copytree(a, b, dirs_exist_ok=True)
    else:
        target = outputdir / nested.name
        copy_func = shutil.copy2

    print(f'{nested} -> {target}', flush=True)
    copy_func(nested, target)


def find_nested(p: Path, is_first=True) -> Path:
    if not p.is_dir():
        return p
    if contains_multiple_subpaths_or_is_empty(p, is_first):
        return p
    return find_nested(subpath_in(p), False)


def contains_multiple_subpaths_or_is_empty(p: Path, is_first: bool) -> bool:
    i = iter(p.glob('*'))
    if is_first:
        i = filter(is_not_special_file, i)
    if next(i, None) is None:
        return True
    return next(i, None) is not None


def is_not_special_file(p: Path) -> bool:
    return p.name not in ('input.meta.json', 'output.meta.json')


def subpath_in(p: Path) -> Path:
    return next(iter(p.glob('*')))


if __name__ == '__main__':
    main()
