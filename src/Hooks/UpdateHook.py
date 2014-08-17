"""
Base Hook for update treatment.

AUTHOR:
    Gael Magnan de bornier
"""

from src.Hooks.ExchangeHook import ExchangeHook

class UpdateHook(ExchangeHook):
    """
    Base Hook for update treatment.
    """

    def get_exec_params(self):
        """Reads the standard input to get execution parameters"""

        ret = super(UpdateHook, self).get_exec_params()
        lines_args = self.get_refs_parameters()
        if lines_args:
            line = lines_args[0]
            compare_from = line['oldrev']
            if compare_from == self.NO_REF_COMMIT:
                compare_from = "master"
            line.update(self.get_list_of_files_changed_divided_by_change(origin=compare_from,
                                                                         head=line['newrev']))
            ret.update(line)
        return ret
