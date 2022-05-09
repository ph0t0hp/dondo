import configparser

class ConfigsManager(object):
    def __init__(self, file_path) -> None:
        self.parser=configparser.ConfigParser()
        self.parser.read(file_path)

    def get_do_token(self):
        return self.parser['do']['token']

    def get_do_droplets_count(self):
        return self.parser['do']['droplets_count']

    def get_do_droplets_name_template(self):
        return self.parser['do']['template']

    def get_do_droplet_os(self):
        return self.parser['do']['os']

    def get_do_droplet_hw(self):
        return self.parser['do']['hw']

    def get_ssh_file_path(self):
        return self.parser['ssh']['file_path']

    def get_ssh_user_name(self):
        return self.parser['ssh']['user_name']

    def get_ssh_password(self):
        return self.parser['ssh']['password']

    def get_ssh_commands(self):
        return self.parser['ssh']['commands']