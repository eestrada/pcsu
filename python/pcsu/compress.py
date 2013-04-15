#!/usr/bin/env python3
import sys
import os

def run(argv):
    prog = os.path.basename(argv[0])
    msg = 'utility "{}" not yet implemented'.format(prog)

    try:
        # Run main functions in here
        raise NotImplementedError(msg, 1)
    except Exception as e:
        sys.stderr.write('{}: {}\n'.format(e.__class__.__name__, e.args[0]))
        raise SystemExit(e.args[1])

def _test(argv):
    '''Run tests on module code'''
    run(argv)

if __name__ == "__main__":
    _test(sys.argv)

