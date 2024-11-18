from ..BaseBuilder.impl import BaseGroup,BaseCommand,ArgManager,BaseProject
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
    
    @staticmethod
    def JarFile():
        return FileFilter().addRule(lambda x: x.suffix in (".jar",))
    
class _javaCmd(BaseCommand):    
    def cmdName(self) -> str:pass
    def getExecutable(self):
        assert isinstance(self.group,JavaGroup)
        return ("{}\\".format(self.group.JavaHome) if self.group.JavaHome else '' )+self.cmdName() 

class _class_path_list:
    
    def __init__(self,arg) -> None:
        self.arg=arg
    
    def format(self,class_path):
        return self.arg+" "+";".join(map(str,class_path))        

class _props:

    def format(self,vars):
        return " ".join(map(lambda x:f"-D{x}",vars))
    
class java(_javaCmd):
    
    class Arg(Enum):
        Version="-version"
        Jar="-jar"
        Class_Path=_class_path_list("-classpath") 
        Maximum_Heap_Size="-Xmx{}"
        Initial_Heap_Size="-Xms{}"
        Thread_Stack_Size="-Xss{}"
        Var=_props()
        
    Global=ArgManager()
    
    def cmdName(self) -> str:
        return "java"

class javac(_javaCmd):
    
    class Arg(Enum):
        Version="-version"
        Dir="-d {}"
        SourceParh="-sourcepath {}"
        Encoding="-encoding {}"
        Class_Path=_class_path_list("-classpath")
    
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
        
        self.group:JavaGroup
        
        jar_path=Path(self.group.WorkPath if
            not (tmp:=self.getCustom(self.AvailableCustom.jar_path)) else tmp)
        jar_path=jar_path.joinpath(f"{self.group.Name}.jar" if
            not (tmp:=self.getCustom(self.AvailableCustom.jar_file)) else tmp)
        
        self.group.result=jar_path
        
        return "{} {} {} {} {}".format(
            self.getExecutable(),
            self.getArgString(),
            jar_path,
            tmp if (tmp:=self.getCustom(self.AvailableCustom.mani_file)) else "",
            self.getFilesString()
        )

class JavaGroup(BaseGroup):
    
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

class JavaProject(BaseProject):
    pass