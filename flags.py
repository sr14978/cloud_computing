class Flags:
    def __init__(self, zipname, *args):
        m = dict()
        for arg in args:
            if "=" not in arg: continue
            key, value = arg.split("=", 1)
            m[key] = value
        self.exename = m["exename"] if "exename" in m else zipname.split(".")[0]
        self.compiler = m["compiler"] if "compiler" in m else "g++"
        self.fcompile = m["compiler-flags"] if "compiler-flags" in m else ""
        self.flink = m["link-flags"] if "link-flags" in m else ""
