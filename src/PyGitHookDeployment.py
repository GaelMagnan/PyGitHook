#!python

import os
import sys
import json
import argparse
import stat
import string

hooks_script = {'pre-receive': 'PreReceiveHook',
				'post-receive': 'PostReceiveHook',
				'update': 'UpdateHook',
				'pre-commit': 'PreCommitHook',
				'prepare-commit-msg': 'PrepareCommitMsgHook',
				'pre-push': 'PrePushHook'}

def get_args():
	parser = argparse.ArgumentParser(description="Installer for PyGitHook, this is a usefull tool but not necessary you can also do it by hand.")
	parser.add_argument('-v', '--version', action='version', version="0.1")

	manual_conf_group = parser.add_argument_group(title='Manual Conf')
	file_conf_group = parser.add_argument_group(title='File Conf')

	manual_conf_group.add_argument('-gd', '--git_directory', action='store', help="The directory of the git project you want to creat a hook for.")
	manual_conf_group.add_argument('-pd', '--pygithook_directory', action='store', help="The directory of PyGitHook.")
	manual_conf_group.add_argument('-ht', '--hook_type', action='store', help="The type of hook you want to create.")
	manual_conf_group.add_argument('-t', '--tasks', nargs='+', help="The tasks you want your hook to execute.")

	file_conf_group.add_argument('-f', '--file', action='store', help="A json config file used to configure your hook.")

	return vars(parser.parse_args())


def get_hooks_path(git_directory):
    if os.path.exists(git_directory):
        git_hook_path = os.path.join(git_directory, ".git/hooks")
        if os.path.exists(git_hook_path):
            return git_hook_path
        else:
            print("Invalid git directory, cannot find the .git/hooks repertory")
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
					 reduce(lambda x,y:x + "from src.Tasks." + str(y) +
					  		" import " + str(y) + "\n", tasks, "") +
					 "tasks = [${TasksList}]\n\n" +
					 "if __name__ == '__main__':\n" +
					 "    main( ${HookType}, tasks, ${ConfPath} )\n")
	hook_template = string.Template(hook_template)

	params = {'exec' : sys.executable,
			  'PyGitHookPath': pygithook_path,
			  'HookType': hooks_script[hook_type],
			  'TasksList': ",".join(tasks),
			  'ConfPath': os.path.join(pygithook_path, "conf")}

	file_name = os.path.join(git_hook_path, hook_type)

	with open(file_name,"w") as hook_file:
		hook_file.write(hook_template.substitute(params))

	make_executable(file_name)


def get_config_from_file(file_path):
	with open(file_path, "r") as config_file:
		config = json.load(config_file)

	return config


if __name__ == "__main__":
	args = get_args()
	if args.get('file',None):
		(hook_directory, hook_type, pygithook_path,
		 tasks) = get_config_from_file(args['file'])
	else:
		hook_directory = args['git_directory']
		hook_type = args['hook_type']
		pygithook_path = args['pygithook_directory']
		tasks = args['tasks']

	if hook_type not in hooks_script.keys():
		print("Invalid hook_type(%s), should be one of:%s" %
			  (hook_type, str(HOOK_TYPE_LIST)))
		sys.exit(1)

	hook_path = get_hooks_path(hook_directory)
	create_hook(hook_type, hook_path, pygithook_path, tasks)
