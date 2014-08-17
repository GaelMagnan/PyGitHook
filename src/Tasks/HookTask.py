"""
Git Task for hooks.

HookTask is the base class for every tasks.
HookFileTask is a subclass of HookTask for tasks that should be run on each updated files.
4 subclass exists to be applied to different type of the change.

AUTHOR:
    Gael Magnan de bornier
"""

class HookTask(object):

    def execute(self, **kwargs):
        """Main function of a Task, will be called by the Hook
        This is the only function that has to be implemented
        returns a boolean that determined if the Hook is successfull"""
        return False


class HookFileTask(HookTask):

    def execute(self, file_desc, filename, file_value, **kwargs):
        return False


class HookNewFileTask(HookFileTask):
    pass

class HookModifiedFileTask(HookFileTask):
    pass

class HookNewOrModifiedFileTask(HookNewFileTask, HookModifiedFileTask):
    pass

class HookDeletedFileTask(HookFileTask):
    pass
