import ctypes as c
from ctypes import wintypes as w
from struct import *
from time import *
import datetime
import sys
import time
import numpy as np

k32 = c.windll.kernel32

OpenProcess = k32.OpenProcess
OpenProcess.argtypes = [w.DWORD,w.BOOL,w.DWORD]
OpenProcess.restype = w.HANDLE

ReadProcessMemory = k32.ReadProcessMemory
ReadProcessMemory.argtypes = [w.HANDLE,w.LPCVOID,w.LPVOID,c.c_size_t,c.POINTER(c.c_size_t)]
ReadProcessMemory.restype = w.BOOL

WriteProcessMemory = k32.WriteProcessMemory
WriteProcessMemory.argtypes = [w.HANDLE,w.LPCVOID,w.LPVOID,w.DWORD, w.LPDWORD]
WriteProcessMemory.restype = w.BOOL
PAA = 0x1F0FFF
address = 0x04000000

buff = c.create_string_buffer(4)
bufferSize = (c.sizeof(buff))
bytesRead = c.c_ulonglong(0)

addresses_list = range(address,0x12000000,0x4)

class Search(object):


    def __init__(self):
        self.ph = None
        self.reslut1 = []
        self.reslut2 = []

    def getPh(self, pid):
        # pid = guii.pid
        self.ph = OpenProcess(PAA,False,int(pid))

    # def firstSearch(self, first):
    #     for i in addresses_list:
    #         ReadProcessMemory(self.ph, c.c_void_p(i), buff, bufferSize, c.byref(bytesRead))
    #         value = unpack('I',buff)[0]
    #         if value == int(first):
    #             self.reslut1.append(i)
    #     return self.reslut1

    def firstSearch(self, first):
        self.reslut1 = []
        self.reslut2 = []
        first = int(first)
        offset = 0x04000000
        end_offset = 2200000000
       
        chunk = 4096
        while offset < end_offset:
            a = np.zeros(chunk,'i')          
            r = ReadProcessMemory(self.ph, c.c_void_p(offset), a.ctypes.data, a.itemsize*a.size, c.byref(bytesRead))
            if r:
                indices, = np.where(a == first)
                self.reslut1.extend(offset+indices*4)
            try:
                offset += chunk
            except:
                break
        ii = set(self.reslut1)
        self.reslut1 = list(ii)
        return self.reslut1


    def reSearch(self, num):
        for i in self.reslut1:
            i = int(i)
            ReadProcessMemory(self.ph, c.c_void_p(i), buff, bufferSize, c.byref(bytesRead))
            value = unpack('I',buff)[0]
            if value == int(num):
                self.reslut2.append(i)
        self.reslut1 = self.reslut2
        return self.reslut2

    def change(self, data, cho, addr = None):
        newdata = c.c_long(int(data))
        if cho == 1:
            WriteProcessMemory(self.ph, c.c_void_p(int(addr)), c.byref(newdata), 4, None)

        else:
            if len(self.reslut2) == 1:
                WriteProcessMemory(self.ph, self.reslut2[0], c.byref(newdata), 4, None)