#!/usr/bin/env python3
import sys
import os
import argparse

def getargs(argv):
    NAME='mkfifo'
    DESCRIPTION='''\
    The mkfifo utility will create the FIFO special files specified by the operands, in the order specified.


    For each file operand, the mkfifo utility will perform actions equivalent to the mkfifo() function defined in the System Interfaces volume of POSIX.1-2008, called with the following arguments:

        The file operand is used as the path argument.

        The value of the bitwise-inclusive OR of S_IRUSR, S_IWUSR, S_IRGRP, S_IWGRP, S_IROTH, and S_IWOTH is used as the mode argument. (If the -m option is specified, the value of the mkfifo() mode argument is unspecified, but the FIFO will at no time have permissions less restrictive than the -m mode option-argument.)
'''

    prsr = argparse.ArgumentParser(prog=NAME, description=DESCRIPTION,
        add_help=False)

    prsr.add_argument('-m', metavar='mode', action='store',
        default=None, type=pmode)
        
    prsr.add_argument('file', nargs='+', action='store',
        type=pathc)

    prsr.add_argument('--version', action='version',
        version='%(prog)s (PCSU) 1.0')

    prsr.add_argument('--help', action='help',
        help='print this help message and exit')

    ns = prsr.parse_args(argv)
    args = vars(ns)

    return args

def makefifos(args):
    sys.stderr.write('{}\n'.format(args))
    raise NotImplementedError('makefifos function not implemented')

def _chmod_mode(l):
    return l
    raise NotImplementedError('_chmod_mode function not implemented')
    return int()

def pathc(s):
    #raise NotImplementedError('pathc function not implemented')
    return s + '_the_poop' 
    

def pmode(s):
    retval = None
    try:
        retval = int(s, 8)
    except ValueError as ve:
        try:
            retval = int(s)
        except ValueError as ve2:
            l = list(s)
            retval = _chmod_mode(l)
        else:
            raise ValueError('mode is not an octal integer value')

    return retval

def run(argv):
    args = getargs(argv[1:])

    try:
        # Run main functions in here
        makefifos(args)
    except Exception as e:
        sys.stderr.write('{}: {}\n'.format(e.__class__.__name__, e.args[0]))
        raise SystemExit(1)
    else:
        raise SystemExit(0)

def _test(argv):
    '''Run tests on module code'''
    run(argv)

if __name__ == "__main__":
    _test(sys.argv)

