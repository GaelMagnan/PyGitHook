"""
Task to check the PyLint grade of a file and reject if note is too low.

AUTHORS:
    Abdelhalim Kadi
"""


import re
import shlex
from subprocess import PIPE
from subprocess import Popen

from src.Tasks.CheckSyntaxTask import CheckSyntaxTask
from src.Tasks.HookTask import HookNewOrModifiedFileTask


class CheckPythonPyLintTask(CheckSyntaxTask, HookNewOrModifiedFileTask):
    """
    Task to check the PyLint grade of a file and reject if note is too low.
    """
    EVALUATION = re.compile(r"Your code has been rated at (-\d\.\d\d)/10|Your code has been rated at (\d\.\d\d)/10")
    ERRORS = re.compile(r"^E:.*\d+:", re.MULTILINE)
    MINIMUM_GRADE = 5.0
    PYLINT_COMMANDE = "pylint"
    PYLINT_FILE_NAME = "pylint.conf"


    def check_syntax(self, file_desc, filename=""):
        """Execute PyLint and parse the result, fails if the MINIMUM_GRADE is not obtained"""
        pylint_cmd = "%s --rcfile %s %s" % (self.PYLINT_COMMANDE, 
                                            self.conf_location + self.PYLINT_FILE_NAME,
                                            file_desc.name)
        process = Popen(shlex.split(pylint_cmd), stdout=PIPE, stderr=PIPE)
        (data, _errors) = process.communicate()

        error = self.ERRORS.search(data)
        if error:
            print(">>> " + "\n>>> ".join(data.split("\n")))
            return False

        evaluation = self.EVALUATION.search(data)
        if evaluation:
            value = evaluation.group(1) or evaluation.group(2)
            print(">> You where graded %s/10" % (float(value)))
            if float(value) < self.MINIMUM_GRADE:
                print(">>> " + "\n>>> ".join(data.split("\n")))
                return False

        return True
