import digitalocean
import random
import time

import SSHManager

class DOManager(object):
    def __init__(self, config) -> None:
        self.config=config
        self.manager=digitalocean.Manager(token=self.config.get_do_token())
        self.channels = []

    def reboot_droplets(self):
        for droplet in self.manager.get_all_droplets():
            droplet.reboot()

    def shutdown_droplets(self):
        for droplet in self.manager.get_all_droplets():
            droplet.shutdown()

    def enable_droplets(self):
        for droplet in self.manager.get_all_droplets():
            droplet.power_on()

    def init_droplets(self):
        self.deinit_droplets()

        needed_droplets=int(self.config.get_do_droplets_count())
        for i in range(0, needed_droplets):
            name=self.config.get_do_droplets_name_template() +str(i + 1)
            if  self.create_droplet(name,
                                    self.get_random_region(),
                                    self.config.get_do_droplet_os(),
                                    self.config.get_do_droplet_hw()) == False:
                return False

        return True

    def is_need_init_droplets(self):
        return self.get_droplets_count() < len(self.manager.get_all_droplets())

    def deinit_droplets(self):
        for droplet in self.manager.get_all_droplets():
            droplet.destroy()

    def wait(self):
        while any(x is not None for x in self.channels):
            for i in range(len(self.channels)):
                channel = self.channels[i]
                if channel is not None:
                    exited = channel.exit_status_ready()
                    while channel.recv_ready():
                        s = channel.recv(1048576).decode('utf8')
                        print(f"#{i} stdout: {s}")
                    while channel.recv_stderr_ready():
                        s = channel.recv_stderr(1048576).decode('utf8')
                        print(f"#{i} stderr: {s}")
                    if exited:
                        self.channels[i] = None
            time.sleep(0.1) 

    def create_droplet(self, name, rg, os, hw):
        try:
            keys=self.manager.get_all_sshkeys()
            droplet=digitalocean.Droplet(token=self.config.get_do_token(),
                                        name=name,
                                        region=rg,
                                        image=os,
                                        size_slug=hw,
                                        ssh_keys=keys,
                                        backups=False)
            droplet.create()

        except digitalocean.DataReadErro as e:
            print(e)
            return False

        while True:
            actions = droplet.get_actions()
            for action in actions:
                action.load()
                if action.status == 'completed':
                    print('Create droplet completed...')
                    return True

    def destroy_droplet(self, index):
        self.manager.get_all_droplets()[index].destroy()

    def get_droplets_count(self):
        return int(self.config.get_do_droplets_count())

    def get_droplet_ip(self, index):
        if index < self.get_droplets_count():
            return self.manager.get_all_droplets()[index].ip_address
        else:
            return None

    def get_regions(self):
        return self.manager.get_all_regions()

    def get_random_region(self):
        while True:
            region=random.choice(self.get_regions())
            if region.available:
                return region.slug

    def execute_commands(self, index, commands, wait):
        ssh_manager=SSHManager.SSHManager(self.config.get_ssh_file_path(),
                                          self.config.get_ssh_user_name(),
                                          self.config.get_ssh_password())
        ssh_manager.connect(self.get_droplet_ip(index))
        for i in range(0, commands.get_commands_count()):
            command=str(commands.get_command(i))
            print('Execute command: ', command)
            stdin, stdout,stderr=ssh_manager.execute_command(command_str=command)
            self.channels.append(stdin.channel)
            self.channels.append(stdout.channel)
            self.channels.append(stderr.channel)
            if wait:
                self.wait()
                stdout.channel.recv_exit_status()
            