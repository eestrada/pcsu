from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import sys
import os
import io
import stat
import time
import copy
import logging

from builtins import open as _open # Since 'open' is TarFile.open
from builtins import type as _type 

_log = logging.getLogger('pcsu.utils.cpiofile')
_log.setLevel(logging.DEBUG)
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

DIRTYPE =   C_ISDIR
REGTYPE =   C_ISREG
FIFOTYPE =  C_ISFIFO
BLKTYPE =   C_ISBLK
CHRTYPE =   C_ISCHR
CTGTYPE =   C_ISCTG
LNKTYPE =   C_ISLNK
SOCKTYPE =  C_ISSOCK

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
    def __init__(self, name=""):
        # Public data attributes
        self.magic = MAGIC
        self.dev = 0
        self.ino = 0
        self.mode = 0o644
        self.uid = 0
        self.gid = 0
        self.nlink = 0
        self.rdev = 0
        self.mtime = 0
        self.namesize = 0
        self.size = 0

        self.name = str(name)
        self.type = REGTYPE

        self.offset_hdr = 0     # offset to header data
        self.offset_data = 0    # offset to file data
        self.cpiofile = None    # reference to CpioFile object

    def __str__(self):
        return str(vars(self))

    @classmethod
    def frombuf(cls, buf):
        if len(buf) == 0:
            raise EmptyHeaderError()

        info = cls()
        ba = bytearray(buf)

        _magic = ba[:6]
        try:
            info.magic = int(ba[:6], base=8)
        except ValueError as e:
            raise InvalidHeaderError()
        else:
            if _magic != b'070707':
                raise InvalidHeaderError()
            del _magic
            del ba[:6]
        info.dev = int(ba[:6], base=8)
        del ba[:6]
        info.ino = int(ba[:6], base=8)
        del ba[:6]
        info.mode = int(ba[:6], base=8)
        del ba[:6]
        info.uid = int(ba[:6], base=8)
        del ba[:6]
        info.gid = int(ba[:6], base=8)
        del ba[:6]
        info.nlink = int(ba[:6], base=8)
        del ba[:6]
        info.rdev = int(ba[:6], base=8)
        del ba[:6]
        info.mtime = int(ba[:11], base=8)
        del ba[:11]
        info.namesize = int(ba[:6], base=8)
        del ba[:6]
        info.size = int(ba[:11], base=8)
        del ba[:11]

        return info

    @classmethod
    def fromcpiofile(cls, cpiofile):
        raise NotImplementedError()

    fromfile = fromcpiofile

    @classmethod
    def tobuf(cls, format=DEFAULT_FORMAT, errors='strict'):
        raise NotImplementedError()

    def isfile(self):
        return self.isreg()

    def isreg(self):
        return self.type == REGTYPE

    def isdir(self):
        return self.type == DIRTYPE

    def issym(self):
        return self.type == LNKTYPE

    def islnk(self):
        raise NotImplementedError()

    def ischr(self):
        return self.type == CHRTYPE

    def isblk(self):
        return self.type == BLKTYPE

    def isfifo(self):
        return self.type == FIFOTYPE

    def isdev(self):
        return self.ischr() or self.isblk() or self.isfifo()

class CpioMember(io.RawIOBase):
    def __init__(self, cpioinfo):
        if not cpioinfo.cpiofile:
            raise ValueError('CpioInfo object is not associated with a usable CpioFile object.')
        self.cpioinfo = copy.copy(cpioinfo)
        self.cur_pos = 0

    def isatty(self):
        return self.cpioinfo.cpiofile.fileobj.isatty()

    def readable(self):
        return self.cpioinfo.cpiofile.fileobj.readable()

    def seekable(self):
        return self.cpioinfo.cpiofile.fileobj.seekable()

    def writable(self): return False

class CpioFile(object):
    def __init__(self, name=None, mode='r', fileobj=None, **kwargs):
        if len(mode) > 1 or mode not in 'rwa':
            raise ValueError("improper mode supplied: '%s'" % mode)

        self.mode = mode
        self._true_mode = {'r': 'rb', 'w': 'wb', 'a': 'ab'}[mode]

        if fileobj is not None:
            self.fileobj = fileobj
            self._close_fileobj = False
            if hasattr(fileobj, 'mode'):
                self._mode = fileobj.mode
            if name is None and hasattr(fileobj, 'name'):
                name = fileobj.name
        elif name is not None:
            self.fileobj = io.open(name, mode=self._true_mode)
            self._close_fileobj = True
        else:
            raise ValueError("At least one of 'name' or 'fileobj' must have a value. Both were 'None'")

        self.name = name

        self.closed = False

        self._info_list = []

        self._current_member = None

        # all other used keyword arguments
        self.format = kwargs.get('format', DEFAULT_FORMAT)
        self.dereference = kwargs.get('dereference', False)
        self.cpioinfocls = kwargs.get('cpioinfo', CpioInfo)


    @classmethod
    def open(cls, name=None, mode='r', fileobj=None, bufsize=10240, **kwargs):
        msg = 'CpioFile.open has been called with %s\n' % fileobj
        _log.debug(msg)
        return cls(name, mode, fileobj, **kwargs)

    def getmember(self, name):
        raise NotImplementedError()

    def getmembers(self):
        return self._info_list

    def getnames(self):
        return []

    def list(self, verbose=True):
        return []

    def next(self):
        if self._current_member is not None:
            if self._current_member.name == b'TRAILER!!!':
                return None
            self.fileobj.seek(self._current_member.offset_data + self._current_member.size)

        position = self.fileobj.tell()
            
        buf = self.fileobj.read(512)
        try:
            info = self.cpioinfocls.frombuf(buf)
        except HeaderError as e:
            return None
        else:
            info.offset_hdr = position
            info.offset_data = position + info.namesize + 76
            self.fileobj.seek(info.offset_hdr + 76)
            info.name = self.fileobj.read(info.namesize - 1)
            self.fileobj.seek(1, io.SEEK_CUR) # skip null at end of file name
            info.cpiofile = self # make reference to self
            self._current_member = info # make this info object the current info object

            if self._current_member.name == b'TRAILER!!!':
                return None
            self._info_list.append(info) # append to list of info objects
            return info

    def extractall(self, path=".", members=None):
        raise NotImplementedError()

    def extract(self, member, path="."):
        raise NotImplementedError()

    def extractfile(self, member):
        raise NotImplementedError()

    def add(self, name, **kwargs):
        raise NotImplementedError()

    def addfile(self, cpioinfo, fileobj=None):
        raise NotImplementedError()

    def gettarinfo(name=None, arcname=None, fileobj=None):
        return False

    def close(self):
        if self.closed: return

        # TODO: fill remainder of block with NULLs.

        if self._close_fileobj: self.fileobj.close()
        else: self.fileobj.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def __iter__(self):
        """Get an iterator over CpioInfo objects in CpioFile object."""

        while True:
            info = self.next()
            if info is None:
                break
            yield info

open = CpioFile.open

def is_cpiofile(name):
    try:
        cf = CpioFile.open(name)
    except CpioError:
        return False
    else:
        cf.close()
        return True

def main(argv):
    prog = os.path.basename(argv[0])
    msg = 'utility "{}" not yet implemented'.format(prog)

    try:
        # Run main functions in here
        raise NotImplementedError(msg)
    except Exception as e:
        _log.error('{}: {}\n'.format(e.__class__.__name__, e))
        #sys.stderr.write('{}: {}\n'.format(e.__class__.__name__, e))
        sys.exit(1)

def _test(argv):
    '''Run tests on module code'''
    main(argv)

if __name__ == "__main__":
    _test(sys.argv)

