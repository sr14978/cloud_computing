import subprocess

def preprocess(source_path, out_path, compiler_name='g++', flags=''):
    print("preprocessing " + source_path + " to " + out_path + " using " + compiler_name)
    cargs = [compiler_name, "-E", source_path, "-o", out_path] + flags.split(" ")
    try:
        subprocess.call([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(e.output)
