import subprocess
import compiler
import pickles

class Result:
    def __add__(self, msgs):
        self.msgs += msgs
        return self

    @classmethod
    def process(cls, msgstr):
        return [msgstr]

class Success(Result):
    def __init__(self, msgstr):
        self.msgs = self.process(msgstr)

class Failure(Result):
    def __init__(self, msgstr):
        self.msgs = self.process(msgstr)

def link(msgs, get_object_files, exename, compiler, flags):
    results = [pickle.loads(msg) for msg in msgs]
    objects = get_object_files()
    msgs = merge(results)
    if all(map(lambda result: isinstance(result, compiler.Success), results)):
        cargs = [compiler, "-o", exename] + objects + flags.split(" ")
        try:
            return Success(subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)) + msgs
        except subprocess.CalledProcessError as e:
            return Failure(e.output) + msgs
    else:
        return None

def merge(results): #[String]
    # results: List[compiler.Success | compiler.Failure]
    return [msg for result in results for msg in result.msgs]
