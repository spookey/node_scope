from lib.config import load
from lib.common import DATADIR, shell
from os import listdir, path
from fnmatch import fnmatch


def _files():
    res = []
    for sf in listdir(DATADIR):
        if fnmatch(sf, '*.svg'):
            res.append(path.join(DATADIR, sf))
    return res


def push():
    conf = load()

    cmd = 'scp {} {}:{}'.format(
        ' '.join(_files()),
        conf['upload']['ssh'],
        conf['upload']['folder']
    )

    code, out, err = shell(cmd)
    if code == 0:
        print('ok:', out, err)
    else:
        print('ERROR:', err)
