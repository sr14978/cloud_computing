import zipfile
import shutil

def unzip(path, session):
    destination = session + "-unpacked"
    shutil.rmtree(destination, True)
    with zipfile.ZipFile(path) as z:
        z.extractall(destination)
        return (destination, z.namelist())
