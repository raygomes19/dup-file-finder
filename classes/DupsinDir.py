from classes import Files
import os, glob, hashlib
import webbrowser, itertools

def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

def calfullhash(fullpath):
    hashobj = hashlib.sha1()
    for chunk in chunk_reader(open(fullpath, 'rb')):
        hashobj.update(chunk)
    return hashobj.hexdigest()

def gethash(hashobj, chunk):
    hashobj.update(chunk)
    return hashobj.hexdigest()

def file_compare(file1, file2):
    file1_hash = hashlib.sha1()
    file2_hash = hashlib.sha1()
    for (chunk1, chunk2) in itertools.zip_longest(chunk_reader(open(file1, "rb")), chunk_reader(open(file2, "rb"))):
        if gethash(file1_hash, chunk1) != gethash(file2_hash, chunk2):
            return False
    return True

class DupsFile:
    def __init__(self, path):
        self.path = path
        self.dirname = "~"

    def find_dups(self):
        matches = []
        self.dirname = "/home/aspera/Documents/DataMining/"
        print("Searching in directory... ", self.dirname)
        for dirp, dirn, files in os.walk(self.dirname):
            for fname in files:
                fullpath = os.path.join(dirp, fname)
                print(fullpath)
                if file_compare(self.path, fullpath):
                    matches.append(fullpath)
        return matches

    def view_dups(self):
        self.dups = self.find_dups()
        print(self.dups)
        if self.dups:
            print("Search completed. Duplicates found!")
            print("Index \t Duplicate File Location")
            for i, x in enumerate(self.dups):
                print(i + 1, x)
        else:
            print("No duplicates found!")
            return 0

    def view_file(self, index):
        print("Opening file...")
        webbrowser.open_new(self.dups[index - 1])

    def delete_file(self, index):
        print("Deleting file...")
        os.remove(self.dups[index - 1])
        print(self.dups[index - 1], "deleted.")
        del self.dups[index - 1]
        print("Index \t Duplicate File Location")
        for i, x in enumerate(self.dups):
            print(i + 1, x)


class DupsDir:
    def __init__(self, path):
        self.path = path

    def find_duplicates(self):
        matches = {}
        dups = {}
        for dirp, dirn, files in os.walk(self.path):
            for fname in files:
                fullpath = os.path.join(dirp, fname)
                print(fullpath)
                hashvalue = calfullhash(fullpath)
                if hashvalue in matches:
                    if fullpath not in matches[hashvalue]:
                        matches[hashvalue].append(fullpath)
                else:
                    matches[hashvalue] = [fullpath]
        for key, value in matches.items():
            if len(value) > 1:
                dups[key] = value
        return dups

    def display_dups(self):
        print("Searching directory...")
        self.duplicates = self.find_duplicates()
        if len(self.duplicates) == 0:
            print("No Duplicates Found!!")
            return False
        else:
            print("Duplicates found in", self.path)
            print("Index", "\t", "No. of duplicates", "\t", "Path of Duplicates")
            for i, k in enumerate(self.duplicates.keys()):
                print("\n", i+1, "\t\t", len(self.duplicates[k]), "\t\t\t", str(self.duplicates[k]))
            #    for v in self.duplicates[k]:
            #        print(v, end=' ')
            return True

    def view_file_dups(self, index):
        dups = list(self.duplicates.values())
        val = dups[index-1]
        return val

    def update_duplicates(self, index, v):
        k = list(self.duplicates.keys())[index-1]
        if len(v) != 0:
            self.duplicates[k] = v
        else:
            del self.duplicates[k]

    def display_file_dups(self,index):
        val = self.view_file_dups(index)
        print("The duplicates of selected file are: ")
        for i, v in enumerate(val):
            print(i + 1, "\t", v)

    def view_file(self, index):
        val = self.view_file_dups(index)
        while True:
            print("Select file index to view...")
            i = int(input())
            print("Opening file...")
            webbrowser.open_new(val[i - 1])
            print("Press n/N to exit, any other key to select other files")
            loop = input()
            if loop == "n" or loop == "N":
                break

    def delete_file(self, index):
        val = self.view_file_dups(index)
        loop = "y"
        while loop != 'n' or loop != 'N':
            print("Select file index to delete...")
            i = int(input())
            print("Deleting file...")
            os.remove(val[i - 1])
            print(val[i-1], "deleted.")
            del val[i-1]
            self.update_duplicates(index, val)
            print("Press n/N to exit, any other key to select other files")
            loop = input()











