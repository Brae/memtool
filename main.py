#!python

__author__ = "Brae <brae@brae.io"

from winpmem import *
import subprocess
import sys
import os

def searchmem():
    #TODO
    
def readmem():
    #TODO

def menu():
    print "\n=============================\n"
    print "Menu:\n\t1 - Search memory for string\n\t2 - Read section of memory"
    c = raw_input("\t> ")
    if c == '1':
        print "\n\t[i] Launching 'searchmem()'..."
    elif c == '2':
        print "\n\t[i] Launching 'readmem()'..."
    else:
        print "\n\t[!] Input not recognised. Please try again"
        menu()

print "=============================\n Live memory monitoring tool \n --      For Windows      --\n==============================\n\n"

print "[i] Loading winpmem driver...\n"
chk = subprocess.call(["winpmem_2.0.1.exe", "-l"])
if chk != 0:
    print "[!] Error occured loading driver. Please check it is available in the same directory as this script"
    sys.exit(0)
else:
    print "\n[i] Winpmem driver loaded successfully"

print "[i] Initialising file"
fd = win32file.CreateFile(r"\\.\pmem",win32file.GENERIC_READ | win32file.GENERIC_WRITE,win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,None,win32file.OPEN_EXISTING,win32file.FILE_ATTRIBUTE_NORMAL,None)
menu()




#fd = win32file.CreateFile(r"\\.\pmem", win32file.GENERIC_READ | win32file.GENERIC_WRITE, win32file.FILE_SHARE_READ | win32.FILE_SHARE_WRITE, None, win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None)
