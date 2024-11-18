from ..BaseBuilder.impl import BaseCommand

from enum import Enum

class xelatex(BaseCommand):
    class Arg(Enum):
        Aux_directory = "-aux-directory={}"
        Include_directory = "-include-directory={}"
        Output_directory = "-output-directory={}"
        Interaction = "-interaction={}"
    
    def getExecutable(self):
        return "xelatex"