#!/usr/bin/env python3
import sys
import io
import argparse

def getargs(argv):
    NAME='cat'
    DESCRIPTION='''The cat utility will read files in sequence and write their
        contents to the standard output in the same sequence.'''
    EPILOG=''

    prsr = argparse.ArgumentParser(prog=NAME, description=DESCRIPTION,
        epilog=EPILOG, usage='%(prog)s [-u] [file...]')
    prsr.add_argument('file', nargs='*',
        type=argparse.FileType(mode='rb'), help='''A pathname of an input
        file. If no file operands are specified, the standard input shall
        be used. If a file is '-' , the cat utility shall read from the
        standard input at that point in the sequence. The cat utility shall
        not close and reopen standard input when it is referenced in this way,
        but shall accept multiple occurrences of '-' as a file operand. The
        input files can be any file type (i.e. all file types are simply
        treated as byte sequences).''')
    prsr.add_argument('-u', dest='unbuffered', action='store_true',
        help='''Write bytes from the input file to the standard output
            without delay as each is read (i.e. reading and writing is
            unbuffered). This can be very inefficient and is not generally
            recommended.''')
    prsr.add_argument('--version', action='version', version='%(prog)s 1.0')

    ns = prsr.parse_args(argv)
    args = vars(ns)

    return args

def processargs(args):
    retargs = args
    files = retargs['file']

    for i in range(len(files)):
        if files[i].name == '<stdin>':
            files[i] = retargs['file'][i].buffer

    if retargs['unbuffered']: retargs['bufsize'] = 1
    else: retargs['bufsize'] = io.DEFAULT_BUFFER_SIZE 
        
    return retargs

def catfiles(args):
    l = args['file']
    for f in l:
        b = True
        while bool(b):
            b = f.read(args['bufsize'])
            sys.stdout.buffer.write(b)
        if f.name != '<stdin>': f.close()
        else: f.flush()
    sys.stdout.buffer.flush()

def run(argv):
    rawargs = getargs(argv)
    args = processargs(rawargs)
    catfiles(args)
    sys.exit(0)

if __name__ == "__main__":
    run(sys.argv[1:])

