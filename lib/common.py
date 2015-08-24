from os import path, makedirs

BASEDIR = path.abspath(path.dirname(path.dirname(__file__)))
CONFIG = path.join(BASEDIR, 'config.json')

DATADIR = path.join(BASEDIR, 'data')

if not path.exists(DATADIR):
    makedirs(DATADIR)
