import unzip
import compile
import link
import flags
import shutil

if __name__ == "__main__":
    zipname = "../ChimeraVirtualMachine.zip"
    session = "1"
    (dest, files) = unzip.unzip(zipname, session)
    sources = [dest + "/" + f for f in files if not f.endswith(".h")]
    flags = flags.Flags(zipname, "compiler=g++", "compiler-flags=-std=c++11 -O3", "link-flags=-pthread")
    compiler = compile.Compiler(flags)
    for source in sources:
        print(compiler(source))
    linker = link.Linker(session, flags)
    print(linker([source.split(".")[0] + ".o" for source in sources]))
    shutil.rmtree(dest, True)
