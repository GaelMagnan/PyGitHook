"""
Git pre push Hook.
The simple python way to code a pre push Hook

ExchangeHook is the base class for every pre push Hook.

AUTHOR:
Gael Magnan de bornier
"""

from src.Hooks.ExchangeHook import ExchangeHook

class PrePushHook(ExchangeHook):

    def get_exec_params(self):
        params = super(PrePushHook, self).get_exec_params()
        params['remote'] = params['$1']
        params['url'] = params['$2']
        ret['ref_received'] = self.get_refs_parameters()
        return params

    def process(self, **kwargs):
        """Main treatment, execute the tasks """
        tasks = self.get_tasks_group_by_type()

        for ref in kwargs['ref_received']:
            kwargs.update(ref)
            if not self.execute_tasks_group_by_type(*tasks, **kwargs):
                return False
        return True

    def get_refs_parameters(self):
        ret = []
        for line in sys.stdin.readlines():
            (local_ref, local_sha1,
            remote_ref, remote_sha1) = line.strip().split()
            ret.append({'local_ref': local_ref, 'local_sha1': local_sha1,
                        'remote_ref': remote_ref, 'remote_sha1':remote_sha1})
        return ret
