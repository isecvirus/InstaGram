import subprocess

clear_commands = ["clear", "cls"]
def ClearScreen():
    try:
        [
            subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
            for cmd in
            clear_commands
        ]
    except Exception:
        pass