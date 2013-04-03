#!/usr/bin/env python3
import sys
import io
import argparse

_NAME='cat'
_DESCRIPTION='Concatenate FILE(s), or standard input, to standard output.'
_EPILOG='With no FILE, or when FILE is -, read standard input.'

def getargs(argv):
    prsr = argparse.ArgumentParser(prog=_NAME, description=_DESCRIPTION,
        epilog=_EPILOG, usage='%(prog)s [-u] [file...]')
    prsr.add_argument('file', nargs='*',
        type=argparse.FileType(mode='rb'), help='''File(s) to
        concatenate to standard output.''')
    prsr.add_argument('-u', dest='unbuffered', action='store_true',
        help='''Write bytes from the input file to the standard output
            without delay as each is read. (i.e. Reading and writing is unbuffered)''')
    prsr.add_argument('--version', action='version', version='%(prog)s 1.0')

    ns = prsr.parse_args(argv)
    args = vars(ns)

    return args

def run(argv):
    args = getargs(argv)
    sys.stderr.write(str(args))
    sys.stderr.write('\n')
    l = args['file']
    for f in l:
        while f.readable():
            b = f.read(4096)
            sys.stdout.buffer.write(b)
        f.close()
    

if __name__ == "__main__":
    run(sys.argv[1:])

