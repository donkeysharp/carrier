import csv
import json
import math
import os
import yaml

from carrier.ssh import generate_ssh_keys
from os.path import expanduser


CARRIER_SETTINGS_DIR = '.carrier'

def split_array(array=[], sub_arrays=1):
    total_items = len(array)
    idx = 0
    groups = []
    while idx < sub_arrays:
        size = int(math.ceil(total_items / (sub_arrays * 1.0)))
        groups.append(array[size * idx: size * (idx + 1)])
        idx += 1
    return groups


class ConfigurationManager:
    def __init__(self, api_key):
        self.api_key = api_key
        home = expanduser('~')
        self.directory = '%s/%s' % (home, CARRIER_SETTINGS_DIR)
        self.private_key_file = '%s/carrier' % self.directory
        self.public_key_file = '%s/carrier.pub' % self.directory

    def create_config_file(self, nodes, containers_per_node):
        directory = self.directory

        with open('%s/%s' % (self.directory, 'targets')) as hosts_file:
            reader = csv.reader(hosts_file)
            records = [{'host': row[0], 'scheme': row[1]} for row in reader]

        result = {}
        hosts_per_node = split_array(records, nodes)

        node_idx = 1
        container_idx = 1
        for host_list in hosts_per_node:
            hosts_per_container = split_array(host_list, containers_per_node)
            node_id = 'carrier-worker-node-%d' % (node_idx)
            result[node_id] = {'containers': []}

            for hosts in hosts_per_container:
                container = {
                    'name': 'container%d' % (container_idx),
                    'targets': []
                }
                container_idx += 1
                container['targets'] = [host for host in hosts]
                result[node_id]['containers'].append(container)
            node_idx += 1

        public_key = self.get_ssh_keys()[1]

        result = {
            'doloris_settings': result,
            'public_key': public_key,
            'do_api_key': self.api_key,
            'number_of_workers': nodes,
        }
        config_file = open('%s/doloris.yml' % (directory), 'w')
        config_file.write(yaml.dump(result))
        config_file.close()

    def get_ssh_keys(self):
        if not (os.path.exists(self.private_key_file) and os.path.exists(self.public_key_file)):
            self.__create_ssh_keys()

        f = open(self.public_key_file, 'r')
        public_key = f.read()
        f.close()

        f = open(self.private_key_file, 'r')
        private_key = f.read()
        f.close()
        return (private_key, public_key)

    def __create_ssh_keys(self):
        private_key, public_key = generate_ssh_keys()
        f = open(self.private_key_file, 'w')
        f.write(private_key)
        f.close()
        os.chmod(self.private_key_file, 0o600)

        f = open(self.public_key_file, 'w')
        f.write(public_key)
        f.close()

