#!/usr/bin/env python
"""Carrier

Usage:
  carrier.py provision --nodes=<n> --containers-per-node=<c> --api-key=<key>
  carrier.py delete
  carrier.py start
  carrier.py stop

Options:
    --nodes=<n>                 Number of nodes to create
    --containers-per-node=<c>   Number of containers-per-node
    --api-key=<key>             DigitalOcean API key
"""

from docopt import docopt
from os.path import expanduser
from carrier.config import ConfigurationManager
from carrier.worker import WorkerController


def provision_droplets(args):
    nodes = int(args['--nodes'])
    containers_per_node = int(args['--containers-per-node'])
    api_key = args['--api-key']

    conf = ConfigurationManager(api_key)
    conf.create_config_file(nodes, containers_per_node)

    controller = WorkerController()
    controller.provision_workers()


def start_attack():
    controller = WorkerController()
    controller.start_attack()


def stop_attack():
    controller = WorkerController()
    controller.stop_attack()


def delete_droplets():
    controller = WorkerController()
    controller.delete_workers()


def main(args):
    if args['provision']:
        provision_droplets(args)
    elif args['start']:
        start_attack()
    elif args['stop']:
        stop_attack()
    elif args['delete']:
        delete_droplets()


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
