import subprocess

class Success:
    def __init__(self, filename, warnings):
        self.filename = filename
        self.warnings = warnings
        
class Error:
    def __init__(self, filename, msgs):
        self.filename = filename
        self.warnings = warnings
        
def Compiler(flags):
    compiler = flags.compiler
    flags = flags.fcompile
    def compile(filename):
        print("compiling " + filename)
        objectname = filename.split(".")[0] + ".o"
        cargs = [compiler, "-c", filename, "-o", objectname] + flags.split(" ")
        try:
            return subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            return e.output
    return compile
