from pathlib import Path
from typing import Callable, List ,Any,Self

class FileFilter:
    def __init__(self) -> None:
        self.__rules=[]
        
    def addRule(self,rule:Callable[[Any],bool])->Self:
        self.__rules.append(rule)
        return self
            
    def __call__(self,value) -> bool:
        for rule in self.__rules:
            if not rule(value):
                return False
        return True
        
class PathList:
    def __init__(self) -> None:
        self.__paths=[]
    
    def add(self,path:Path) -> None:
        self.__paths.append(path)
    
    def remove(self,index:int) -> Path:
        return self.__paths.pop(index)
    
    def lst(self) -> List[Path]:
        return self.__paths.copy()