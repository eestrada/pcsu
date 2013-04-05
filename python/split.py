#!/usr/bin/env python3
import sys
import io
import argparse
import copy
import string
import collections

class SuffixError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class suffix(collections.Sequence):
    '''This is an sequence class for alphabetic suffixes

This class is used to generate alphabetic suffixes for the split command when
creating output files.'''
    def __init__(self, count = 2):
        intc = int(count)
        if intc < 1:
            raise ValueError( "Value provided less than 1: " + str(count) )
        self._iter_count = 0
        self._count = intc
        self._max_len = pow(26, intc)

    def __len__(self):
        return self._max_len

    @staticmethod
    def _idiv(i, j):
        k = int(i) // int(j)
        l = int(i) % int(j)
        return k,l

    def __iter__(self):
        self._iter_count = 0
        return self

    def _next_helper(self, index):
        if index < self._max_len: # Only iterate if we haven't maxed out
            q = index
            r = int()
            l = list()
            for i in range(self._count): # make string as long as the count
                q,r = suffix._idiv( q, 26 )
                l.append( string.ascii_lowercase[r] )

            l.reverse()
            return ''.join(l)
        else:
            raise IndexError('suffix object index out of range')

    def __getitem__(self, index):
        return self._next_helper(index)

    def __next__(self):
        try:
            retval = self._next_helper(self._iter_count)
            self._iter_count += 1
            return retval
        except IndexError:
            raise StopIteration()

def getargs(argv):
    NAME='split'
    DESCRIPTION='''The split utility shall read an input file and write one or more output files. The default size of each output file shall be 1000 lines. The size of the output files can be modified by specification of the -b or -l options. Each output file shall be created with a unique suffix. The suffix shall consist of exactly suffix_length lowercase letters from the POSIX locale. The letters of the suffix shall be used as if they were a base-26 digit system, with the first suffix to be created consisting of all 'a' characters, the second with a 'b' replacing the last 'a' , and so on, until a name of all 'z' characters is created. By default, the names of the output files shall be 'x' , followed by a two-character suffix from the character set as described above, starting with "aa" , "ab" , "ac" , and so on, and continuing until the suffix "zz" , for a maximum of 676 files.

If the number of files required exceeds the maximum allowed by the suffix length provided, such that the last allowable file would be larger than the requested size, the split utility shall fail after creating the last file with a valid suffix; split shall not delete the files it created with valid suffixes. If the file limit is not exceeded, the last file created shall contain the remainder of the input file, and may be smaller than the requested size.'''
    EPILOG=''

    prsr = argparse.ArgumentParser(prog=NAME, description=DESCRIPTION,
        usage='''%(prog)s [-l line_count | -b n[k|m]] [-a suffix_length] [file[name]]''',
        epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    prsr.add_argument('-a', metavar='suffix_length', default=suffix(2),
        action='store', type=suffix, help='''Use suffix_length letters to form the
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

def processtext(args):
    for sfx in args['a']:
        with io.open(args['name'] + sfx, mode='wt') as of:
            i = 0
            l = True
            while i < args['l'] and l:
                l = args['file'].readline()
                if not l:
                    args['file'].close()
                    return
                of.write(l)
                i += 1

    raise SuffixError('Ran out of all usable suffixes')

def processbinary(args):
    f = args['file'].buffer
    if args['b'] > io.DEFAULT_BUFFER_SIZE:
        rsize = io.DEFAULT_BUFFER_SIZE
    else:
        rsize = args['b']
    for sfx in args['a']:
        with io.open(args['name'] + sfx, mode='wb') as of:
            i = 0
            b = True
            while i < args['b'] and b:
                b = f.read(rsize)
                if not b:
                    f.close()
                    return
                bytes_written = of.write(b)
                if bytes_written != len(b):
                    raise IOError('Bytes not written')
                i += bytes_written

    raise SuffixError('Ran out of all usable suffixes')

def splitfile(args):
    if args['b'] != None: processbinary(args)
    else: processtext(args)

def run(argv):
    args = getargs(argv)
    try: splitfile(args)
    except NotImplementedError: sys.stderr.write(str(args) + '\n')
    except SuffixError as se:
        sys.stderr.write(str(se.value) + '\n')
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    run(sys.argv[1:])

