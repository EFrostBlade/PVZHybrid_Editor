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

newmem_putVaseInit=None
newmem_putVaseInit2=None

def putVaseInit():
    global newmem_putVaseInit
    global newmem_putVaseInit2
    
    newmem_putVaseInit = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 512)
    newmem_putVaseInit2 = pymem.memory.allocate_memory(
        data.PVZ_memory.process_handle, 256)
    print(hex(newmem_putVaseInit))
    print(hex(newmem_putVaseInit2))
    shellcode1=asm.Asm(newmem_putVaseInit)
    shellcode1.mov_exx_dword_ptr_eyy_add_byte(asm.EBX,asm.ESP,0x04)
    shellcode1.movzx_exx_dword_ptr_eyy_add_dword(asm.EBX,asm.EBX,newmem_putVaseInit+14)
    shellcode1.ret_word(0x4)
    for i in range(0,256):
        shellcode1.add_byte(i)
    data.PVZ_memory.write_bytes(newmem_putVaseInit, bytes(shellcode1.code[:shellcode1.index]), shellcode1.index)

    shellcode2=asm.Asm(newmem_putVaseInit2)
    shellcode2.push_exx(asm.ESI)
    shellcode2.mov_exx_eyy(asm.ESI,asm.EAX)
    shellcode2.add_exx_dword(asm.ESI,0x0000011C)
    shellcode2.call(0x0041E1C0)
    shellcode2.mov_exx_dword_ptr_eyy_add_byte(asm.EDX,asm.ESP,0x08)
    shellcode2.mov_exx_eyy(asm.ECX,asm.EDI)
    shellcode2.imul_exx_eyy_dword(asm.ECX,asm.ECX,0x00002710)
    shellcode2.add_exx_dword(asm.ECX,0x00049BB0)
    shellcode2.mov_ptr_exx_add_byte_dword(asm.EAX,0x08,0x00000007)
    shellcode2.mov_ptr_exx_add_byte_eyy(asm.EAX,0x1C,asm.ECX)
    shellcode2.mov_ptr_exx_add_byte_eyy(asm.EAX,0x10,asm.EDX)
    shellcode2.mov_ptr_exx_add_byte_eyy(asm.EAX,0x14,asm.EDI)
    shellcode2.mov_exx_dword_ptr_eyy_add_byte(asm.EDI,asm.ESP,0x0C)
    shellcode2.mov_ptr_exx_add_byte_eyy(asm.EAX,0x50,asm.EDI)
    shellcode2.mov_exx_dword_ptr_eyy_add_byte(asm.EDI,asm.ESP,0x10)
    shellcode2.mov_ptr_exx_add_byte_eyy(asm.EAX,0x3C,asm.EDI)
    shellcode2.mov_exx_dword_ptr_eyy_add_byte(asm.EDI,asm.ESP,0x14)
    shellcode2.mov_ptr_exx_add_byte_eyy(asm.EAX,0x40,asm.EDI)
    shellcode2.mov_exx_dword_ptr_eyy_add_byte(asm.EDI,asm.ESP,0x18)
    shellcode2.mov_ptr_exx_add_byte_eyy(asm.EAX,0x44,asm.EDI)
    shellcode2.mov_exx_dword_ptr_eyy_add_byte(asm.EDI,asm.ESP,0x1c)
    shellcode2.mov_ptr_exx_add_byte_eyy(asm.EAX,0x0c,asm.EDI)
    shellcode2.mov_exx_dword_ptr_eyy_add_byte(asm.EDI,asm.ESP,0x20)
    shellcode2.mov_ptr_exx_add_byte_eyy(asm.EAX,0x54,asm.EDI)
    shellcode2.pop_exx(asm.ESI)
    shellcode2.ret_word(0x001C)
    data.PVZ_memory.write_bytes(newmem_putVaseInit2, bytes(shellcode2.code[:shellcode2.index]), shellcode2.index)

putVaseInit()

def putVase(plantTpye,skin,type,zombieType,sun,row,col):
    global newmem_putVaseInit
    global newmem_putVaseInit2
    class vasePut:
        def __init__(self,plantTpye,skin,type,zombieType,sun,row,col):
            self.plantType=plantTpye
            self.skin=skin
            self.type=type
            self.zombieType=zombieType
            self.sun=sun
            self.row=row
            self.col=col
        
        def creat_asm(self,startAddress):
            vasePut_asm=asm.Asm(startAddress)
            vasePut_asm.push_byte(plantTpye)
            vasePut_asm.call(newmem_putVaseInit)
            vasePut_asm.mov_exx_dword_ptr(asm.EAX, 0x006a9ec0)
            vasePut_asm.mov_exx_dword_ptr_eyy_add_dword(
                asm.EAX, asm.EAX,  0x768)
            vasePut_asm.push_byte(0)
            vasePut_asm.push_byte(self.skin)
            vasePut_asm.push_byte(self.type)
            vasePut_asm.push_exx(asm.EBX)
            vasePut_asm.push_byte(self.zombieType)
            vasePut_asm.push_dword(self.sun)
            vasePut_asm.mov_exx(asm.EDI,self.row)
            vasePut_asm.push_byte(self.col)
            vasePut_asm.call(newmem_putVaseInit2)
            return vasePut_asm
        
    asm.runThread(vasePut(plantTpye,skin,type,zombieType,sun,row,col))

putVase(10,3,1,6,128,1,1)