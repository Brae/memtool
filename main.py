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


def searchmem(fd, margins=40):
    #WIP
    print "\n=============================\n=     Search for string     =\n"
    try:
        start = input("\tEnter start address for search: ")
        end = input("\tEnter end address for search: ")
        srch = raw_input("\tEnter the string to search for: ")
    except SyntaxError:
        print ("\t[!] Invalid input. Please retry.")
        searchmem(fd)
    results = []
    for pointer in range(start, end, 1024*1024): #step through memory 1MB at a time
        seg = readmem(fd, pointer, 1024*1024)
        if srch in seg and not "msrch(" in seg:
            offset = seg.index(srch)
            results.append(str(seg[offset-margins:offset+len(srch)]))
            #results.append(pointer+offset)
        if srch.encode("utf-16le") in seg and not "msrch(" in seg:
            offset = seg.index(srch.encode("utf-16le"))
            results.append(str(seg[offset-margins:offset+(len(srch)*2)]))
            #results.append(pointer+seg.index(srch.encode("utf-16le")))
        if srch.encode("utf-16be") in seg and not "msrch(" in seg:
            offset = seg.index(srch.encode("utf-16be"))
            results.append(str(seg[offset-margins:offset+(len(srch)*2)]))
            #results.append(pointer+seg.index(srch.encode("utf-16be")))
    if not results:
        print "\n-----------------------------\n\n\tNo matches found in this address range\n"
    else:
        print "\n-----------------------------\n\n"
        for a in results:
            print "\t", a, "\n"

    temp = raw_input("\tSearch comlete\n\tNew search? (y/N)    -> ")
    if temp == 'y' or temp == 'Y':
        searchmem(fd)
    else:
        return


def menu(fd):
    print "\n=============================\n"
    print "Menu:\n\t1 - Search memory for string\n\t2 - Read section of memory\n\n\tq - Quit program\n"
    c = raw_input("\t> ")
    if c == '1':
        print "\n\t[i] Launching 'searchmem()'..."
        searchmem(fd)
        menu(fd)
    elif c == '2':
        print "\n\t[i] Launching 'readmem()'..."
    elif c == 'q' or c == 'Q':
        sys.exit(0)
    else:
        print "\n\t[!] Input not recognised. Please try again"
        menu(fd)


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
