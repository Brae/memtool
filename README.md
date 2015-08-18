# memtool
PoC tool for analysis of volatile memory.

###See https://gist.github.com/GeneralBrae/d90c8670fca1b2aea931 for detailed notes###

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
