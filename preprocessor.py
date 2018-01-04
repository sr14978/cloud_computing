import subprocess
import pickle
from compiler import Success
from compiler import Error


def preprocess(source_path, out_path, compiler_name='g++', flags=''):
    print("preprocessing " + source_path + " to " + out_path + " using " + compiler_name)
    cargs = [compiler_name, "-E", source_path, "-o", out_path] + flags.split(" ")
    try:
        return True, pickle.dumps(Success(subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)))
    except subprocess.CalledProcessError as e:
        print('preprocessor error output', e.output)
        return False, pickle.dumps(Error(e.output))
