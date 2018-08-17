from classes import DupsinDir as dd
import os, glob, hashlib
from tkinter import filedialog
import tkinter as tk

print("Welcome to Duplicate File Finder")

def exit_app():
    print("Exiting...")
    exit(0)

while True:
    print("Select Option:")
    print("1: Search for duplicate files in a directory")
    print("2: Search for duplicates of a file")
    print("3: Exit Application")
    option = int(input("Enter your option: "))

    if option == 3:
        exit_app()
    elif option == 1:
        application_window = tk.Tk()
        dirname = filedialog.askdirectory(parent=application_window,
                                     initialdir=os.getcwd(),
                                     title="Please select a folder to search")
        application_window.quit()

        dups = dd.DupsDir(dirname)
        if dups.display_dups():
            while True:
                print("Select Option:")
                print("1: View duplicates of a particular file")
                print("2: Go to Main Menu")
                print("3: Exit Application")
                op1 = int(input("Enter your option: "))

                if op1 == 1:
                    op2 = 2
                    while True:
                        index = int(input("Enter index of the file to view duplicates: "))
                        dups.display_file_dups(index)
                        while True:
                            print("Select Option:")
                            print("1: Delete a file")
                            print("2: View the file")
                            print("3: Select another file")
                            print("4: Go to Main Menu")
                            print("5: Exit Application")
                            op2 = int(input("Enter your option: "))

                            if op2 == 5:
                                exit_app()
                            elif op2 == 4 or op2 == 3:
                                break
                            elif op2 == 1:
                                print("delete file")
                            #    dups.delete_file(index)
                            #    dups.display_file_dups(index)
                            elif op2 == 2:
                                print("view file")
                             #   dups.view_file(index)

                        if op2 == 4:
                            op1 = 2
                            break

                if op1 == 3:
                    exit_app()
                if op1 == 2:
                    print("Loading Main Menu")
                    break

    elif option == 2:
        print("Select a file")
        application_window = tk.Tk()
        filename = filedialog.askopenfilename(parent=application_window,
                                            initialdir=os.getcwd(),
                                            title="Please select a file:")
        application_window.destroy()

        print(filename)
        dups = dd.DupsFile(filename)
        dups.view_dups()