import zipfile
import shutil

def unzip(zip_path, destination):
    shutil.rmtree(destination, True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(destination)
        return z.namelist()
