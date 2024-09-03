from __future__ import annotations

from .api import ArgManagerAPI, BuilderAPI, CommandAPI
from ..util.types import FileFilter

from pathlib import Path 
from typing import Iterable,List,Tuple,Self,Any
from enum import Enum
from collections.abc import Iterator
import subprocess

def enum2value(name:Enum) -> Any:
    if isinstance(name,Enum):
        name=name.value
    return name

class ArgManager(ArgManagerAPI):
    
    def __init__(self) -> None:
        super().__init__()
        self.__args={}
    
    def addArg(self, name: str|Enum, value: str|Iterable[str] = None) -> Self:
        name=enum2value(name)
        self.__args[name]=value if not isinstance(value,(list,tuple)) else " ".join(value)
        return self
        
    def addArgs(self,*args:Tuple[str|Enum,str|None]) -> Self:
        for arg in args:
            self.addArg(*arg)
        return self
    
    def removeArg(self, name) -> str:
        return self.__args.pop(name)
    
    def iterArg(self) -> Iterable:
        yield from self.__args.items()
    
class BaseCommand(ArgManager,CommandAPI):
    
    Global=ArgManager()
    
    def __init__(self,project:CommandAPI) -> None:
        self.__files=[]
        super().__init__()
        self.addArgs(*project.iterArg())
        self.__custom={}
        self.__project:BuilderAPI=project
    
    def setCustom(self,k, v) -> Self:
        self.__custom[k]=v
        return self
    
    def getCustom(self, k) -> Any:
        return self.__custom[k] if k in self.__custom.keys() else None
    
    def getExecutable(self):
        return ""
        
    def getArgString(self):
        self.addArgs(*self.Global.iterArg())
        return " ".join([f"{key} {value if not value is None else ''}" for key,value in self.iterArg()])
        
    def getFilesString(self):
        return " ".join([str(path) for path in self.iterFiles()])
    
    def addDir(self, path: Path|str|Enum, filter: FileFilter, recursion: bool = True) -> Self:
        path=enum2value(path)
        path=Path(path)
        for pth in path.iterdir():
            if pth.is_file():
                if filter(pth):self.__files.append(pth)
            elif recursion:
                self.addDir(pth,filter)
        return self
    
    def addFile(self, path: Path | str) -> Self:
        path=enum2value(path)
        self.__files.append(path)
        return self
    
    def iterFiles(self) -> Iterable[Path|str]:
        yield from self.__files
    
    @property
    def project(self) -> BuilderAPI:
        return self.__project
    
    @property
    def command(self):
        return f"{self.getExecutable()} {self.getArgString()} {self.getFilesString()}"
    
    def start(self,workPath:Path|str) -> None:
        return subprocess.run(self.command,cwd=workPath.absolute()).returncode 
    
class BaseBuilder(ArgManager,BuilderAPI):
    
    Global=ArgManager()
    
    def __init__(self,name) -> None:
        super().__init__()
        self.name=name
        self.__commands:List[CommandAPI]=[]
        self.__WorkPath=None
    
    @property
    def Name(self):
        return self.name
    
    def cmdlst(self):
        for command in self.__commands:
            yield command.command
    
    def build(self) -> None:
        for command in self.__commands:
            if not (code:=command.start(self.WorkPath)) == 0:
                print(f"sub proccess '{command.command}' exit with code {code} , build stoped")
                return
        print("successed")
    
    def addCommand(self, Command: CommandAPI) -> None:
        self.__commands.append(Command)
    
    @property
    def WorkPath(self) -> Path:
        if not self.__WorkPath:raise ValueError("WorkPath not set")
        return self.__WorkPath
        
    @WorkPath.setter
    def WorkPath(self,path:Path|str|Enum) -> None:
        path=enum2value(path)
        self.__WorkPath=Path(path)
    
    