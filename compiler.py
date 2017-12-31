import subprocess

class Success:
    def __init__(self, filename, warnings):
        self.filename = filename
        self.warnings = warnings
        
class Error:
    def __init__(self, filename, msgs):
        self.filename = filename
        self.warnings = warnings
        
def compile(filename, compiler='g++', flags=''):
    print("compiling " + filename)
    objectname = filename.rsplit(".", 1)[0] + ".o"
    cargs = [compiler, "-c", filename, "-o", objectname] + flags.split(" ")
    try:
        return objectname, subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return objectname, e.output
