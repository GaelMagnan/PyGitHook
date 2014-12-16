#!/usr/bin/env python

import os
import sys
import json
import argparse
import stat
import string
import time

hooks_script = {'pre-receive': 'PreReceiveHook',
                'post-receive': 'PostReceiveHook',
                'update': 'UpdateHook',
                'pre-commit': 'PreCommitHook',
                'prepare-commit-msg': 'PrepareCommitMsgHook',
                'pre-push': 'PrePushHook'}

def get_args():
    parser = argparse.ArgumentParser(description="Installer for PyGitHook, this is a usefull tool but you can do it by hand.")
    parser.add_argument('-v', '--version', action='version', version="0.1")

    parser.add_argument('-gd', '--git_directory', action='store',
                        help="The directory of the git project you want to creat a hook for.")
    parser.add_argument('-pd', '--pygithook_directory', action='store', help="The directory of PyGitHook.")
    parser.add_argument('-ht', '--hook_type', action='store', help="The type of hook you want to create.")
    parser.add_argument('-t', '--tasks', nargs='+', help="The tasks you want your hook to execute.")

    return vars(parser.parse_args())


def get_hooks_path(git_directory):
    if os.path.exists(git_directory):
        if git_directory.endswith('.git'):
            git_hook_path = os.path.join(git_directory, "hooks")
        else:
            git_hook_path = os.path.join(git_directory, ".git/hooks")
        if os.path.exists(git_hook_path):
            return git_hook_path
        else:
            print("Invalid git directory, cannot find the {0} repertory".format(git_hook_path))
    else:
        print("Invalid git directory, this repertory doesn't exist")
    sys.exit(1)

def make_executable(file_path):
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IEXEC)

def create_hook(hook_type, git_hook_path, pygithook_path, tasks):
    hook_template = ("#!${exec} \n\n" +
                     "import sys\n\n" +
                     "sys.path.append('${PyGitHookPath}')\n\n" +
                     "from src.Hooks.Hook import main\n" +
                     "from src.Hooks.${HookType} import ${HookType}\n" +
                     reduce(lambda x, y: x + "from src.Tasks." + str(y) +
                            " import " + str(y) + "\n", tasks, "") +
                     "tasks = [${TasksList}]\n\n" +
                     "if __name__ == '__main__':\n" +
                     "    main( ${HookType}, tasks, '${ConfPath}' )\n")
    hook_template = string.Template(hook_template)

    params = {'exec': sys.executable,
              'PyGitHookPath': pygithook_path,
              'HookType': hooks_script[hook_type],
              'TasksList': ",".join(tasks),
              'ConfPath': os.path.join(pygithook_path, "conf")}

    file_name = os.path.join(git_hook_path, hook_type)

    if os.path.lexists(file_name):
        os.rename(file_name, "{0}.old{1}".format(file_name, time.time()))

    with open(file_name, "w") as hook_file:
        hook_file.write(hook_template.substitute(params))

    make_executable(file_name)

if __name__ == "__main__":
    args = get_args()
    hook_directory = os.path.abspath(args['git_directory'])
    hook_type = args['hook_type']
    pygithook_path = os.path.abspath(args['pygithook_directory'])
    tasks = args['tasks']

    if hook_type not in hooks_script.keys():
        print("Invalid hook_type({0}), should be one of:{1}".format((hook_type, hooks_script.keys())))
        sys.exit(1)

    hook_path = get_hooks_path(hook_directory)
    create_hook(hook_type, hook_path, pygithook_path, tasks)
