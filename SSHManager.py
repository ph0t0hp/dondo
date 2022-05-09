import os
import paramiko

class SSHManager(object):
    def __init__(self, file_path, username, password) -> None:
        self.password=password
        self.username=username
        self.keyfilename=os.path.expanduser(file_path)
        self.ssh=paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, host):
        self.ssh.connect(hostname=host,
                        username=self.username,
                        key_filename=self.keyfilename,
                        password=self.password)
    
    def execute_command(self, command_str):
        return self.ssh.exec_command(command_str)
