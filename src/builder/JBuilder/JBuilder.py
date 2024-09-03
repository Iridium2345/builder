from ..BaseBuilder.impl import BaseBuilder,BaseCommand,ArgManager
from ..util.types import FileFilter

from pathlib import Path
from enum import Enum

class JFilter:
    
    @staticmethod
    def JavaFile():
        return FileFilter().addRule(lambda x: x.suffix in (".java",))
    
    @staticmethod
    def ClassFile():
        return FileFilter().addRule(lambda x: x.suffix in (".class",))
    
class _javaCmd(BaseCommand):    
    def cmdName(self) -> str:pass
    def getExecutable(self):
        assert isinstance(self.project,JavaProject)
        return ("{}\\".format(self.project.JavaHome) if self.project.JavaHome else '' )+self.cmdName() 

class java(_javaCmd):
    
    Global=ArgManager()
    
    def cmdName(self) -> str:
        return "java"

class javac(_javaCmd):
    
    Global=ArgManager()
    
    def cmdName(self) -> str:
        return "javac"

class jar(_javaCmd):
    """
    jar tool
    
    **should put the arg 'f' before the arg 'm'**
    
    """
    Global=ArgManager()
    
    class AvailableCustom(Enum):
        jar_file="jar_file"
        jar_path="jar_path"
        mani_file="mani_file"
    
    def cmdName(self) -> str:
        return "jar"
    
    @property
    def command(self):
        jar_path=Path(self.project.WorkPath if
            not (tmp:=self.getCustom(self.AvailableCustom.jar_path)) else tmp)
        jar_path=jar_path.joinpath(x:=f"{self.project.Name}.jar" if
            not (tmp:=self.getCustom(self.AvailableCustom.jar_file)) else tmp)
        return "{} {} {} {} -C {}".format(
            self.getExecutable(),
            self.getArgString(),
            jar_path,
            self.getCustom(self.AvailableCustom.mani_file),
            self.getFilesString()
        )

class JavaProject(BaseBuilder):
    
    Global=ArgManager()
    
    def __init__(self, name,JavaHome:str=None) -> None:
        super().__init__(name)
        self.JavaHome=JavaHome
    
    @property
    def JavaHome(self):
        return self.__JavaHome
    
    @JavaHome.setter
    def JavaHome(self,JavaHome):
        self.__JavaHome=JavaHome