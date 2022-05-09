class SSHCommandsList(object):
    def __init__(self, commands_list_str):
        self.commands=commands_list_str.split(',')
        
    def get_commands_count(self):
        return len(self.commands)

    def get_command(self, index):
        if index < len(self.commands):
            return self.commands[index]
        else:
            return None