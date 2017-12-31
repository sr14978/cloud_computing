import subprocess

def link(msgs, get_object_files, exename, compiler, flags):
    cargs = [compiler, "-o", exename] + objects + flags.split(" ")
    try:
        return subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return e.output