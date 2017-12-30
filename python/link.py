import subprocess

def Linker(session, flags):
    exename = flags.exename
    compiler = flags.compiler
    flags = flags.flink
    def link(objects):
        cargs = [compiler, "-o", session + "-" + exename] + objects + flags.split(" ")
        try:
            return subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            return e.output
    return link
