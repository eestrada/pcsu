#!/usr/bin/env python3
import sys
import os

def run(argv):
    try:
        prog = os.path.basename(argv[0])
        msg = 'utility "{}" not yet implemented'.format(prog)
        raise NotImplementedError(msg, 1)
    except Exception as e:
        sys.stderr.write('{}: {}\n'.format(e.__class__.__name__, e.args[0]))
        return e.args[1]

if __name__ == "__main__":
    retval = run(sys.argv)
    sys.exit(retval)

