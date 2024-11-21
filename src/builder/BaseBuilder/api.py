from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from enum import EnumType,Enum
from pathlib import Path
from typing import Any, Iterable, Tuple , Self , TypeVar
from logging import Logger

from ..util.types import FileFilter

Arg = TypeVar("Arg",str,Enum,Path,int)

class ArgManagerAPI(ABC):
    
    Arg:EnumType
    
    @abstractmethod
    def addArg(self,name:Arg,value:Arg|Iterable[Arg]=None) -> Self : pass

    @abstractmethod
    def addArgs(self,*args:Tuple[Arg,Arg]) -> Self: pass

    @abstractmethod
    def removeArg(self,name) -> str : pass

    @abstractmethod
    def iterArg(self) -> Iterable[Tuple[str,str]]: pass

    @abstractmethod
    def getArg(self,name) -> str: pass

class CommandMeta(ABCMeta):
    def __matmul__(self,target:CmdGroupAPI) -> CommandAPI :
        target.addCommand(tmp:=self(target))
        return tmp

class CommandAPI(ArgManagerAPI,metaclass=CommandMeta):

    AvailableCustom:EnumType=None

    Arg:EnumType=None
    
    Global:ArgManagerAPI=None

    @abstractmethod
    def addDir(self,path:Arg,filter:FileFilter,recursion:bool=True) -> Self:pass

    @abstractmethod
    def addFile(self,path:Arg) -> Self:pass

    @abstractmethod
    def iterFiles(self) -> Iterable[Path]:pass

    @abstractmethod
    def setCustom(self,k,v) -> Self:pass

    @abstractmethod
    def getCustom(self,k) -> Any:pass

    @abstractmethod
    def showInfo(self) -> Self:pass
    
    @property
    @abstractmethod
    def command(self) -> str : pass

    @property
    @abstractmethod
    def group(self) -> CmdGroupAPI:pass

    @abstractmethod
    def start(self,workPath:Path|str) -> None: pass

    @abstractmethod
    def setWorkPath(self,workPath:Path|str) -> None: pass
    
class CmdGroupAPI(ArgManagerAPI):

    Global:ArgManagerAPI=None

    @abstractmethod
    def run(self) -> None:pass

    @property
    @abstractmethod
    def WorkPath(self) -> Path:pass

    @WorkPath.setter
    @abstractmethod
    def WorkPath(self,path:Arg) -> None:pass

    @property
    @abstractmethod
    def result(self) -> Any:pass
    
    @property
    def Name(self) -> str:pass

    @abstractmethod
    def addCommand(self,Command:CommandAPI) -> None:pass

    @abstractmethod
    def cmdlst(self) -> Iterable[str]:pass

class ProjectAPI(ABC):
    @abstractmethod
    def addGroup(self,name:Any,group:type[CmdGroupAPI]) -> None:pass
    
    @abstractmethod
    def runGroup(self,name:Any) -> None:pass
    
    @abstractmethod
    def getGroup(self,name:Any) -> CmdGroupAPI:pass
    
    @abstractmethod
    def start(self):pass