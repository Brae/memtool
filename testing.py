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
        if srchstr.encode("utf-16le") in x and (includepython or not "msrch(".encode("utf-16le") in x):
            offset=x.index(srchstr.encode("utf-16le"))
            if verbose:print curloc+offset,str(x[offset-margins:offset+(len(srchstr)*2)+margins])
            srchres.append(curloc+x.index(srchstr.encode("utf-16le")))
        if srchstr.encode("utf-16be") in x and (includepython or not "msrch(".encode("utf-16be") in x):
            offset=x.index(srchstr.encode("utf-16be"))
            if verbose:print curloc+offset,str(x[offset-margins:offset+(len(srchstr)*2)+margins])
            srchres.append(curloc+x.index(srchstr.encode("utf-16be")))
        if len(srchres)>=numtofind:
            break
    return srchres

fd = win32file.CreateFile(r"\\.\pmem",win32file.GENERIC_READ |
win32file.GENERIC_WRITE,win32file.FILE_SHARE_READ |
win32file.FILE_SHARE_WRITE,None,win32file.OPEN_EXISTING,win32file.FILE_ATTRIBUTE_NORMAL,None)
