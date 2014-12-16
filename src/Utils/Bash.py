"""
Bash is a placeholder for the execute_command function;

execute_command is a wrapper around subprocess.check_output.

AUTHOR:
    Gael Magnan de bornier
"""

from subprocess import check_output, CalledProcessError, STDOUT, PIPE, Popen

def execute_command(command, shell=False):
    """Execute a bash command,
    returns a return code 0 for success the error code otherwise
    and the output as a array of string (1 element = 1 line)"""
    try:
        ret_code = 0
        try:
            output = check_output(command.split(), stderr=STDOUT, shell=shell)
        except CalledProcessError, error:
            output = error.output
            ret_code = error.returncode
        return ret_code, output.split('\n')
    except StandardError, error:
        print("The command: %s failed.\n"
              "Please transmit the following message to your administrator:" %
              command)
        print(error)
    return 1, []


def execute_piped_command(command1, command2):

    try:
        p1 = Popen(command1.split(), stdout=PIPE)
    except CalledProcessError, error:
        return error.returncode, error.output.split('\n')
    else:
        try:
            p2 = Popen(command2.split(), stdin=p1.stdout, stderr=STDOUT )
        except CalledProcessError, error:
            return error.returncode, error.output.split('\n')
        else:
            try:
                p1.stdout.close()
                output = p2.communicate()[0]
                return 0, output.split('\n')
            except StandardError, error:
                print("The commands: {0} failed.\n".format((command1, command2)))
                print("Please transmit the following message to your administrator:")
                print(error)
    return 1, []
