"""
Hook task to check if python syntax error have been made using PEP8.

You can ignore some errors by adding them in the ignore list in the conf.

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
        config = self.conf_location + self.PEP8_FILE_LOCATION
        command = "pep8 --config=%s %s" % (config, file_desc.name)
        ret_code, output = Bash.execute_command(command=command)
        if not ret_code:
            return True
        else:
            for line in output:
                print("> " + line.replace(file_desc.name, filename))
            return False
