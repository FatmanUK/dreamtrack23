#!/usr/bin/env python3

import modules.helpers as mh

def main():
    mh.playbook(
        wants_vault=True,
        env='dev',
        hosts='control',
        action='repo_stop',
    )

if __name__ == '__main__':
    main()

