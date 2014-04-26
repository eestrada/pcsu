#!/usr/bin/env python3
import sys
import io
import copy
import argparse
import string
import collections
import textwrap

from .utils import cpiofile
import tarfile

def getargs(argv):
    argv = list(copy.copy(argv))

    #NAME='pax'
    NAME=argv.pop(0)

    t = textwrap.TextWrapper(width=70, replace_whitespace=False, drop_whitespace=True,
        expand_tabs=False)

    DESCRIPTION= t.fill('''The pax utility shall read, write, and write lists of the members of archive files and copy directory hierarchies. A variety of archive formats shall be supported; see the -x format option.

The action to be taken depends on the presence of the -r and -w options. The four combinations of -r and -w are referred to as the four modes of operation: list, read, write, and copy modes.''')

    EPILOG=''''''

    prsr = argparse.ArgumentParser(prog=NAME, description=DESCRIPTION,
        epilog=EPILOG, add_help=False, formatter_class=argparse.RawDescriptionHelpFormatter)

    prsr.add_argument('-r', dest='read', action='store_true', 
        help='''Read an archive file from standard input.''')

    prsr.add_argument('-w', dest='write', action='store_true', 
        help='''Write files to the standard output in the specified archive format.''')

    prsr.add_argument('-a', dest='append', action='store_true',
        help='''Append files to the end of the archive.''')

    prsr.add_argument('-b', dest='blocksize', metavar='blocksize', action='store', 
        type=_blocksize, default=None, help='''Block the output at a positive decimal integer number of bytes per write to the archive file. It is not possible to specify a blocksize value larger than 32256. Default blocking when creating archives depends on the archive format.''')

    prsr.add_argument('-c', action='store_true', 
        help='''Match all file or archive members except those specified by the pattern or file operands.''')

    prsr.add_argument('-d', action='store_true', 
        help='''Cause files of type directory being copied or archived or archive members of type directory being extracted or listed to match only the file or archive member itself and not the file hierarchy rooted at the file.''')

    prsr.add_argument('-f', metavar='archive', dest='file', action='store',
        default=None, help='''Specify the pathname of the input or output archive, overriding the default standard input (in list or read modes) or standard output (write mode).''')

    prsr.add_argument('-H', action='store_true', help='''If a symbolic link referencing a file of type directory is specified on the command line, pax shall archive the file hierarchy rooted in the file referenced by the link, using the name of the link as the root of the file hierarchy.''')

    prsr.add_argument('-i', action='store_true', help='''Interactively rename files or archive members.''')

    prsr.add_argument('-k', action='store_true', help='''Prevent the overwriting of existing files.''')

    prsr.add_argument('-l', action='store_true', help='''(The letter ell.) In copy mode, hard links shall be made between the source and destination file hierarchies whenever possible.''')

    prsr.add_argument('-L', action='store_true', help='''If a symbolic link referencing a file of type directory is specified on the command line or encountered during the traversal of a file hierarchy, pax shall archive the file hierarchy rooted in the file referenced by the link, using the name of the link as the root of the file hierarchy. ''')

    prsr.add_argument('-n', action='store_true', help='''Select the first archive member that matches each pattern operand. No more than one archive member shall be matched for each pattern (although members of type directory shall still match the file hierarchy rooted at that file).''')

    prsr.add_argument('-o', metavar='options', dest='options', action='store',
        help='''Keyword options.''')

    prsr.add_argument('-p', metavar='string', dest='privileges', action='store',
        help='''File characteristic options (privileges).''')

    prsr.add_argument('-s', metavar='replstr', dest='substitute', action='store',
        help='''Modify file or archive member names according to the substitution expression replstr.''')

    prsr.add_argument('-t', dest='time', action='store_true', 
        help='''When reading files from the file system, and if the user has the permissions required by utime() to do so, set the access time of each file read to the access time that it had before being read by pax.''')

    prsr.add_argument('-u', action='store_true', 
        help='''Ignore files that are older (having a less recent file modification time) than a pre-existing file or archive member with the same name.''')

    prsr.add_argument('-v', dest='verbose', action='store_true', 
        help='''In list mode, produce a verbose table of contents (see the STDOUT section). Otherwise, write archive member pathnames to standard error (see the STDERR section).''')

    prsr.add_argument('-x', metavar='format', dest='format', action='store',
        default='pax', choices=('cpio','pax','ustar'), help='''Specify the output archive format. The pax utility shall support the following formats: cpio, pax, ustar. The default is pax.''')

    prsr.add_argument('-X', action='store_true', 
        help='''When traversing the file hierarchy specified by a pathname, pax shall not descend into directories that have a different device ID''')

    prsr.add_argument('--version', action='version', version='%(prog)s 1.0',
        help="Show program's version number and exit.")

    prsr.add_argument('-h', '--help', action='help', 
        help='Show this help message and exit.')

    ns = prsr.parse_args(argv)
    args = vars(ns)

    # FIXME: This assumes we are always reading from stdin, which may not always be the case
    if args['file'] is None:
        args['file'] = sys.stdin.detach()

    return args

def _blocksize(string):
    retval = int(string)
    if retval < 512 or retval > 32256:
        raise ValueError("Blocksize value must be between 512 and 32256, inclusive.")
    return retval

def listArchive(args):
    cpiofp = cpiofile.open(fileobj=args['file'])
    print(cpiofp)
    
    for farch in cpiofp:
        print(farch)
    #sys.stdout.buffer.write(args['file'].read())
    #raise NotImplementedError('pax list functionality not implemented')

def createArchive(args):
    raise NotImplementedError()

def extractArchive(args):
    raise NotImplementedError()

def main(argv):
    args = getargs(argv)
    try:
        listArchive(args)
    except NotImplementedError as e:
        sys.stderr.write('Exception caught!\n')
        sys.stderr.write('%s: %s\n' % (e, str(args)))
        raise e
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)

