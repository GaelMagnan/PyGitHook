"""
Bash is a placeholder for the execute_command function;

execute_command is a wrapper around subprocess.check_output.

AUTHOR:
    Gael Magnan de bornier
"""

from subprocess import check_output, CalledProcessError, STDOUT

def execute_command(command):
    """Execute a bash command,
    returns a return code 0 for success the error code otherwise
    and the output as a array of string (1 element = 1 line)"""
    try:
        ret_code = 0
        try:
            output = check_output(command.split(), stderr=STDOUT)
        except CalledProcessError, error:
            output = error.output
            ret_code = error.returncode
        res = output.split('\n')
        return ret_code, res
    except StandardError, error:
        print("The command: %s failed.\n"
              "Please transmit the following message to your administrator:" %
              command)
        print(error)
    return 1, []
