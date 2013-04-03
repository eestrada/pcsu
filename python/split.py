#!/usr/bin/env python3
import sys
import io
import argparse
import copy

def getargs(argv):
    NAME='split'
    DESCRIPTION='''The split utility shall read an input file and write one or more output files. The default size of each output file shall be 1000 lines. The size of the output files can be modified by specification of the -b or -l options. Each output file shall be created with a unique suffix. The suffix shall consist of exactly suffix_length lowercase letters from the POSIX locale. The letters of the suffix shall be used as if they were a base-26 digit system, with the first suffix to be created consisting of all 'a' characters, the second with a 'b' replacing the last 'a' , and so on, until a name of all 'z' characters is created. By default, the names of the output files shall be 'x' , followed by a two-character suffix from the character set as described above, starting with "aa" , "ab" , "ac" , and so on, and continuing until the suffix "zz" , for a maximum of 676 files.

If the number of files required exceeds the maximum allowed by the suffix length provided, such that the last allowable file would be larger than the requested size, the split utility shall fail after creating the last file with a valid suffix; split shall not delete the files it created with valid suffixes. If the file limit is not exceeded, the last file created shall contain the remainder of the input file, and may be smaller than the requested size.'''
    EPILOG=''

    prsr = argparse.ArgumentParser(prog=NAME, description=DESCRIPTION,
        usage='''%(prog)s [-l line_count | -b n[k|m]] [-a suffix_length] [file[name]]''',
        epilog=EPILOG)
    prsr.add_argument('file', type=argparse.FileType(mode='rt'), default='-',
        nargs='?', help='''The pathname of the ordinary file to be split. If no
        input file is given or file is '-' , the standard input shall be
        used.''')
    prsr.add_argument('name', type=str, nargs='?', default='x', help='''The
        prefix to be used for each of the files resulting from the split
        operation. If no name argument is given, 'x' shall be used as the
        prefix of the output files. The combined length of the basename of
        prefix and suffix_length cannot exceed {NAME_MAX} bytes. See the
        OPTIONS section.''')
    prsr.add_argument('-a', metavar='suffix_length', default=2,
        action='store', type=int, help='''Use suffix_length letters to form the
        suffix portion of the filenames of the split file. If -a is not
        specified, the default suffix length shall be two. If the sum of the
        name operand and the suffix_length option-argument would create a
        filename exceeding {NAME_MAX} bytes, an error shall result; split shall
        exit with a diagnostic message and no files shall be created.''')
    prsr.add_argument('-b', metavar ='n', action='store', type=bytecount, 
        default=None, help='''Split a file into pieces n bytes in size.''')
    prsr.add_argument('-l', metavar ='line_count', action='store', type=int,
        default=1000, help='''Specify the number of lines in each resulting
        file piece. The line_count argument is an unsigned decimal integer.
        The default is 1000. If the input does not end with a <newline>, the
        partial line shall be included in the last output file.''')
    prsr.add_argument('--version', action='version', version='%(prog)s 1.0')

    ns = prsr.parse_args(argv)
    args = vars(ns)

    return args

def bytecount(s):
    if s[-1] in 'kK':
        return int(s[:-1]) * 1024 
    if s[-1] in 'mM':
        return int(s[:-1]) * 1024 * 1024
    else:
        return int(s)

def processargs(args):
    retargs = args

    if retargs['b'] != None:
        retargs['file'] = retargs['file'].buffer
        
    return retargs


class suffix:
    '''This is an iterator class'''
    def __init__(self, count):
        self.count = count
        self.max_len = pow(26, count)
        sys.stderr.write(str(self.max_len) + '\n')

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration()

def processtext(args):
    si = suffix(args['a'])
    raise NotImplementedError()
    
    l = True
    while l:
        for i in range(args['l']):
            l = args['file'].readline()

def processbinary(args):
    raise NotImplementedError()

def splitfile(args):
    if args['b'] != None: processbinary(args)
    else: processtext(args)

def run(argv):
    rawargs = getargs(argv)
    args = processargs(rawargs)
    try: splitfile(args)
    except NotImplementedError: sys.stderr.write(str(args) + '\n')
    sys.exit(0)

if __name__ == "__main__":
    run(sys.argv[1:])

