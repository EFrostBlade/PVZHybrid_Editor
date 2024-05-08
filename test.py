import PVZ_asm
import PVZ_Hybrid as pvz
import PVZ_data as data
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
import pymem.thread
import pymem.memory
import pymem.process
import pymem.ressources.structure
import pymem.ressources.kernel32
import pymem.exception
import ctypes
import sys
import os
import time
import re
import psutil
import win32process
import win32gui
import PVZ_asm as asm
from pymem import Pymem
from PIL import Image
Image.CUBIC = Image.BICUBIC

hwnd = win32gui.FindWindow("MainWindow", None)
pid = win32process.GetWindowThreadProcessId(hwnd)
data.update_PVZ_memory(Pymem(pid[1]))
data.update_PVZ_pid(pid[1])

addr = int.from_bytes(data.PVZ_memory.read_bytes(0x00453B24, 1)+data.PVZ_memory.read_bytes(0x00453B23, 1) +
                          data.PVZ_memory.read_bytes(0x00453B22, 1)+data.PVZ_memory.read_bytes(0x00453B21, 1))+0x00453B25

print(hex(addr))
newmem_unlock = pymem.memory.allocate_memory(
    data.PVZ_memory.process_handle, 128)
print(hex(newmem_unlock))
shellcode=asm.Asm(newmem_unlock)
shellcode.push_exx(asm.ESI)
shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ESI,asm.EDI,0x82c)
shellcode.mov_ptr_exx_add_dowrd_dword(asm.ESI,0x1c0,1)
shellcode.pop_exx(asm.ESI)
shellcode.add_byte(0xb0)
shellcode.add_byte(0x01)#mov al,01
shellcode.ret()
shellcode.jmp(0x00840a77)
data.PVZ_memory.write_bytes(newmem_unlock, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
