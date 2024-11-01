from enum import Enum
from typing import Any,Iterable
from pathlib import Path

from .types import FileFilter
from ..BaseBuilder.api import Arg

def enum2value(name:Enum) -> Any:
    if isinstance(name,Enum):
        name=name.value
    return name

def fileSearch(path:Enum|str|Path,filefilter:FileFilter=None,recursion:bool=True) -> list:
    return list(_fileSearch(path,filefilter,recursion))

def _fileSearch(path:Enum|str|Path,filefilter:FileFilter=None,recursion:bool=True) -> Iterable[Path]:
    path=Path(enum2value(path))
    for pth in path.iterdir():
        if pth.is_file():
            if filefilter(pth):
                yield pth
        elif recursion:
            yield from _fileSearch(pth,filefilter,recursion)
    return

