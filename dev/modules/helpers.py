from os import environ
from os.path import dirname, realpath, exists
from sys import argv, stdin, stdout, stderr
import ansible_runner

ERR_NO_VAULT=1

def env_with_default(name, default):
    if name in environ:
        return environ[name]
    return default

def scriptdir():
    return dirname(realpath(argv[0]))

def env_hosts(env, default):
    return env_with_default(f'{env.upper()}_HOSTS', default)

def env_playbook(scriptdir, action):
    return env_with_default('PLAYBOOK', realpath(f'{scriptdir}/../books/{action}.yml'))

def env_vault(scriptdir, env):
    return env_with_default('VAULT', realpath(f'{scriptdir}/../vaults/{env}-vault.yml'))

def env_vault_secret(scriptdir, env):
    return env_with_default('VAULT_SECRET', realpath(f'{scriptdir}/../vaults/{env}-password.txt'))

def env_inventory(scriptdir, env):
    return env_with_default('ANSIBLE_INVENTORY', realpath(f'{scriptdir}/../inventories/{env}'))

def playbook(action, env, wants_vault=True, hosts='all'):
    print('Env: ' + env)
    print('Action: ' + action)
    if action == 'prep':
        wants_vault = False
    wants_root = False
    if action == 'create':
        wants_root = True
    #if action == 'inst':
    #    wants_root = True
    DIR_SCRIPT=scriptdir()
    HOSTS=env_hosts(env, hosts)
    PLAYBOOK=env_playbook(DIR_SCRIPT, action)
    ANSIBLE_INVENTORY=env_inventory(DIR_SCRIPT, env)
    if wants_vault:
        VAULT=env_vault(DIR_SCRIPT, env)
        if not exists(VAULT):
            print(f'Vault file {VAULT} missing!')
            exit(ERR_NO_VAULT)
        else:
            VAULT_SECRET=env_vault_secret(DIR_SCRIPT, env)
    args=[]
    args.append(f'--limit={HOSTS}')
    args.append(f'--inventory={ANSIBLE_INVENTORY}')
    if wants_root:
        args.append(f'--ask-become-pass')
    if wants_vault:
        args.append(f'-e@{VAULT}')
        args.append(f'--vault-password-file={VAULT_SECRET}')
    args += argv[1:]
    args.append(f'{PLAYBOOK}')
    print(f'Running with args: {args}')
    ansible_runner.run_command('/usr/bin/ansible-playbook', cmdline_args=args, input_fd=stdin, output_fd=stdout, error_fd=stderr)
