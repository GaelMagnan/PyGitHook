"""
Hook task to check if code syntax errors have been made.

This is a base class, extend it and implement check_syntax.

This class is a subclass of HookFileTask to be generic as possible.
You may want to also make your subclass extend either:
- HookNewFileTask
- HookNewOrModifiedFileTask
- HookModifiedFileTask

AUTHOR:
    Gael Magnan de bornier
"""

from src.Tasks.HookTask import HookFileTask

class CheckSyntaxTask(HookFileTask):

    def execute(self, file_desc, filename, conf_location="", **kwargs):

        self.conf_location = conf_location
        print("> validating syntax for '%s' ... " % filename)
        if not self.check_syntax(file_desc, filename):
            print(">> Synthax Error, please check the file\n")
            return False

        print(">> OK")
        return True



    def check_syntax(self, file_desc, filename=""):
        pass
