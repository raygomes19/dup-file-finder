import os

class FileObject:
    def __init__(self, fname):
        self.fname = fname

    def setpath(self, fpath):
        self.fpath = fpath

    def setcurrentpath(self):
        # set current path
        self.fpath = os.getcwd()

    def sethash(self, hashval):
        self.hashval = hashval

    def getpath(self):
        return self.fpath

    def getname(self):
        return self.fname

    def gethash(self):
        return self.hashval

    def deletefile(self):
        os.remove(os.path.join(self.fpath, self.fname))

