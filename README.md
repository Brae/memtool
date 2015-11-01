# memtool
PoC tool for analysis of volatile memory.

Notes:

* http://www.rekall-forensic.com/
* Link above includes a signed driver for memory dumping, which is normally integrated into their own Python program.
*

/tools/windows/winpmem/executable/main.cpp
* Only includes ```winpmem.h```
* ```int _tmain(int argc, _TCHAR* argv[])```
    * Calls WinPmemFactory() - this returns ```new WinPmem32()``` if the processor architecture is INTEL, or ```new WinPmem64()``` if architecture is AMD64.
    * Parses and deals with commandline flags
    * **```print_memory_info()```**
    * **```install_driver()```**
    * **```set_write_enabled()```**
    * **```set_driver_filename(TCHAR*)```**

Tasks:

[ ] Create custom python script to read and correctly display memory address ranges

* http://www.rekall-forensic.com/faq.html: information on issues with symbol acquisition

__ntkrnlmp.pdb__ for Windows 8.1 on Rig:
GUID = 3BAEE2762F6442089EF8B926DDC8DBA61
Offset = 0x00014ccceb48

###Creating Profile for Windows kernel:###
==

**Scan for GUID of kernel**
rekal -f [*image name*] version_scan --name_regex ntkrnl

**Download .pdb symbols for kernel**
* rekal fetch_pdb --pdb_filename ntkrnlmp.pdb --guid [*guid from previous step here*]
* *Listing of known GUIDs can be found here* - https://github.com/google/rekall-profiles/blob/gh-pages/v1.0/src/guids.txt

**Convert .pdb into .json for rekal**
* rekal parse_pdb --output ntkrnlmp.json --profile_class [*used Win8SP1x64 for Win 8.1 x64*] ntkrnlmp.pdb

**Run commands**
* rekal --profile ./ntkrnlmp.json -f [*filename*] [*plugin*]

==

Above applies when using the python version of Rekall, try the .exe? Installs to C:\Program Files\Rekall.

`c:\Program Files\Rekall\rekall.exe -f [*image file path*]`

On 8.1 VM in lab, this successfully autodetected the profile required and seems to be detecting contents appropriately.

==

Basic introduction to Winpmem - https://isc.sans.edu/forums/diary/Winpmem+Mild+mannered+memory+aquisition+tool/17054

How to use Winpmem driver in custom python scripts - https://isc.sans.edu/forums/diary/Searching+live+memory+on+a+running+machine+with+winpmem/17063/

* `winpmem.exe -l` - loads device driver
* Creates \\.\pmem device which can be reused in some python code
* `win32file.CreateFile(r"\\.\pmem",win32file.GENERIC_READ |
win32file.GENERIC_WRITE,win32file.FILE_SHARE_READ |
win32file.FILE_SHARE_WRITE,None,win32file.OPEN_EXISTING,win32file.FILE_ATTRIBUTE_NORMAL,None)` - creates handle
* `win32file.SetFilePointer(*handle*,*start address*,*FILE_BEGIN* or *FILE_CURRENT* or *FILE_END*)` - point to address to be read
* `win32file.ReadFile()` - read bytes from location

==

###Code from links above to read memory sections and search for string###
```python
from winpmem import *

def readmem(fd, start, size):
    win32file.SetFilePointer(fd, start, 0 )
    x,data = win32file.ReadFile(fd, size)
    return data


def memsrch(fd, srchstr,start, end, numtofind=1, margins=20,verbose=False,includepython=False):
    srchres=[]
    for curloc in range(start, end, 1024*1024):
        x=readmem(fd, curloc,1024*1024)
        if srchstr in x and (includepython or not "msrch(" in x):
            offset=x.index(srchstr)
            if verbose:print curloc+offset,str(x[offset-margins:offset+len(srchstr)+margins])
            srchres.append(curloc+x.index(srchstr))
        if srchstr.encode("utf-16le") in x and (includepython or not "msrch(".encode("utf-16le") in
x):
            offset=x.index(srchstr.encode("utf-16le"))
            if verbose:print curloc+offset,str(x[offset-margins:offset+(len(srchstr)*2)+margins])
            srchres.append(curloc+x.index(srchstr.encode("utf-16le")))
        if srchstr.encode("utf-16be") in x and (includepython or not "msrch(".encode("utf-16be") in
x):
            offset=x.index(srchstr.encode("utf-16be"))
            if verbose:print curloc+offset,str(x[offset-margins:offset+(len(srchstr)*2)+margins])
            srchres.append(curloc+x.index(srchstr.encode("utf-16be")))
        if len(srchres)>=numtofind:
            break
    return srchres

fd = win32file.CreateFile(r"\\.\pmem",win32file.GENERIC_READ |
win32file.GENERIC_WRITE,win32file.FILE_SHARE_READ |
win32file.FILE_SHARE_WRITE,None,win32file.OPEN_EXISTING,win32file.FILE_ATTRIBUTE_NORMAL,None)
```

##Prerequisites:##
* Install Python 2.7 (NOT 3)
* pywin32 - http://sourceforge.net/projects/pywin32/

==

##Laptop Info##

4 memory ranges:
* Start 0x00001000 - Length 0x0009C000
* Start 0x00200000 - Length 0x00002000
* Start 0x00103000 - Length 0xB753C000
* Start 0xB77FF000 - Length 0x00001000

==

##Registry info##

Good whitepaper from 2008 - http://www.dfrws.org/2008/proceedings/p26-dolan-gavitt.pdf
