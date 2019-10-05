import os
import subprocess


class AnsiblePlaybook:
    def __init__(self):
        self.playbook = None
        self.inventory = None
        self.private_key = None
        self.tags = []
        self.extra_vars = []

    def set_playbook(self, playbook):
        self.playbook = playbook

    def set_inventory(self, inventory):
        self.inventory = inventory

    def set_private_key(self, private_key):
        self.private_key = private_key

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_extra_vars(self, extra_var):
        self.extra_vars.append(extra_var)

    def __get_tags(self):
        tags = self.tags[0]
        for tag in self.tags[1:]:
            tags += ',' + tag
        return tags

    def __get_extra_vars(self):
        extra_vars = '--extra-vars ' + self.extra_vars[0]
        for extra_var in self.extra_vars[1:]:
            extra_vars += ' --extra-vars ' + extra_var
        return extra_vars

    def __create_command(self):
        if not self.playbook or not self.inventory:
            raise Error('Playbook and inventory variables are mandatory')

        cmd = 'ansible-playbook'
        cmd += ' -i ' + self.inventory
        cmd += ' ' + self.playbook
        if self.private_key:
            cmd += ' --private-key ' + self.private_key
        if len(self.tags) > 0:
            cmd += ' --tags ' + self.__get_tags()
        if len(self.extra_vars) > 0:
            cmd += ' ' + self.__get_extra_vars()
        return cmd

    def run(self):
        cmd = self.__create_command()
        process = subprocess.Popen(cmd.split(' '), cwd=os.getcwd())
        process.communicate()
        return process.returncode
