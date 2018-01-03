import subprocess
import compiler
import pickle
import re
from datetime import datetime
from itertools import tee
from itertools import izip_longest as zip_longest

class Result:
    def __add__(self, msgs):
        print("linker.Result.__add__: self.msgs=" + self.msgs.toString() + " msgs= " + ",".join(msgs))
        self.msgs = msgs + self.msgs
        return self

    @classmethod
    def process(cls, msgstr):
        uni = msgstr.decode("utf-8")
        today = datetime.today()
        date_format = today.strftime("%Y-%m-%d")
        stripped = re.sub(r'/tmp/.*?/|-' + date_format + r'-\d+', '', uni)
        msg_starts = [match.start() for match in re.finditer(r'.*\.o: ', stripped)]
        if len(msg_starts) == 0: return []
        start, end = tee(msg_starts)
        next(end)
        return [stripped[i:j] for i, j in zip_longest(start, end)]

class Success(Result):
    def __init__(self, msgstr):
        self.msgs = self.process(msgstr)

class Failure(Result):
    def __init__(self, msgstr):
        self.msgs = self.process(msgstr)

def link(msgs, get_object_files, exename='a.out', compiler_name='g++', flags=''):
    results = [pickle.loads(msg) for msg in msgs]
    msgs = merge(results)
    if all(map(lambda result: isinstance(result, compiler.Success), results)):
        objects = get_object_files()
        cargs = [compiler_name, "-o", exename] + objects + flags.split(" ")
        try:
            return Success(subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)) + msgs
        except subprocess.CalledProcessError as e:
            return Failure(e.output) + msgs
    else:
        return Failure("") + msgs

def merge(results): #[String]
    # results: List[compiler.Success | compiler.Failure]
    return [msg for result in results for msg in result.msgs]
