"""
Git exchange Hook.
The simple python way to control or act on the data being exchanged by git
commands

ExchangeHook is the base class for every exchange Hook.

AUTHOR:
    Gael Magnan de bornier
"""

import sys

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

    def get_line_params(self, **kwargs):
        return {'ref_received': self.get_refs_parameters(**kwargs)}

    def process(self, ref_received, **kwargs):
        """Main treatment, execute the tasks """
        try:
            tasks = self.get_tasks_group_by_type()
            for ref in ref_received:
                kwargs.update(ref)
                if 'newrev' in ref and ref['newrev'] == self.NO_REF_COMMIT:
                    print("Branch deletion not handler as of yet, doing nothing.")
                    return True
                if not self.execute_tasks_group_by_type(*tasks, **kwargs):
                    return False
            return True
        except Exception as e:
            print("An error occured during the runing of the script, "
                  "please report this following message to you administrator.")
            print(e)
            return False

    def get_file(self, filename, newrev, **kwargs):
        ret_code, output = Bash.execute_command("git cat-file blob %s:%s " %
                                                (newrev, filename))
        if not ret_code:
            return output
        else:
            print("read error file:%s:%s" % (newrev, filename))
        return None


    def get_file_diffs(self, origin, head, **kwargs):
        command = ("git diff-tree --no-commit-id --name-status -r %s %s" %
                   (origin, head))
        ret_code, output = Bash.execute_command(command=command)
        if not ret_code:
            return output
        return ""

    def get_refs_parameters(self, **kwargs):
        ret = []
        for line in sys.stdin.readlines():
            (base, commit, ref) = line.strip().split()
            if base == self.NO_REF_COMMIT:
                base = "master"
            ret.append({'oldrev': base, 'newrev': commit, 'refname': ref})
        return ret

    def get_files_params(self, ref_received, **kwargs):
        new_ref = []
        for ref in ref_received:
            ref.update(self.get_files_grouped_by_change(origin=ref['oldrev'],
                                                        head=ref['newrev']))
            new_ref.append(ref)

        return {'ref_received': new_ref}
