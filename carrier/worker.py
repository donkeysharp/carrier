from carrier.utils import AnsiblePlaybook


class WorkerController:
    def provision_workers(self):
        playbook = AnsiblePlaybook()
        playbook.set_inventory('inventory')
        playbook.set_playbook('workers-playbook.yml')
        playbook.set_private_key('~/.carrier/carrier')
        playbook.add_tag('always')
        playbook.add_tag('setup')
        playbook.add_extra_vars('@~/.carrier/doloris.yml')
        returncode = playbook.run()
        if returncode != 0:
            raise Exception('Provisioning failed with exit code %d' % returncode)

    def start_attack(self):
        playbook = AnsiblePlaybook()
        playbook.set_inventory('inventory')
        playbook.set_playbook('workers-playbook.yml')
        playbook.set_private_key('~/.carrier/carrier')
        playbook.add_tag('always')
        playbook.add_tag('execution')
        playbook.add_extra_vars('@~/.carrier/doloris.yml')
        playbook.add_extra_vars('action=carrier_start')
        returncode = playbook.run()
        if returncode != 0:
            raise Exception('Starting attack failed with exit code %d' % returncode)

    def stop_attack(self):
        playbook = AnsiblePlaybook()
        playbook.set_inventory('inventory')
        playbook.set_playbook('workers-playbook.yml')
        playbook.set_private_key('~/.carrier/carrier')
        playbook.add_tag('always')
        playbook.add_tag('execution')
        playbook.add_extra_vars('@~/.carrier/doloris.yml')
        playbook.add_extra_vars('action=carrier_stop')
        returncode = playbook.run()
        if returncode != 0:
            raise Exception('Stopping attack failed with exit code %d' % returncode)

    def delete_workers(self):
        playbook = AnsiblePlaybook()
        playbook.set_inventory('inventory')
        playbook.set_playbook('workers-playbook.yml')
        playbook.set_private_key('~/.carrier/carrier')
        playbook.add_tag('always')
        playbook.add_extra_vars('@~/.carrier/doloris.yml')
        playbook.add_extra_vars('param_server_state=deleted')
        returncode = playbook.run()
        if returncode != 0:
            raise Exception('Deleting workers failed with exit code %d' % returncode)
