import subprocess

def link(objects, exename, compiler, flags):
    cargs = [compiler, "-o", exename] + objects + flags.split(" ")
    try:
        return subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return e.output