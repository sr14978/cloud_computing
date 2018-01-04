import subprocess

def preprocess(source_path, out_path, compiler_name='g++', flags=''):
    print("preprocessing " + source_path + " to " + out_path + " using " + compiler_name)
    cargs = [compiler_name, "-E", source_path, "-o", out_path] + flags.split(" ")
    try:
        subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)
        return True, None
    except subprocess.CalledProcessError as e:
        return False, e.output
