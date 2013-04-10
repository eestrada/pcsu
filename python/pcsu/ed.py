#!/usr/bin/env python3
import sys

def run(argv):
    try:
        raise NotImplementedError('ed/ex/vi not yet implemented', 1)
    except Exception as e:
        sys.stderr.write('{}: {}\n'.format(e.__class__.__name__, e.args[0]))
        return e.args[1]

if __name__ == "__main__":
    retval = run(sys.argv)
    sys.exit(retval)

