from fnmatch import fnmatch
from os import listdir, path
from string import ascii_lowercase, digits

from pygal import DateTimeLine, Treemap

from lib.common import DATADIR, ts_dt
from lib.files import readjson


class PlotNode:
    def __init__(self, data):
        self.hostname = data['hostname']
        self.name = ''.join(
            c for c in self.hostname.lower() if
            c in (ascii_lowercase + digits + '_' + '-')
        )
        self.data = {}

        for ts in sorted(data['log']):
            for field in sorted(data['log'][ts]):
                self.data[field] = self.data.get(field, [])
                self.data[field].append((
                    ts_dt(float(ts)),
                    data['log'][ts][field]
                ))

    def _plot(self, x_title):
        plot = DateTimeLine(
            legend_at_bottom=True,
            title=self.hostname,
            x_label_rotation=35,
            x_value_formatter=lambda dt: dt.strftime('%Y.%m.%d %H:%M:%S')
        )
        plot.x_title = x_title
        return plot

    def clients(self):
        plot = self._plot('Clients')
        plot.add('WiFi', self.data['clients_wifi'])
        plot.add('Total', self.data['clients_total'])
        return plot

    def traffic(self):
        plot = self._plot('Traffic')
        plot.add('RX', self.data['traffic_rx'])
        plot.add('TX', self.data['traffic_tx'])
        return plot

    def traffic_full(self):
        plot = self.traffic()
        plot.x_title = 'Traffic (full)'
        plot.add('Forward', self.data['traffic_forward'])
        plot.add('Management RX', self.data['traffic_mgmt_rx'])
        plot.add('Management TX', self.data['traffic_mgmt_tx'])
        return plot

    def system(self):
        plot = self._plot('System')
        plot.add('Load', self.data['load_avg'])
        return plot


def _load():
    for jf in listdir(DATADIR):
        if fnmatch(jf, '*.json'):
            data = readjson(path.join(DATADIR, jf))
            yield PlotNode(data)


def plot():
    def save(name, graph, field):
        graph.render_to_file(
            path.join(DATADIR, '{}_{}.svg'.format(name, field))
        )

    def _cmp(comp, node, field):
        comp.add(node.hostname, [d[-1] for d in node.data[field]])
        return comp

    compare_clients = Treemap()
    compare_traffic_rx = Treemap()
    compare_traffic_tx = Treemap()

    for node in _load():
        save(node.name, node.clients(), 'clients')
        save(node.name, node.system(), 'system')
        save(node.name, node.traffic(), 'traffic')
        save(node.name, node.traffic_full(), 'traffic_full')

        save('', _cmp(compare_clients, node, 'clients_total'), 'clients')
        save('', _cmp(compare_traffic_rx, node, 'traffic_rx'), 'traffic_rx')
        save('', _cmp(compare_traffic_tx, node, 'traffic_tx'), 'traffic_tx')
