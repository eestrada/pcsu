from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import sys
import os
import io
import stat
import time
import copy

from builtins import open as _open # Since 'open' is TarFile.open
from builtins import type as _type 

#######################################################################
# cpio.h constants
#######################################################################

# c_mode constants
C_IRUSR =   int('0000400')
C_IWUSR =   int('0000200')
C_IXUSR =   int('0000100')

C_IRGRP =   int('0000040')
C_IWGRP =   int('0000020')
C_IXGRP =   int('0000010')

C_IROTH =   int('0000004')
C_IWOTH =   int('0000002')
C_IXOTH =   int('0000001')

C_ISUID =   int('0004000')
C_ISGID =   int('0002000')
C_ISVTX =   int('0001000')

C_ISDIR =   int('0040000')
C_ISFIFO =  int('0010000')
C_ISREG =   int('0100000')
C_ISBLK =   int('0060000')
C_ISCHR =   int('0020000')
C_ISCTG =   int('0110000')
C_ISLNK =   int('0120000')
C_ISSOCK =  int('0140000')

MAGIC = b'070707'

# end of cpio.h constants

# other constants
BINARY_MAGIC = int(MAGIC) 
POSIX_MAGIC = MAGIC 
ASCII_MAGIC = b'070701' 

NULL = b'\0'
BLOCKSIZE = 512

BIN_FORMAT = 0
POSIX_FORMAT = 1
ASCII_FORMAT = 2
DEFAULT_FORMAT = POSIX_FORMAT


class CpioError(Exception):
    """Base Exception."""
    pass

class ReadError(CpioError):
    """Exception for unreadable cpio archives."""
    pass

class StreamError(CpioError):
    """Exception for unsupported operations on stream-like CpioFiles."""
    pass

class ExtractError(CpioError):
    """General exception for extract errors."""
    pass

class HeaderError(CpioError):
    """Base exception for header errors."""
    pass

class EmptyHeaderError(HeaderError):
    """Exception for empty headers."""
    pass

class TruncatedHeaderError(HeaderError):
    """Exception for truncated headers."""
    pass

class EOFHeaderError(HeaderError):
    """Exception for end of file headers."""
    pass

class InvalidHeaderError(HeaderError):
    """Exception for invalide headers."""
    pass

class CpioInfo(object):
    __magic_num = b'070707' 
    def __init__(self, name=""):
        # Public data attributes
        self.name = str()
        self.size = int()
        self.mtime = int()
        self.mode = int()
        self.type = int()
        self.uid = int()
        self.gid = int()
        self.dev = int()
        self.ino = int()
        self.nlink = int()
        self.rdev = int()

        # Private data attributes
        self.__c_magic = __magic_num
        self.__c_dev = NotImplemented
        self.__c_ino = NotImplemented
        self.__c_mode = NotImplemented
        self.__c_uid = NotImplemented
        self.__c_gid = NotImplemented
        self.__c_nlink = NotImplemented
        self.__c_rdev = NotImplemented
        self.__c_mtime = NotImplemented
        self.__c_namesize = NotImplemented
        self.__c_filesize = NotImplemented
        self.__c_name = NotImplemented
        self.__c_filedata = NotImplemented

    def frombuf(self, buf):
        raise NotImplementedError()

    def fromcpiofile(self, cpiofile):
        raise NotImplementedError()

    def tobuf(self, errors='raise'):
        raise NotImplementedError()

class CpioFile(object):
    def __init__(self, name, mode, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def open(self, **kwargs):
        raise NotImplementedError()

def open(name=None, mode='r', fileobj=None, bufsize=10240, **kwargs):
    pass

def is_cpiofile(name):
    try:
        cf = CpioFile.open(name)
    except CpioError:
        return False
    else:
        cf.close()
        return True

def run(argv):
    prog = os.path.basename(argv[0])
    msg = 'utility "{}" not yet implemented'.format(prog)

    try:
        # Run main functions in here
        raise NotImplementedError(msg)
    except Exception as e:
        sys.stderr.write('{}: {}\n'.format(e.__class__.__name__, e))
        raise SystemExit(1)

def _test(argv):
    '''Run tests on module code'''
    run(argv)

if __name__ == "__main__":
    _test(sys.argv)

