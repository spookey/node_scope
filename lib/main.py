from lib.common import timestamp
from lib.config import load
from lib.retrieve import query
from lib.store import store


def pull():
    conf = load()
    mesh = query(conf['connection'])
    now = timestamp()

    for mac, data in mesh.items():
        if any([
            n.lower() in [
                c.lower() for c in conf['targets']
            ] for n in [
                mac,
                data.get('hostname'),
                data.get('node_id')
            ]
        ]):
            store(now, data)
