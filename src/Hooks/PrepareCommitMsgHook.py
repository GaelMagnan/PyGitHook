"""
Git prepare commit message Hook.
The simple python way to code a prepare commit message Hook

LocalHook is the base class for every prepare commit msg Hook.

AUTHOR:
Gael Magnan de bornier
"""

from src.Hooks.LocalHook import LocalHook

class PrepareCommitMsgHook(LocalHook):

    def get_exec_params(self):
        params = super(PrepareCommitMsgHook, self).get_exec_params()
        params.extend(get_file_parameters())
        return params

def get_file_parameters():
    line = sys.stdin.readline()
    (commit_msg_file, commit_desc) = line.strip().split()
    return {'commit_msg_file': commit_msg_file, 'commit_desc': commit_desc}
