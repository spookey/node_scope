from json import loads

from lib.common import RAW_ALFRED, merge, shell
from lib.files import writejson


def _alfred(conn):
    def _ssh(cmd):
        if conn.get('ssh'):
            return 'ssh {} "{}"'.format(conn['ssh'], cmd)
        return cmd

    def _sudo(cmd):
        if conn.get('sudo'):
            return 'sudo {}'.format(cmd)
        return cmd

    res = []
    for channel in conn['channels']:
        alfred = 'alfred-json -s {} -r {} -f json -z'.format(
            conn['socket'], channel
        )
        res.append(_ssh(_sudo(alfred)))
    return res


def query(conn):
    def _ask(curr, cmd):
        code, out, err = shell(cmd)
        if code == 0 and out is not None:
            try:
                data = loads(out)
                if data is not None:
                    curr = merge(curr, data)
                    return curr
            except ValueError as ex:
                print('ERROR: {}'.format(ex))

    res = {}
    for cmdline in _alfred(conn):
        res = _ask(res, cmdline)
    if conn['keep']:
        writejson(RAW_ALFRED, res)
    return res
