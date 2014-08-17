"""
Hook task to check if python syntax error have been made using PEP8.

You can ignore some errors by adding them to IGNORE_CODES

AUTHOR:
    Gael Magnan de bornier
"""

from src.Tasks.CheckSyntaxTask import CheckSyntaxTask
from src.Tasks.HookTask import HookNewOrModifiedFileTask
from src.Utils import Bash

class CheckPythonPEP8Task(CheckSyntaxTask, HookNewOrModifiedFileTask):

    PEP8_FILE_NAME = "pep8.conf"

    def check_syntax(self, file_desc, filename=""):

        if filename[len(filename) - 3:] != ".py":
            print("%s doesn't end with .py we ignore it" % filename)
            return True
        ret_code, output = Bash.execute_command(command="pep8 --config=%s %s" %
                                                (self.CONF_LOCATION + self.PEP8_FILE_LOCATION, file_desc.name))
        if not ret_code:
            return True
        else:
            for line in output:
                print("> " + line.replace(file_desc.name, filename))
            return False

