from copy import deepcopy
from os import makedirs, path
from shlex import split as l_split
from subprocess import PIPE, Popen

BASEDIR = path.abspath(path.dirname(path.dirname(__file__)))
CONFIG = path.join(BASEDIR, 'config.json')

DATADIR = path.join(BASEDIR, 'data')

if not path.exists(DATADIR):
    makedirs(DATADIR)


def shell(cmd):
    try:
        res = Popen(l_split(cmd), stdout=PIPE, stderr=PIPE)
        out, err = res.communicate()
    except OSError as ex:
        print('ERROR: {}'.format(ex))
        return -1, None, None

    return res.returncode, out.decode(), err.decode()


def merge(di, ct):
    if not isinstance(ct, dict):
        return ct
    res = deepcopy(di)
    for key in ct.keys():
        res[key] = (
            merge(res[key], ct[key]) if
            res.get(key) and
            isinstance(res[key], dict) else
            deepcopy(ct[key])
        )
    return res
