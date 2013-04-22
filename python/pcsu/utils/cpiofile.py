import sys
import os
import io

class CpioError(Exception):
    pass

class ReadError(CpioError):
    pass

class CpioInfo(object):
    __magic_num = b'070707' 
    def __init__(self, name, mode):
        self.c_magic = __magic_num
        self.c_dev = NotImplemented
        self.c_ino = NotImplemented
        self.c_mode = NotImplemented
        self.c_uid = NotImplemented
        self.c_gid = NotImplemented
        self.c_nlink = NotImplemented
        self.c_rdev = NotImplemented
        self.c_mtime = NotImplemented
        self.c_namesize = NotImplemented
        self.c_filesize = NotImplemented
        self.c_name = NotImplemented
        self.c_filedata = NotImplemented

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

