"""
Hook task to check if a python synthax error has been made using pyflakes.

You can ignore some errors by adding them to PYFLAKES_EXCLUSION_LIST

AUTHOR:
    Gael Magnan de bornier
"""

from src.Tasks.CheckSyntaxTask import CheckSyntaxTask
from src.Tasks.HookTask import HookNewOrModifiedFileTask
from src.Utils import Bash

class CheckPythonPyflakesTask(CheckSyntaxTask, HookNewOrModifiedFileTask):

    PYFLAKES_EXCLUSION_LIST = []


    def check_syntax(self, file_desc, filename=""):
        ret_code, output = Bash.execute_command(command="/usr/local/bin/pyflakes %s" % file_desc.name)
        if not ret_code:
            return True
        else:
            return self.check_error_code_against_pyflakes_exclusion_list(output)



    def check_error_code_against_pyflakes_exclusion_list(self, output):
        errors = output
        real_errors = []
        for error in errors:
            if error and len(error):
                found = False
                for regex in self.PYFLAKES_EXCLUSION_LIST:
                    if regex in error:
                        found = True
                        break
                if not found:
                    real_errors.append(error)

        if len(real_errors) > 0:
            print(">> " + '\n>>'.join(real_errors))
            return False

        return True
