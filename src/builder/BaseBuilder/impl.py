from __future__ import annotations

from .api import ArgManagerAPI, CmdGroupAPI, CommandAPI ,Arg ,ProjectAPI
from ..util.types import FileFilter
from ..util.func import enum2value

from pathlib import Path 
from typing import Iterable,List,Tuple,Self,Any,Dict
from collections import OrderedDict
from enum import Enum
import subprocess


class ArgManager(ArgManagerAPI):
    
    def __init__(self) -> None:
        super().__init__()
        self.__args={}
    
    def addArg(self, name: Any, value: Arg|Iterable[Arg] = None) -> Self:
        # name=enum2value(name)
        value=enum2value(value)
        self.__args[name]=value
        return self
        
    def addArgs(self,*args:Tuple[Arg,Arg|None]) -> Self:
        for arg in args:
            self.addArg(*arg)
        return self
    
    def removeArg(self, name) -> str:
        return self.__args.pop(name)
    
    def iterArg(self) -> Iterable[Tuple[str,str]]:
        yield from self.__args.items()
        
    def getArg(self, name):
        return self.__args[name] if name in self.__args.keys() else None
    
class BaseCommand(ArgManager,CommandAPI):
    
    Global=ArgManager()
    
    def __init__(self,project:CommandAPI) -> None:
        self.__files=[]
        super().__init__()
        self.addArgs(*project.iterArg())
        self.__custom={}
        self.__group:CmdGroupAPI=project
        self.workPath = None
    
    def setCustom(self,k, v) -> Self:
        self.__custom[k]=enum2value(v)
        return self
    
    def getCustom(self, k) -> Any:
        return self.__custom[k] if k in self.__custom.keys() else None
    
    def getExecutable(self):
        return ""
        
    def getArgString(self):
        self.addArgs(*self.Global.iterArg())
        return " ".join([(key.value if isinstance(key,Enum) else key).format("" if value is None else value) for key,value in self.iterArg()])
        
    def getFilesString(self):
        return " ".join([str(path) for path in self.iterFiles()])
    
    def addDir(self, path: Arg, filter: FileFilter, recursion: bool = True) -> Self:
        path=enum2value(path)
        path=Path(path)
        for pth in path.iterdir():
            if pth.is_file():
                if filter(pth):self.__files.append(pth)
            elif recursion:
                self.addDir(pth,filter)
        return self
    
    def addFile(self, path: Arg) -> Self:
        path=enum2value(path)
        self.__files.append(path)
        return self
    
    def iterFiles(self) -> Iterable[Path|str]:
        yield from self.__files
    
    @property
    def group(self) -> CmdGroupAPI:
        return self.__group
    
    @property
    def command(self):
        return f"{self.getExecutable()} {self.getArgString()} {self.getFilesString()}"
    
    def showInfo(self):
        print(
            f"WorkAt:{self.workPath}",
            f"Command:{self.command}",
            f"Group:{self.group}",
            sep="\n"
        )
        return self
    
    def start(self,workPath:Path|str) -> None:
        if(self.workPath):workPath = self.workPath
        return subprocess.run(self.command,cwd=workPath.absolute(),check=True,shell=True).returncode 
    
    def setWorkPath(self, path):
        self.workPath = path
        return self
    
class BaseGroup(ArgManager,CmdGroupAPI):
    
    Global=ArgManager()
    
    def __init__(self,name) -> None:
        super().__init__()
        self.name=name
        self.__commands:List[CommandAPI]=[]
        self.__WorkPath=None
        self.__result=None
        
    @property
    def Name(self):
        return self.name
    
    def cmdlst(self):
        for command in self.__commands:
            yield command.command
    
    def run(self) -> None:
        for command in self.__commands:
            if not (code:=command.start(self.WorkPath)) == 0:
                print(f"sub command '{command.command}' exit with code {code} , build stoped")
                return
        print(f"Command Group {self.Name} execute")
    
    @property
    def result(self):
        for _ in self.cmdlst():pass
        return self.__result
    
    @result.setter
    def result(self,value):
        self.__result=value
    
    def addCommand(self, Command: CommandAPI) -> None:
        # if len(self.__commands)>0:print(self.__commands[-1].command)
        self.__commands.append(Command)
    
    @property
    def WorkPath(self) -> Path:
        if not self.__WorkPath:raise ValueError("WorkPath not set")
        return self.__WorkPath
        
    @WorkPath.setter
    def WorkPath(self,path:Arg) -> None:
        path=enum2value(path)
        self.__WorkPath=Path(path)
    

class BaseProject(ProjectAPI):
    
    def __init__(self) -> None:
        super().__init__()
        self.__group:OrderedDict[Any,CmdGroupAPI]=OrderedDict()    
    
    def addGroup(self, name: Any, group: type[CmdGroupAPI]) -> CmdGroupAPI:
        self.__group[name]=group(name)
        return self.__group[name]
    
    def runGroup(self, name: Any) -> None:
        self.__group[name].run()
    
    def getGroup(self, name: Any) -> CmdGroupAPI:
        return self.__group[name] if name in self.__group.keys() else None
    
    def start(self):
        for group in self.__group.values():
            group.run()