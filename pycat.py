#!/usr/bin/env python3
import sys
import io
import argparse

#print("hola, mundo.")

NAME='cat'
DESCRIPTION='Concatenate FILE(s), or standard input, to standard output.'
EPILOG='With no FILE, or when FILE is -, read standard input.'

def getargs(argv):
    prsr = argparse.ArgumentParser(prog=NAME, description=DESCRIPTION, epilog=EPILOG)
    prsr.add_argument('file', metavar='FILE', nargs='*',
        type=argparse.FileType(mode='rb', bufsize=4096))

    ns = prsr.parse_args(argv)
    args = vars(ns)

    return args

def run(argv):
    args = getargs(argv)
    print(args)

if __name__ == "__main__":
    run(sys.argv[1:])

