"""
Hook task to check if a merge error has been made.
Uses regex to check for existance of standard merge separator.
Inherite of this class and modify the regex attribute for custom merge separator.

AUTHOR:
    Gael Magnan de bornier
"""

import re

from src.Tasks.HookTask import HookNewOrModifiedFileTask

class CheckMergeErrorTask(HookNewOrModifiedFileTask):

    regex = "^.*(>>>>>>>|<<<<<<<).*$"

    def execute(self, filename, file_value, **kwargs):

        print("> Checking bad merge for '%s' ... " % (filename))
        i = 0
        error = False
        for line in file_value:
            i = i + 1
            err_code = re.search(self.regex, line)
            if err_code is not None:
                print(">> Merge Errors(%s) Line:%d, please check the file\n" %
                      (str(err_code.group(0)), i))
                error = True

        if not error:
            print(">> OK")

        return not error
