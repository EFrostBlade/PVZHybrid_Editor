
import ctypes
import time
import pymem.exception
import pymem.ressources.kernel32
import pymem.ressources.structure
import pymem.process
import pymem.memory
import pymem.thread
import PVZ_data as data

EAX= 0
ECX= 1
EDX= 2
EBX= 3
ESP= 4
EBP= 5
ESI= 6
EDI= 7


class Asm:
    def __init__(self,startAddress):
        self.code = bytearray(2048)
        self.index = 0
        self.startAddress=startAddress

    def add_byte(self, val):
        self.code[self.index] = val
        self.index += 1

    def add_word(self, val):
        self.code[self.index:self.index + 2] = val.to_bytes(2, 'little')
        self.index += 2

    def add_dword(self, val):
        self.code[self.index:self.index + 4] = val.to_bytes(4, 'little')
        self.index += 4

    def push_dword(self, val):
        self.add_byte(0x68)
        self.add_dword(val)

    def push_byte(self, val):
        self.add_byte(0x6a)
        self.add_byte(val)

    def mov_exx(self, exx, val):
        self.add_byte(0xb8 + exx)
        self.add_dword(val)

    def mov_exx_dword_ptr(self, exx, val):
        self.add_byte(0x8b)
        self.add_byte(0x05 + exx * 8)
        self.add_dword(val)

    def mov_exx_dword_ptr_eyy_add_byte(self, exx, eyy, val):
        self.add_byte(0x8b)
        self.add_byte(0x40 + exx * 8 + eyy)
        self.add_byte(val)

    def mov_exx_dword_ptr_eyy_add_dword(self, exx, eyy, val):
        self.add_byte(0x8b)
        self.add_byte(0x80 + exx * 8 + eyy)
        self.add_dword(val)

    def push_exx(self, exx):
        self.add_byte(0x50 + exx)

    def pop_exx(self, exx):
        self.add_byte(0x58 + exx)

    def ret(self):
        self.add_byte(0xc3)

    def call(self, addr):
        # 计算相对偏移量，需要减去当前指令的长度（5字节）
        relative_offset = addr - (self.startAddress+self.index + 5)
        # 将相对偏移量转换为32位有符号整数的字节序列
        # 使用 int.to_bytes 方法，并指定字节长度为4，使用小端字节序
        # 使用 signed=True 来允许负数的转换
        offset_bytes = relative_offset.to_bytes(4, byteorder='little', signed=True)
        self.add_byte(0xe8)  # call 指令的操作码
        self.code[self.index:self.index + 4] = offset_bytes
        self.index += 4

    def mov_exx_eyy(self, exx, eyy):
        self.add_byte(0x89)
        self.add_byte(0xc0 + eyy * 8 + exx)


def runThread(cla):
    process_handle = pymem.process.open(data.PVZ_pid)
    startAddress=pymem.memory.allocate_memory(process_handle, 1024) 
    print(hex(startAddress))
    asm=cla.creat_asm(startAddress+1)
    shellcode=b'\x60'+bytes(asm.code[:asm.index])+b'\x61\xc3'
    print(shellcode.hex(','))
    data.PVZ_memory.write_bytes(startAddress,shellcode,asm.index+3)
    data.PVZ_memory.write_bytes(0x00552014,b'\xfe',1)
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



