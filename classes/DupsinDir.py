from classes import Files
import os, glob, hashlib
import webbrowser

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

class DupsDir:
    def __init__(self, path):
        self.path = path

    def find_duplicates(self):
        matches = {}
        dups = {}
        for dirp, dirn, files in os.walk(self.path):
            for fname in files:
                fullpath = os.path.join(dirp, fname)
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

    def delete_file(self, li, index):
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









