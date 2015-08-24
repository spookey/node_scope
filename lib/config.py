
from lib.files import readjson, writejson
from lib.common import CONFIG

def __ask_prompt(descr, default):
    print('{}:\t[ {} ]'.format(descr, default))
    return input('>> ')


def _ask_bool(descr, default):
    res = __ask_prompt(
        '{} (y/n)'.format(descr),
        'Y' if default else 'N'
    )
    return default if res == '' else (
        True if res.lower() == 'y' else False
    )

def _ask_list(descr, default):
    res = __ask_prompt(
        '{} (comma separated list)'.format(descr),
        ','.join([str(d) for d in default])
    )
    return default if res == '' else res.split(',')


def _ask_str(descr, default):
    res = __ask_prompt(descr, default)
    return default if res == '' else res


def gen_connection():
    conn = {}
    if _ask_bool('Use SSH', False):
        conn['ssh'] = _ask_str('SSH options', '-i ~/.ssh/id_rsa root@localhost')
    conn['channels'] = _ask_list('Alfred Channels', [158, 159])
    conn['socket'] = _ask_str('Alfred Socket Path', '/var/run/alfred.sock')
    conn['sudo'] = _ask_bool('Run with sudo', False)

    return conn

def gen_targets():
    return _ask_list('Exact Hostnames or MACs of nodes to watch', ['node'])


def load():
    conf = readjson(CONFIG)
    if not conf:
        conf = {}
    if not conf.get('connection'):
        conf['connection'] = gen_connection()
    if not conf.get('targets'):
        conf['targets'] = gen_targets()

    writejson(CONFIG, conf)
    return conf

