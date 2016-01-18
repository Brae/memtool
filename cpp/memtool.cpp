#include <windows.h>
#include <winioctl.h>
#include "winpmem_ioctl.h"
#include <iostream>
#include <stdint.h>

int main() {
  HANDLE pmemDriver = CreateFile("C:/Users/Peter/Documents/Atom/WinPMem/memtool/winpmem_x86.sys", GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);

  if (pmemDriver == INVALID_HANDLE_VALUE) {
    std::cout << "Error: Invalid driver file" << std::endl;
  } else {
    std::cout << "Driver loaded successfully" << std::endl;
  }

  DWORD junk = 0;
  char* buffer = new char[1024*1024];
  BOOL ioctlResult = FALSE;
  unsigned int mode = 1;
  std::cout << "[debug] first driver call";
  DeviceIoControl(pmemDriver, //driver handle
                  (ULONG)INFO_IOCTL_DEPRECATED, //ioctl code
                  &mode, //pointer to driver mode as input buffer(hard coded to physical at the moment as this is the default value. Will want to add if statement to deal with other options passed as parameters later)
                  0, //is this correct? Should be size of input buffer. Taken from Dr Dobbs blog post
                  &buffer, //output buffer
                  1024*1024, //buffer size (set to this size for 1MB)
                  &junk, //dump output into the junk buffer to get rid of it (not required at this stage)
                  (LPOVERLAPPED) NULL //NULL value due to no overlap of data at this point
                );
  std::cout << "...done" << std::endl;
  buffer[1024*1024-1] = 0;
  fputs(buffer, stdout);

  CloseHandle(pmemDriver);
  return 0;
}
