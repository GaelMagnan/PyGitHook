"""
Hook task to check if a BOM is in the file.
Uses regex to check for presence of standard BOM. If any is present return False.
Inherite of this class and modify the regexes attribute for custom BOM representation.

AUTHOR:
    Gael Magnan de bornier
"""

import re

from src.Tasks.HookTask import HookModifiedFileTask

class CheckNoBOMTask(HookModifiedFileTask):
    """
    Hook task to check if a BOM is in the file.
    Uses regex to check for presence of standard BOM. If any is present return False.
    Inherite of this class and modify the regexes attribute for custom BOM representation.
    """
    regexes = ["^\xEF\xBB\xBF", "^\xFE\xFF", "^\xFF\xFE"]

    def execute(self, filename, file_value, **kwargs):
        """ Check for presence of a BOM"""
        print("> Checking BOM presence for '%s' ... " % (filename))
        i = 0
        error = False
        for line in file_value:
            i = i + 1
            for regex in self.regexes:
                err_code = re.search(regex, line)
                if err_code is not None:
                    print(">> BOM Error(%s) Line:%d, please check the file\n" % (str(err_code.group(0)), i))
                    error = True

        if not error:
            print(">> OK")

        return not error
