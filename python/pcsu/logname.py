#!/usr/bin/env python3
import sys
import os
import argparse

def getargs(argv):
    NAME='logname'
    DESCRIPTION='''The logname utility will write the user's login name to
    standard output. The login name will be the string that would be returned
    by the getlogin() function defined in the System Interfaces volume of POSIX
    .1-2008. Under the conditions where the getlogin() function would fail, the
    logname utility will write a diagnostic message to standard error and exit
    with a non-zero exit status.'''

    prsr = argparse.ArgumentParser(prog=NAME, description=DESCRIPTION)
    prsr.add_argument('--version', action='version',
        version='%(prog)s (PCSU) 1.0')

    ns = prsr.parse_args(argv)
    args = vars(ns)

    return args

def run(argv):
    getargs(argv[1:])

    try:
        # Run main functions in here
        logname = os.getlogin()
    except Exception as e:
        sys.stderr.write('{}: {}\n'.format(e.__class__.__name__, e.args[0]))
        raise SystemExit(1)
    else:
        sys.stdout.write('{}\n'.format(logname))
        raise SystemExit(0)

def _test(argv):
    '''Run tests on module code'''
    run(argv)

if __name__ == "__main__":
    _test(sys.argv)

