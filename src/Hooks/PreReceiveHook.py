"""
Base Hook for pre-receive treatment.
Similar to Update instead that it is executed one for
every branch pushed when update is executed one by branch
if pre-receive fails nothing is updated

AUTHOR:
    Gael Magnan de bornier
"""

from src.Hooks.ExchangeHook import ExchangeHook

class PreReceiveHook(ExchangeHook):
    """
    Base Hook for pre-receive treatment.
    Similar to Update instead that it is executed one for
    every branch pushed when update is executed one by branch
    if pre-receive fails nothing is updated
    """

    def process(self, **kwargs):
        """Main treatment, execute the tasks """
        tasks = self.get_tasks_group_by_type()

        for ref in kwargs['ref_received']:
            kwargs.update(ref)
            if not self.execute_tasks_group_by_type(*tasks, **kwargs):
                return False
        return True



    def get_exec_params(self):
        """Reads the standard input to get execution parameters"""

        ret = super(PreReceiveHook, self).get_exec_params()
        lines_args = self.get_refs_parameters()
        for line in lines_args:
            compare_from = line['oldrev']
            if compare_from == self.NO_REF_COMMIT:
                compare_from = "master"
            line.update(self.get_list_of_files_changed_divided_by_change(origin=compare_from,
                                                                         head=line['newrev']))
        ret['ref_received'] = lines_args
        return ret
