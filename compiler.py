import subprocess
import pickle

def process(msgstr):
    return [msgstr]

class Success:
    def __init__(self, warnings):
        self.msgs = process(warnings)

class Error:
    def __init__(self, msgs):
        self.msgs = process(msgs)

def compile(source_path, object_path, compiler='g++', flags=''):
    print("compiling " + source_path + " to " + object_path + " using " + compiler)
    cargs = [compiler, "-c", source_path, "-o", object_path] + flags.split(" ")
    # if this succeeds we wrap the result up in a Success object
    try:
        return pickle.dumps(Success(subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)))
    # otherwise we return an Error object
    except subprocess.CalledProcessError as e:
        return pickle.dumps(Error(e.output))
