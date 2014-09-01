"""
Git pre commit Hook.
The simple python way to code a pre commit Hook

LocalHook is the base class for every pre commit Hook.

AUTHOR:
Gael Magnan de bornier
"""

from src.Utils import Bash
from src.Hooks.LocalHook import LocalHook

class PreCommitHook(LocalHook):

    def get_file(self, filename, **kwargs):
        ret_code, output = Bash.execute_command("git show :%s " % filename)
        if not ret_code:
            return output
        else:
            print("Read error file:%s" % filename)
        return None
