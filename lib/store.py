from os import path

from lib.common import DATADIR
from lib.files import readjson, writejson


def store(now, data):
    node_id = data.get('node_id')
    if node_id:
        loc = path.join(DATADIR, '{}.json'.format(node_id))

        node = readjson(loc)
        if not node:
            node = {'log': {}}
        clients = data.get('clients', {})
        traffic = data.get('traffic', {})

        node['hostname'] = data.get('hostname')

        node['log'][now] = {}
        node['log'][now]['load_avg'] = data.get('loadavg', 0.0)
        node['log'][now]['clients_total'] = clients.get('total', 0)
        node['log'][now]['clients_wifi'] = clients.get('wifi', 0)
        node['log'][now]['traffic_rx'] = traffic.get('rx', {}).get('bytes', 0)
        node['log'][now]['traffic_tx'] = traffic.get('tx', {}).get('bytes', 0)
        node['log'][now][
            'traffic_forward'
        ] = traffic.get('forward', {}).get('bytes', 0)
        node['log'][now][
            'traffic_mgmt_rx'
        ] = traffic.get('mgmt_tx', {}).get('bytes', 0)
        node['log'][now][
            'traffic_mgmt_tx'
        ] = traffic.get('mgmt_tx', {}).get('bytes', 0)

        return writejson(loc, node)
