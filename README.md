PyGitHook
====================

What is PyGitHook?
---------------------

PyGitHook is a simple way to create git hooks using python.
It's also an easy way to share tasks with the community.


What do I need to use it?
---------------------

You just need to have python and git installed on your machine.


How do I use it?
---------------------

First you need to get PyGitHook.
Go to the location you want to put it and run:
> git clone https://github.com/GaelMagnan/PyGitHook.git

You then need to decide what type of Hook you want to create and what tasks you want your hook to execute

One that's done you can execute the PyGitHookDeployment script:
> Python PyGitHookDeployment.py -gd YourProjectDirectory -pd PyGitHookDirectory -ht Hook_type -t Your_Tasks

Example: I want a pre-commit hook that's gonna run CheckPythonPEP8Task for my project Test
> Python PyGitHookDeployment.py -gd /var/Test -pd /var/PyGitHookDirectory -ht pre-commit -t PyGitHookDirectory

And it's done, if you want to had tasks you can either run the script again or edit the hook script in /YourProjectDirectory/.git/hooks/hook_type


I don't find the task I want, what to do?
---------------------

If you know python you can easily implement your task, just go to PyGitHook/src/Tasks and add a python class that implements HookTask.
You just have to define the execute method, that will be run. You can select the parameters you want from the list of any Hook.

Once that's done and your tasks works fine, please share it with us if you can.
It's the easiest way to contribute to the project.
