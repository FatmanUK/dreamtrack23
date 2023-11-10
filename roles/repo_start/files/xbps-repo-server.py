#!/usr/bin/env python3
import sys
from subprocess import Popen, DEVNULL, STDOUT

port = sys.argv[1]
argv = ['/usr/bin/python3',
        '-m',
        'http.server',
        port]
cwd = '/var/tmp/xbps-static/var/cache/xbps'
pid = Popen(argv, 
            cwd=cwd, 
            start_new_session=True, 
            stdout=DEVNULL, 
            stderr=STDOUT).pid
print(pid)
