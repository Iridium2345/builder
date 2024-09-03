from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from enum import EnumType
from pathlib import Path
from typing import Any, Iterable, Tuple , Self

from ..util.types import FileFilter

class ArgManagerAPI(ABC):
    @abstractmethod
    def addArg(self,name:str,value:str|Iterable=None) -> Self : pass

    @abstractmethod
    def addArgs(self,*args:Tuple[str,str|None]) -> Self: pass

    @abstractmethod
    def removeArg(self,name) -> str : pass

    @abstractmethod
    def iterArg(self) -> Iterable[Tuple[str,str]]: pass


class CommandMeta(ABCMeta):
    def __matmul__(self,target:BuilderAPI) -> CommandAPI :
        target.addCommand(tmp:=self(target))
        return tmp

class CommandAPI(ArgManagerAPI,metaclass=CommandMeta):

    AvailableCustom:EnumType=None

    Global:ArgManagerAPI=None

    @abstractmethod
    def addDir(self,path:Path|str,filter:FileFilter,recursion:bool=True) -> Self:pass

    @abstractmethod
    def addFile(self,path:Path|str) -> Self:pass

    @abstractmethod
    def iterFiles(self) -> Iterable[Path]:pass

    @abstractmethod
    def setOutputPath(self,path:str|Path) -> Self:pass

    @abstractmethod
    def setCustom(self,k,v) -> Self:pass

    @abstractmethod
    def getCustom(self,k) -> Any:pass

    @property
    @abstractmethod
    def command(self) -> str : pass

    @property
    @abstractmethod
    def project(self) -> BuilderAPI:pass

    @abstractmethod
    def start(self,workPath:Path|str) -> None: pass


class BuilderAPI(ArgManagerAPI):

    Global:ArgManagerAPI=None

    @abstractmethod
    def build(self) -> None:pass

    @property
    @abstractmethod
    def WorkPath(self) -> Path:pass

    @WorkPath.setter
    @abstractmethod
    def WorkPath(self,path:Path|str) -> None:pass

    @property
    def Name(self) -> str:pass

    @abstractmethod
    def addCommand(self,Command:CommandAPI) -> None:pass
