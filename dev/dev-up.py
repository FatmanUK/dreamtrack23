#!/usr/bin/env python3

import os
import modules.helpers as mh

def main():
    script = os.path.basename(__file__)
    env = script[0:script.find('-')]
    #print(script)
    #print(env)
    mh.playbook(
        wants_vault=True,
        env=env,
        hosts='all',
        action=script[1 + len(env):-len('.py')],
    )

if __name__ == '__main__':
    main()

