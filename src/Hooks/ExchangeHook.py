"""
Git exchange Hook.
The simple python way to control or act on the data being exchanged by git
commands

ExchangeHook is the base class for every exchange Hook.

AUTHOR:
    Gael Magnan de bornier
"""


from src.Utils import Bash
from src.Hooks.Hook import Hook

class ExchangeHook(Hook):
    """
    Git echange Hook.
    The simple python way to control or act on the data being exchanged by git
    commands

    ExchangeHook is the base class for every echange Hook.
    """

    NO_REF_COMMIT = 40 * '0'


    def get_file(self, filename, newrev, **kwargs):
        ret_code, output = Bash.execute_command("git cat-file blob %s:%s " %
                                                (newrev, filename))
        if not ret_code:
            return output
        else:
            print("read error file:%s:%s" % (newrev, filename))
        return None


    def get_file_diffs(self, origin, head):
        command = ("git diff-tree --no-commit-id --name-status -r %s %s" %
                   (origin, head))
        ret_code, output = Bash.execute_command(command=command)
        if not ret_code:
            return output
        return ""


    def get_refs_parameters(self):
        ret = []
        for line in sys.stdin.readlines():
            (base, commit, ref) = line.strip().split()
            ret.append({'oldrev': base, 'newrev': commit, 'refname': ref})
        return ret
