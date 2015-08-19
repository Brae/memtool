#!python

__author__ = "Brae <brae@brae.io"

from winpmem import *
import subprocess
import sys
import os

def readmem(fd, start, size):
    win32file.SetFilePointer(fd, start, 0 )
    x,data = win32file.ReadFile(fd, size)
    return data

def searchmem(fd):
    #WIP
    print "\n=============================\n=     Search for string     =\n"
    start = input("\tEnter start address for search: ")
    end = input("\tEnter end address for search: ")
    srch = raw_input("\tEnter the string to search for: ")
    results = []
    for pointer in range(start, end, 1024*1024): #step through memory 1MB at a time
        seg = readmem(fd, pointer, 1024*1024)
        if srch in seg and not "msrch(" in seg:
            offset = seg.index(srch)
            results.append(pointer+offset)
        if srch.encode("utf-16le") in seg and not "msrch(" in seg:
            offset = seg.index(srch.encode("utf-16le"))
            srchres.append(pointer+seg.index(srch.encode("utf-16le")))
        if srch.encode("utf-16be") in seg and not "msrch(" in seg:
            offset = seg.index(srch.encode("utf-16be"))
            srchres.append(pointer+x.index(srch.encode("utf-16be")))
    for a in results:
        print "\n-----------------------------\n", a, "\n"
    return



def menu(fd):
    print "\n=============================\n"
    print "Menu:\n\t1 - Search memory for string\n\t2 - Read section of memory"
    c = raw_input("\t> ")
    if c == '1':
        print "\n\t[i] Launching 'searchmem()'..."
        searchmem(fd)
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
menu(fd)




#fd = win32file.CreateFile(r"\\.\pmem", win32file.GENERIC_READ | win32file.GENERIC_WRITE, win32file.FILE_SHARE_READ | win32.FILE_SHARE_WRITE, None, win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None)
