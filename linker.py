import subprocess

def link(msgs, get_object_files, exename, compiler, flags):
    print("linking to " + exename + " using " + compiler)
    objects = get_object_files()
    print("linking " + str(objects) + " to " + exename + " using " + compiler)
    
    cargs = [compiler, "-o", exename] + objects + flags.split(" ")
    try:
        output = subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output
    
    print("linked " + str(objects) + " to " + exename + " using " + compiler + ". Output: " + output)
    return output