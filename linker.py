import subprocess

def link(session, exename, compiler, flags):
    cargs = [compiler, "-o", session + "-" + exename] + objects + flags.split(" ")
    try:
        return subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return e.output