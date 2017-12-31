import subprocess

class Success:
    def __init__(self, filename, warnings):
        self.filename = filename
        self.warnings = warnings
        
class Error:
    def __init__(self, filename, msgs):
        self.filename = filename
        self.warnings = warnings
        
def compile(source_path, object_path, compiler='g++', flags=''):
    print("compiling " + source_path)
    cargs = [compiler, "-c", source_path, "-o", object_path] + flags.split(" ")
    try:
        return subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return e.output
