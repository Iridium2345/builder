from ..BaseBuilder.impl import BaseCommand

from enum import Enum 
from pathlib import Path
import shutil
import os

class _src:
    def format(arg):
        return f"{arg}"
    
class _tar:
    def format(arg):
        return f"{arg}"

class Copy(BaseCommand):
    class Arg(Enum):
        Src=_src()
        Target=_tar()
    
    def getArgString(self):
        return ""
    
    def start(self, workPath):
        src,tar=self.getArg(self.Arg.Src),self.getArg(self.Arg.Target)
        print(f"Copy {src} to {tar}")
        if Path(src).is_dir():
            shutil.copytree(src,tar,dirs_exist_ok=True)
        else:
            shutil.copy2(src,tar)
        return 0

class Remove(BaseCommand):
    
    def start(self, workPath):
        print(f"remove dir {self.getFilesString()}")
        try:
            shutil.rmtree(self.getFilesString())
        except Exception as e:
            print(e)
        return 0

class Mkdir(BaseCommand):
    
    def start(self, workPath):
        print(f"create {self.getFilesString()}")
        os.makedirs(self.getFilesString(),exist_ok=True)
        return 0