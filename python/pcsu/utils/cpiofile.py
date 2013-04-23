import sys
import os
import io

class CpioError(Exception):
    pass

class ReadError(CpioError):
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
    def __init__(self, name, mode):
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

