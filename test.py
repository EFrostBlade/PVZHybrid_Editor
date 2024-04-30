from PIL import Image
Image.CUBIC = Image.BICUBIC
from pymem import Pymem
import win32gui
import win32process
import psutil
import re
import time
import os
import sys
import ctypes
import pymem.exception
import pymem.ressources.kernel32
import pymem.ressources.structure
import pymem.process
import pymem.memory
import pymem.thread
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.tooltip import ToolTip
import PVZ_data as data
import PVZ_Hybrid as pvz
import PVZ_asm

pid=55960
pm=Pymem(pid)


process_handle = pymem.process.open(pid)
startAddress=pymem.memory.allocate_memory(process_handle, 1024) 
print(hex(startAddress))

asm=PVZ_asm.Asm(startAddress)
asm.mov_exx_dword_ptr(PVZ_asm.EAX,0x006A9EC0)
asm.mov_exx_dword_ptr_eyy_add_dword(PVZ_asm.ESI,PVZ_asm.EAX,0x00000774)
asm.mov_exx(PVZ_asm.EBX,10)
asm.imul_exx_eyy_byte(PVZ_asm.EDX,PVZ_asm.EBX,0xf)
asm.lea_exx_byte_dword(PVZ_asm.EAX,0x96,0xa4)
asm.push_exx(PVZ_asm.EAX)
asm.mov_exx_eyy(PVZ_asm.EAX,PVZ_asm.ESI)
asm.call(0x00486030)
shellcode=b'\x60'+bytes(asm.code[:asm.index])+b'\x61\xc3'
pm.write_bytes(startAddress,shellcode,asm.index+3)
pm.write_bytes(0x00552014,b'\xfe',1)
thread_h = pymem.ressources.kernel32.CreateRemoteThread(
            process_handle,
            ctypes.cast(0, pymem.ressources.structure.LPSECURITY_ATTRIBUTES),
            0,
            startAddress,
            0,
            0,
            ctypes.byref(ctypes.c_ulong(0))
        ) 
exit_code=ctypes.c_ulong()
while(1):
    pymem.ressources.kernel32.GetExitCodeThread(thread_h,ctypes.byref(exit_code))
    if(exit_code.value==259):
        pass
    else:
        data.PVZ_memory.write_bytes(0x00552014,b'\xdb',1)
        break
    time.sleep(0.001)    
pymem.memory.free_memory(process_handle, startAddress) 