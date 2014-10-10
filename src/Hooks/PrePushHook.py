"""
Git pre push Hook.
The simple python way to code a pre push Hook

ExchangeHook is the base class for every pre push Hook.

AUTHOR:
Gael Magnan de bornier
"""

import sys

from src.Hooks.ExchangeHook import ExchangeHook

class PrePushHook(ExchangeHook):

    def get_script_params(self, **kwargs):
        params = super(PrePushHook, self).get_script_params(**kwargs)
        params.update({'remote': params['$1'], 'url': '$2'})
        return params


    def get_refs_parameters(self, **kwargs):
        ret = []
        for line in sys.stdin.readlines():
            (local_ref, local_sha1,
             remote_ref, remote_sha1) = line.strip().split()
            if remote_ref == self.NO_REF_COMMIT:
                remote_ref = "master"
            ret.append({'local_ref': local_ref, 'local_sha1': local_sha1,
                        'remote_ref': remote_ref, 'remote_sha1': remote_sha1})
        return ret

    def get_files_params(self, ref_received, **kwargs):
        new_ref = []
        for ref in ref_received:
            ref.update(self.get_files_grouped_by_change(origin=ref['remote_ref'],
                                                        head=ref['local_ref']))
            new_ref.append(ref)

        return {'ref_received': new_ref}
