"""
Hook task to check prefix the commit message with the branch name you are on.

use with PrepareCommitMsgHook

AUTHOR:
    Gael Magnan de bornier
"""

from src.Tasks.HookTask import HookTask
from src.Utils import Bash

class PrefixWithBranchNameTask(HookTask):

    def execute(self, commit_msg_file, **kwargs):
        ret_code, output = Bash.execute_command('git rev-parse --abbrev-ref HEAD')
        if ret_code:
            print('An error occured trying to get the branch name')
            return False

        with open(commit_msg_file, 'r+') as commit_file:
            branch_name = output[0].rstrip('\r\n')
            content = commit_file.read()
            if not content.startswith(branch_name):
                commit_file.seek(0, 0)
                commit_file.write(branch_name + ':' + content)

        return True
