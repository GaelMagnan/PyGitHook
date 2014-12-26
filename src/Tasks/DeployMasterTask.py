"""
Hook task to deploy the last version of master.

AUTHOR:
    Gael Magnan de bornier
"""

from src.Tasks.HookTask import HookTask
from src.Utils.Bash import execute_piped_command

class DeployMasterTask(HookTask):
    """
    Hook task to deploy the last version of master.
    """

    def execute(self, refname, to="/var/PyGitHook/", **kwargs):
        if refname != "refs/heads/master":
            print("This branch({0}) is not master, nothing to do.".format(refname))
            return True

        command1 = "git archive --format=tar master"
        command2 = "tar xf - -C %s" % to
        ret_code, output = execute_piped_command(command1=command1, command2=command2)
        if ret_code:
            print("Error getting the archive from master. Contact your administrator.")
            print("command:{0} | {1}".format(command1, command2))
            print("ret_code:{0} output:{1}".format(ret_code, output))
            return False

        print("master has been successfully deployed in {0}".format(to))
        return True
