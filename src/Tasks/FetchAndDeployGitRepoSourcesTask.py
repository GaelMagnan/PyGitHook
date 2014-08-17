"""
Hook task to get a repo from gitweb and give execute right to all python files.

Beware of bash.

AUTHOR:
    Gael Magnan de bornier
"""

from src.Tasks.HookTask import HookTask
from src.Utils import Bash

class FetchAndDeployGitRepoSourcesTask(HookTask):

    def execute(self, repo, newrev, to="/var/hooks", archive_name="tmp_repo_archive.tgz", **kwargs):

        ret_code, output = Bash.execute_command(command="wget -N http://dev-vil-1.priv.sewan.fr/git/?p=%s.git;" +
                                                "a=snapshot;h=%s;sf=tgz -O %s/%s" % (repo, newrev, to, archive_name))
        if not ret_code:
            print("> get archive done")

            ret_code, output = Bash.execute_command(command='tar -xzf %s/%s -C %s/ --strip 1' %
                                                    (to, archive_name, to))
            if not ret_code:
                print("> extract archive done")

                ret_code, output = Bash.execute_command(command="chmod +x -R %s/" % to)
                if not ret_code:
                    print("> give execution right done")
                else:
                    print("> give execution right error")
                    print("> " + ",".join(output))

            else:
                print("> extract archive error")
                print("> " + ",".join(output))

            ret_code, output = Bash.execute_command(command='rm -f %s/%s' % (to, archive_name))
            if not ret_code:
                print("> remove archive done")
            else:
                print("> remove archive error")
                print("> " + ",".join(output))

        else:
            print("> get archive error")
            print("> " + ",".join(output))
