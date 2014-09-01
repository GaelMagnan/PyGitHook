"""
Hook task to check if PHP syntax errors have been made by using php -l on the file.


AUTHOR:
    Gael Magnan de bornier
"""

from src.Tasks.CheckSyntaxTask import CheckSyntaxTask
from src.Tasks.HookTask import HookNewOrModifiedFileTask
from src.Utils import Bash

class CheckPHPTask(CheckSyntaxTask, HookNewOrModifiedFileTask):

    def check_syntax(self, file_desc, filename=""):
        if filename[len(filename) - 4:] != ".php":
            print("%s doesn't end with .php we ignore it" % filename)
            return True
        ret_code, output = Bash.execute_command(command=("php -l %s" %
                                                         file_desc.name))
        if not ret_code:
            return True
        else:
            print("> " + ",".join(output))
            return False
