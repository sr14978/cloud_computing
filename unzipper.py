import zipfile
import shutil

def unzip(zip_path, destination):
    print("unzipping " + zip_path + " to " + destination)
    shutil.rmtree(destination, True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(destination)
        output =  z.namelist()
        
    print("unzipped " + zip_path + " to " + destination + " : " + str(output))
    return output