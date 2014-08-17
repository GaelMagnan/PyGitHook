"""
Base Hook for post receive treatment.

AUTHOR:
    Gael Magnan de bornier
"""

from src.Hooks.ExchangeHook import ExchangeHook

class PostReceiveHook(ExchangeHook):
    """
    Base Hook for post receive treatment.
    """

    def process(self, **kwargs):
        """Main treatment, execute the tasks return False if any task fails"""
        tasks = self.get_tasks_group_by_type()

        for ref in kwargs['ref_received']:
            kwargs.update(ref)
            if not self.execute_tasks_group_by_type(*tasks, **kwargs):
                return False
        return True

    def get_exec_params(self):
        """Reads the standard input to get execution parameters returns a dict of params"""
        ret = super(PostReceiveHook, self).get_exec_params()
        lines_args = self.get_refs_parameters()
        ret['ref_received'] = lines_args
        return ret
