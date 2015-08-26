#!python

__author__ = "Brae <brae@brae.io"

from winpmem import *
import subprocess
import sys
import os

def readmem(fd, start, size, verbose=False):
    if verbose==False:
        win32file.SetFilePointer(fd, start, 0 )
        x,data = win32file.ReadFile(fd, size)
        return data
    elif verbose==True:
        win32file.SetFilePointer(fd, start, 0)
        data = win32file.ReadFile(fd, size)
        while True:
            output = raw_input("\n\tOutput to file? (y/N)\t->")
            if output == "y" or output == "Y":
                fname = raw_input("\n\tEnter file name: ")
                print "\n\t[i] Opening file. Will create new file if it doesn't already exist"
                dumpfd = open(fname, "wb")
                print "\n\t[i] File opened\n\t[i] Writing data to file"
                dumpfd.write(str(data))
                print "\n\t[i] Memory data successfully written to '",fname,"'. Closing file"
                dumpfd.close()
                print "\n\t[i] File closed"
                break
            elif output == "n" or output == "N":
                print "\n\t[i] Dumping data to stdout\n\n=============================\n",str(data),"\n=============================\n"
                break

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
    offsets = []
    for pointer in range(start, end, 1024*1024): #step through memory 1MB at a time
        seg = readmem(fd, pointer, 1024*1024)
        if srch in seg and not "msrch(" in seg:
            offset = seg.index(srch)
            results.append(str(seg[offset-margins:offset+len(srch)]))
            offsets.append(str(pointer+offset))
            #results.append(pointer+offset)
        if srch.encode("utf-16le") in seg and not "msrch(" in seg:
            offset = seg.index(srch.encode("utf-16le"))
            results.append(str(seg[offset-margins:offset+(len(srch)*2)]))
            offsets.append(str(pointer+offset))
            #results.append(pointer+seg.index(srch.encode("utf-16le")))
        if srch.encode("utf-16be") in seg and not "msrch(" in seg:
            offset = seg.index(srch.encode("utf-16be"))
            results.append(str(seg[offset-margins:offset+(len(srch)*2)]))
            offsets.append(str(pointer+offset))
            #results.append(pointer+seg.index(srch.encode("utf-16be")))
    if not results:
        print "\n-----------------------------\n\n\tNo matches found in this address range\n"
    else:
        print "\n-----------------------------\n\n"
        for i in range(0,len(results)):
            print "\t",offsets[i],"\t", results[i], "\n"

    temp = raw_input("\tSearch comlete\n\tNew search? (y/N)    -> ")
    if temp == 'y' or temp == 'Y':
        searchmem(fd)
    else:
        return

def monitor(fd):
    print "\n=============================\n=    Monitor for string     =\n"
    srch = raw_input("\n\tSearch pattern: ")
    print "\n\tYou will now need to enter the start and end positions for each section of memory to search.\n\tTo finish just leave the start field blank"
    bounds = []
    counter = 1
    while True:
        print "\n\tSection ", counter, ": "
        try:
            tempStart = input("\tStart: ")
        except SyntaxError:
            break
        while True:
            tempEnd = input("\tEnd: ")
            if tempEnd:
                break
        bounds.append([tempStart, tempEnd])
        counter+=1
    #Main loop for scanning memory constantly. Can be stopped by CTRL+C

    print "\n=============================\n"
    raw_input("Press any key to start scanning. Use CTRL+C at any time to stop the process")
    print "\n"

    detections = []
    while True:
        try:
            for numB in range(0, len(bounds), 1): #go through each of the bounds parameters
                for pointer in range(bounds[numB][0], bounds[numB][1], 1024*1024): #step through memory 1MB at a time
                    seg = readmem(fd, pointer, 1024*1024)
                    if srch in seg and not "msrch(" in seg:
                        offset = seg.index(srch)
                        if not str(seg[offset-20:offset+len(srch)]) in detections:
                            print "\t",str(pointer+offset),"\t",str(seg[offset-20:offset+len(srch)])
                            detections.append(str(seg[offset-20:offset+len(srch)]))
                    if srch.encode("utf-16le") in seg and not "msrch(" in seg:
                        offset = seg.index(srch.encode("utf-16le"))
                        if not str(seg[offset-20:offset+(len(srch)*2)]) in detections:
                            print "\t",str(pointer+offset),"\t",str(seg[offset-20:offset+(len(srch)*2)])
                            detections.append(str(seg[offset-20:offset+(len(srch)*2)]))
                    if srch.encode("utf-16be") in seg and not "msrch(" in seg:
                        offset = seg.index(srch.encode("utf-16be"))
                        if not str(seg[offset-20:offset+(len(srch)*2)]) in detections:
                            print "\t",str(pointer+offset), "\t", str(seg[offset-20:offset+(len(srch)*2)])
                            detections.append(str(seg[offset-20:offset+(len(srch)*2)]))
        except KeyboardInterrupt:
            break

def cleanup(fd):
    fd.close()
    print "\n\t[i]Unloading winpmem driver"
    DEVNULL = open(os.devnull, 'wb')
    chk = subprocess.call(["winpmem_2.0.1.exe", "-u"], stdout=DEVNULL, stderr=subprocess.STDOUT)
    if chk != 0:
        print "\n\t[!] Error occured unloading driver."
        sys.exit(0)
    else:
        print "\n\t[i] Winpmem driver unloaded successfully\n\t[i] Exiting..."
        sys.exit(0)


def menu(fd):
    print "\n=============================\n"
    print "Menu:\n\t1 - Search memory for string\n\t2 - Read section of memory\n\t3 - Monitor memory for pattern\n\n\tq - Quit program\n"
    c = raw_input("\t> ")
    if c == '1':
        print "\n\t[i] Launching 'searchmem()'..."
        searchmem(fd)
        menu(fd)
    elif c == '2':
        print "\n\t[i] Launching 'readmem()'..."
        readStart = input("\n\n\tEnter start address: ")
        readSize = input("\n\tSize of read: ")
        readmem(fd, readStart, readSize, verbose=True)
        menu(fd)
    elif c == '3':
        print "\n\t[i] Launching 'monitor()'..."
        monitor(fd)
        menu(fd)
    elif c == 'q' or c == 'Q':
        cleanup(fd)
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
