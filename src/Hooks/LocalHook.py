"""
Git local Hook.

AUTHOR:
    Gael Magnan de bornier
"""

from src.Utils import Bash
from src.Hooks.Hook import Hook
from src.Tasks import HookTask

class LocalHook(Hook):
    """
    Git local Hook.
    The simple python way to check what you are doing on your repository

    LocalHook is the base class for Hook that only impact your repository.
    """

    def get_file_diffs(self, **kwargs):
        command = ("git diff --cached --name-status -r" )
        ret_code, output = Bash.execute_command(command=command)
        if not ret_code:
            return output
        return ""

    def get_file(self, filename, **kwargs):
        ret_code, output = Bash.execute_command("git cat-file blob HEAD:%s " %
                                                filename)
        if not ret_code:
            return output
        else:
            print("read error file:%s" % filename)
        return None
