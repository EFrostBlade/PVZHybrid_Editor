import ctypes
import time
import struct
import pymem.exception
import pymem.ressources.kernel32
import pymem.ressources.structure
import pymem.process
import pymem.memory
import pymem.thread
import PVZ_data as data

EAX = 0
ECX = 1
EDX = 2
EBX = 3
ESP = 4
EBP = 5
ESI = 6
EDI = 7
AX = 0
CX = 1
DX = 2
BX = 3
SP = 4
BP = 5
SI = 6
DI = 7
AL = 0
CL = 1
DL = 2
BL = 3
AH = 4
CH = 5
DH = 6
BH = 7


class Asm:
    def __init__(self, startAddress=0):
        self.code = bytearray(65536)
        self.index = 0
        self.startAddress = startAddress
        self.labels = {}
        self.pending_jumps = {}  # 存储待回填的跳转指令位置，键为标签，值为跳转指令的索引列表
        self.pending_jothers = {}  # 存储待回填的跳转指令位置，键为标签，值为跳转指令的索引列表
        self.pending_leas = {}  # 存储待回填的lea指令位置，键为标签，值为lea指令的索引列表
        self.pending_pushs = {}  # 存储待回填的push指令位置，键为标签，值为push指令的索引列表

    def get_code(self):
        return bytes(self.code[: self.index])

    def add_bytes(self, val):
        self.code[self.index : self.index + len(val)] = val
        self.index += len(val)

    def add_byte(self, val):
        self.code[self.index] = val
        self.index += 1

    def add_word(self, val):
        self.code[self.index : self.index + 2] = val.to_bytes(2, "little")
        self.index += 2

    def add_dword(self, val):
        self.code[self.index : self.index + 4] = val.to_bytes(4, "little")
        self.index += 4

    def add_exx_dword(self, exx, val):
        if exx == EAX:
            self.add_byte(0x05)
            self.add_dword(val)
        else:
            self.add_byte(0x81)
            self.add_byte(0xC0 + exx)
            self.add_dword(val)

    def add_exx_ptr_dword(self, exx, val):
        self.add_byte(0x03)
        self.add_byte(0x05 + exx * 8)
        self.add_dword(val)

    def add_dword_ptr_exx_add_byte_byte(self, exx, val, val2):
        self.add_byte(0x83)
        self.add_byte(0x40 + exx)
        self.add_byte(val)
        self.add_byte(val2)

    def add_ptr_exx_add_byte_eyy(self, exx, val, eyy):
        self.add_byte(0x01)
        self.add_byte(0x40 + exx + eyy * 8)
        self.add_byte(val)

    def add_ptr_exx_add_eyy_times_add_byte_ezz(self, exx, eyy, times, val, ezz):
        self.add_byte(0x01)
        self.add_byte(0x44 + ezz * 8)
        self.add_byte(exx + eyy * 8 + times * 0x20)
        self.add_byte(val)

    def push_dword(self, val):
        if val < 0:
            # 将负数转换为32位无符号整数的等效值
            val += 2**32
        self.add_byte(0x68)
        self.add_dword(val)

    def push_dword_ptr(self, val):
        self.add_byte(0xFF)
        self.add_byte(0x35)
        self.add_dword(val)

    def push_float(self, val):
        self.add_byte(0x68)
        self.code[self.index : self.index + 4] = struct.pack("f", val)
        self.index += 4

    def push_byte(self, val):
        if val < 0:
            # 将负数转换为8位无符号整数的等效值
            val += 2**8
        self.add_byte(0x6A)
        self.add_byte(val)

    def push_ptr_exx_add_byte(self, exx, val):
        self.add_byte(0xFF)
        self.add_byte(0x70 + exx)
        self.add_byte(val)

    def fldz(self):
        self.add_byte(0xD9)
        self.add_byte(0xEE)

    def fild_dword_ptr_address(self, address):
        self.add_byte(0xDB)
        self.add_byte(0x05)
        self.add_dword(address)

    def fild_dword_ptr_exx_add_byte(self, exx, val):
        self.add_byte(0xDB)
        self.add_byte(0x40 + exx)
        self.add_byte(val)

    def fld_dword_ptr_address(self, address):
        self.add_byte(0xD9)
        self.add_byte(0x05)
        self.add_dword(address)

    def fadd_dword_ptr_address(self, address):
        self.add_byte(0xD8)
        self.add_byte(0x05)
        self.add_dword(address)

    def fsub_dword_ptr_address(self, address):
        self.add_byte(0xD8)
        self.add_byte(0x25)
        self.add_dword(address)

    def fcom_dword_ptr_address(self, address):
        self.add_byte(0xD8)
        self.add_byte(0x15)
        self.add_dword(address)

    def fld_dword_ptr_exx_add_byte(self, exx, val):
        self.add_byte(0xD9)
        self.add_byte(0x40 + exx)
        self.add_byte(val)

    def fld_dword_ptr_exx_add_dword(self, exx, val):
        self.add_byte(0xD9)
        self.add_byte(0x80 + exx)
        self.add_dword(val)

    def fstp_dword_ptr_exx_add_byte(self, exx, val):
        self.add_byte(0xD9)
        self.add_byte(0x58 + exx)
        if exx == ESP:
            self.add_byte(0x24)
        self.add_byte(val)

    def fstp_dword_ptr_exx_add_dword(self, exx, val):
        self.add_byte(0xD9)
        self.add_byte(0x98 + exx)
        self.add_dword(val)

    def fiadd_ptr_exx(self, exx):
        self.add_byte(0xDA)
        self.add_byte(exx)
        if exx == ESP:
            self.add_byte(0x24)

    def fiadd_ptr_exx_add_byte(self, exx, val):
        self.add_byte(0xDA)
        self.add_byte(0x40 + exx)
        if exx == ESP:
            self.add_byte(0x24)
        self.add_byte(val)

    def fistp_dword_ptr_exx(self, exx):
        self.add_byte(0xDB)
        self.add_byte(0x18 + exx)
        if exx == ESP:
            self.add_byte(0x24)

    def fstsw_ax(self):
        self.add_byte(0x9B)
        self.add_byte(0xDF)
        self.add_byte(0xE0)

    def sahf(self):
        self.add_byte(0x9E)

    def mov_e(self, e, val):
        self.add_byte(0xB0 + e)
        self.add_byte(val)

    def mov_exx(self, exx, val):
        self.add_byte(0xB8 + exx)
        self.add_dword(val)

    def mov_exx_fs_offset(self, exx, offset):
        if exx == EAX:
            self.add_byte(0x64)
            self.add_byte(0xA1)
        else:
            self.add_byte(0x64)
            self.add_byte(0x8B)
            self.add_byte(0x05 + exx * 8)
        self.add_dword(offset)

    def mov_exx_dword_ptr(self, exx, val):
        self.add_byte(0x8B)
        self.add_byte(0x05 + exx * 8)
        self.add_dword(val)

    def mov_ex_ptr_dword(self, ex, val):
        if ex == AX:
            self.add_byte(0x66)
            self.add_byte(0xA1)
        else:
            self.add_byte(0x66)
            self.add_byte(0x8B)
            self.add_byte(0x05 + ex * 8)
        self.add_dword(val)

    def mov_exx_dword_ptr_eyy_add_byte(self, exx, eyy, val):
        self.add_byte(0x8B)
        self.add_byte(0x40 + exx * 8 + eyy)
        if eyy == ESP:
            self.add_byte(0x24)
        self.add_byte(val)

    def mov_exx_dword_ptr_eyy_add_dword(self, exx, eyy, val):
        self.add_byte(0x8B)
        self.add_byte(0x80 + exx * 8 + eyy)
        if eyy == ESP:
            self.add_byte(0x24)
        self.add_dword(val)

    def movzx_exx_dword_ptr_eyy_add_dword(self, exx, eyy, val):
        self.add_byte(0x0F)
        self.add_byte(0xB6)
        self.add_byte(0x80 + exx * 8 + eyy)
        self.add_dword(val)

    def mov_exx_dword_ptr_eyy(self, exx, eyy):
        self.add_byte(0x8B)
        self.add_byte(exx * 8 + eyy)

    def push_exx(self, exx):
        self.add_byte(0x50 + exx)

    def pop_exx(self, exx):
        self.add_byte(0x58 + exx)

    def ret(self):
        self.add_byte(0xC3)

    def ret_word(self, val):
        self.add_byte(0xC2)
        self.add_word(val)

    def call(self, addr):
        # 计算相对偏移量，需要减去当前指令的长度（5字节）
        relative_offset = addr - (self.startAddress + self.index + 5)
        # 将相对偏移量转换为32位有符号整数的字节序列
        # 使用 int.to_bytes 方法，并指定字节长度为4，使用小端字节序
        # 使用 signed=True 来允许负数的转换
        offset_bytes = relative_offset.to_bytes(4, byteorder="little", signed=True)
        self.add_byte(0xE8)  # call 指令的操作码
        self.code[self.index : self.index + 4] = offset_bytes
        self.index += 4

    def call_exx(self, exx):
        self.add_byte(0xFF)
        self.add_byte(0xD0 + exx)

    def mov_exx_eyy(self, exx, eyy):
        self.add_byte(0x89)
        self.add_byte(0xC0 + eyy * 8 + exx)

    def xchg_exx_eyy(self, exx, eyy):
        if exx == EAX:
            self.add_byte(0x90 + eyy)
        else:
            self.add_byte(0x87)
            self.add_byte(0xC0 + eyy * 8 + exx)

    def cdq(self):
        self.add_byte(0x99)

    def imul_exx_eyy(self, exx, eyy):
        self.add_byte(0x0F)
        self.add_byte(0xAF)
        self.add_byte(0xC0 + exx * 8 + eyy)

    def imul_exx_eyy_byte(self, exx, eyy, val):
        self.add_byte(0x6B)
        self.add_byte(0xC0 + exx * 8 + eyy)
        self.add_byte(val)

    def imul_exx_eyy_dword(self, exx, eyy, val):
        self.add_byte(0x69)
        self.add_byte(0xC0 + exx * 8 + eyy)
        self.add_dword(val)

    def lea_exx_byte_dword(self, exx, exy, val):
        self.add_byte(0x8D)
        self.add_byte(0x84 + exx * 8)
        self.add_byte(exy)  # exx+(eyy)*8
        self.add_dword(val)

    def lea_exx_ptr_eyy(self, exx, eyy):
        self.add_byte(0x8D)
        self.add_byte(0x00 + exx * 8 + eyy)
        if eyy == ESP:
            self.add_byte(0x24)

    def lea_exx_ptr_eyy_add_byte(self, exx, eyy, val):
        self.add_byte(0x8D)
        self.add_byte(0x40 + exx * 8 + eyy)
        if eyy == ESP:
            self.add_byte(0x24)
        self.add_byte(val)

    def lea_exx_ptr_eyy_add_ezz_times(self, exx, eyy, ezz, times):
        self.add_byte(0x8D)
        self.add_byte(0x04 + exx * 8)
        self.add_byte(eyy + ezz * 8 + times * 0x20)

    def lea_exx_ptr_eyy_add_ezz_times_add_byte(self, exx, eyy, ezz, times, val):
        self.add_byte(0x8D)
        self.add_byte(0x44 + exx * 8)
        self.add_byte(eyy + ezz * 8 + times * 0x20)
        self.add_byte(val)

    def lea_exx_dword_ptr(self, exx, val):
        self.add_byte(0x8D)
        self.add_byte(0x05 + exx * 8)
        self.add_dword(val)

    def lea_exy_byte(self, exy, val):
        self.add_byte(0x8D)
        self.add_byte(exy)  # exx+(eyy)*8
        self.add_byte(val)

    def lea_exx_eyy_ezz_times(self, exx, eyy, ezz, times):
        self.add_byte(0x8D)
        self.add_byte(0x4 + exx * 8)
        self.add_byte(eyy + ezz * 8 + times * 0x20)

    def cmp_exx_byte(self, exx, val):
        self.add_byte(0x83)
        self.add_byte(0xF8 + exx)
        self.add_byte(val)

    def cmp_exx_dword(self, exx, val):
        if exx == EAX:
            self.add_byte(0x3D)
        else:
            self.add_byte(0x81)
            self.add_byte(0xF8 + exx)
        self.add_dword(val)

    def cmp_exx_eyy(self, exx, eyy):
        self.add_byte(0x39)
        self.add_byte(0xC0 + exx + eyy * 8)

    def cmp_exx_ptr_eyy_add_dword(self, exx, eyy, val):
        self.add_byte(0x3B)
        self.add_byte(0x80 + exx * 8 + eyy)
        self.add_dword(val)

    def cmp_ptr_exx_add_byte_eyy(self, exx, val, eyy):
        self.add_byte(0x39)
        self.add_byte(0x40 + exx + eyy * 8)
        self.add_byte(val)

    def cmp_dword_ptr_exx_add_byte_byte(self, exx, val, val2):
        self.add_byte(0x83)
        self.add_byte(0x78 + exx)
        if exx == ESP:
            self.add_byte(0x24)
        self.add_byte(val)
        self.add_byte(val2)

    def cmp_dword_ptr_exx_add_byte_dword(self, exx, val, val2):
        self.add_byte(0x81)
        self.add_byte(0x78 + exx)
        self.add_byte(val)
        self.add_dword(val2)

    def cmp_dword_ptr_exx_add_dword_byte(self, exx, val, val2):
        self.add_byte(0x83)
        self.add_byte(0xB8 + exx)
        self.add_dword(val)
        self.add_byte(val2)

    def cmp_byte_ptr_exx_add_byte_byte(self, exx, val, val2):
        self.add_byte(0x80)
        self.add_byte(0x78 + exx)
        self.add_byte(val)
        self.add_byte(val2)

    def cmp_byte_ptr_exx_add_dword_byte(self, exx, val, val2):
        self.add_byte(0x80)
        self.add_byte(0xB8 + exx)
        self.add_dword(val)
        self.add_byte(val2)

    def cmp_dword_ptr_address_byte(self, address, val):
        self.add_byte(0x83)
        self.add_byte(0x3D)
        self.add_dword(address)
        self.add_byte(val)

    def cmp_byte_ptr_address_byte(self, address, val):
        self.add_byte(0x80)
        self.add_byte(0x3D)
        self.add_dword(address)
        self.add_byte(val)

    def cmp_dword_ptr_address_dword(self, address, val):
        self.add_byte(0x81)
        self.add_byte(0x3D)
        self.add_dword(address)
        self.add_dword(val)

    def add_dword_ptr_address_byte(self, address, val):
        self.add_byte(0x83)
        self.add_byte(0x05)
        self.add_dword(address)
        self.add_byte(val)

    def sub_dword_ptr_address_byte(self, address, val):
        self.add_byte(0x83)
        self.add_byte(0x2D)
        self.add_dword(address)
        self.add_byte(val)

    def sub_exx_byte(self, exx, val):
        self.add_byte(0x83)
        self.add_byte(0xE8 + exx)
        self.add_byte(val)

    def sub_exx_dword(self, exx, val):
        self.add_byte(0x81)
        self.add_byte(0xE8 + exx)
        self.add_dword(val)

    def sub_exx_eyy(self, exx, eyy):
        self.add_byte(0x29)
        self.add_byte(0xC0 + exx + eyy * 8)

    def sub_exx_ptr_dword(self, exx, val):
        self.add_byte(0x2B)
        self.add_byte(0x05 + exx * 8)
        self.add_dword(val)

    def neg_exx(self, exx):
        self.add_byte(0xF7)
        self.add_byte(0xD8 + exx)

    def xor_exx_eyy(self, exx, eyy):
        self.add_byte(0x31)
        self.add_byte(0xC0 + exx + eyy * 8)

    def je(self, addr):
        # 计算相对偏移量，需要减去当前指令的长度（5字节）
        relative_offset = addr - (self.startAddress + self.index + 6)
        # 将相对偏移量转换为32位有符号整数的字节序列
        # 使用 int.to_bytes 方法，并指定字节长度为4，使用小端字节序
        # 使用 signed=True 来允许负数的转换
        offset_bytes = relative_offset.to_bytes(4, byteorder="little", signed=True)
        self.add_byte(0x0F)
        self.add_byte(0x84)
        self.code[self.index : self.index + 4] = offset_bytes
        self.index += 4

    def jmp(self, addr):
        relative_offset = addr - (self.startAddress + self.index + 5)
        # 将相对偏移量转换为32位有符号整数的字节序列
        # 使用 int.to_bytes 方法，并指定字节长度为4，使用小端字节序
        # 使用 signed=True 来允许负数的转换
        offset_bytes = relative_offset.to_bytes(4, byteorder="little", signed=True)
        self.add_byte(0xE9)
        self.code[self.index : self.index + 4] = offset_bytes
        self.index += 4

    def jng(self, addr):
        relative_offset = addr - (self.startAddress + self.index + 6)
        # 将相对偏移量转换为32位有符号整数的字节序列
        # 使用 int.to_bytes 方法，并指定字节长度为4，使用小端字节序
        # 使用 signed=True 来允许负数的转换
        offset_bytes = relative_offset.to_bytes(4, byteorder="little", signed=True)
        self.add_byte(0x0F)
        self.add_byte(0x8E)
        self.code[self.index : self.index + 4] = offset_bytes
        self.index += 4

    def random(self, val):  # 取小于val的随机数
        self.add_byte(0x0F)
        self.add_byte(0x31)  # rdtsc读取时间戳计数器的值到 EDX:EAX
        self.add_byte(0x31)
        self.add_byte(0xD2)  # xor edx, edx  ; 将 EDX 寄存器清零
        self.mov_exx(ECX, val)
        self.add_byte(0xF7)
        self.add_byte(0xF1)  # div ecx   EAX = EAX / ECX，EDX = EAX % ECX
        # 现在 EDX 寄存器中的值是0到val的随机数

    def idiv_ex(self, ex):
        self.add_byte(0x66)
        self.add_byte(0xF7)
        self.add_byte(0xF8 + ex)

    def mov_dword_ptr_dword(self, address, val):
        self.add_byte(0xC7)
        self.add_byte(0x05)
        self.add_dword(address)
        self.add_dword(val)

    def mov_dword_ptr_exx(self, address, exx):
        if exx == EAX:
            self.add_byte(0xA3)
            self.add_dword(address)
        else:
            self.add_byte(0x89)
            self.add_byte(0x5 + exx * 8)
            self.add_dword(address)

    def mov_byte_ptr_exx_add_byte_byte(self, exx, val, val2):
        self.add_byte(0xC6)
        self.add_byte(0x40 + exx)
        self.add_byte(val)
        self.add_byte(val2)

    def mov_byte_ptr_exx_add_dword_byte(self, exx, val, val2):
        self.add_byte(0xC6)
        self.add_byte(0x80 + exx)
        self.add_dword(val)
        self.add_byte(val2)

    def mov_dword_ptr_exx_add_dword_dowrd(self, exx, val, val2):
        self.add_byte(0xC7)
        self.add_byte(0x80 + exx)
        self.add_dword(val)
        self.add_dword(val2)

    def mov_byte_ptr_address_byte(self, address, val):
        self.add_byte(0xC6)
        self.add_byte(0x05)
        self.add_dword(address)
        self.add_byte(val)

    def mov_ptr_exx_dword(self, exx, val):
        self.add_byte(0xC7)
        self.add_byte(exx)
        if exx == ESP:
            self.add_byte(0x24)
        self.add_dword(val)

    def mov_ptr_exx_eyy(self, exx, eyy):
        self.add_byte(0x89)
        self.add_byte(0x00 + exx + eyy * 8)

    def mov_ptr_exx_add_byte_eyy(self, exx, val, eyy):
        self.add_byte(0x89)
        self.add_byte(0x40 + exx + eyy * 8)
        if exx == ESP:
            self.add_byte(0x24)
        self.add_byte(val)

    def mov_ptr_exx_add_dword_eyy(self, exx, val, eyy):
        self.add_byte(0x89)
        self.add_byte(0x80 + exx + eyy * 8)
        if exx == ESP:
            self.add_byte(0x24)
        self.add_dword(val)

    def mov_ptr_exx_add_byte_dword(self, exx, val, val2):
        self.add_byte(0xC7)
        self.add_byte(0x40 + exx)
        if exx == ESP:
            self.add_byte(0x24)
        self.add_byte(val)
        self.add_dword(val2)

    def mov_ptr_exx_add_eyy_times_add_byte_doword(self, exx, eyy, times, val, val2):
        self.add_byte(0xC7)
        self.add_byte(0x44)
        self.add_byte(exx + eyy * 8 + times * 0x20)
        self.add_byte(val)
        self.add_dword(val2)

    def mov_ptr_exx_add_dword_dword(self, exx, val, val2):
        self.add_byte(0xC7)
        self.add_byte(0x80 + exx)
        if exx == ESP:
            self.add_byte(0x24)
        self.add_dword(val)
        self.add_dword(val2)

    def mov_ptr_exx_add_byte_float(self, exx, val, val2):
        self.add_byte(0xC7)
        self.add_byte(0x40 + exx)
        if exx == ESP:
            self.add_byte(0x24)
        self.add_byte(val)
        self.code[self.index : self.index + 4] = struct.pack("f", val2)
        self.index += 4

    def mov_ptr_dword_dword(self, address, val):
        self.add_byte(0xC7)
        self.add_byte(0x05)
        self.add_dword(address)
        self.add_dword(val)

    def mov_ptr_dword_float(self, address, val):
        self.add_byte(0xC7)
        self.add_byte(0x05)
        self.add_dword(address)
        self.code[self.index : self.index + 4] = struct.pack("f", val)
        self.index += 4

    def mov_fs_offset_exx(self, offset, exx):
        self.add_byte(0x64)
        self.add_byte(0x89)
        self.add_byte(0x05 + exx * 8)
        self.add_dword(offset)

    def add_exx_byte(self, exx, val):
        self.add_byte(0x83)
        self.add_byte(0xC0 + exx)
        self.add_byte(val)

    def add_exx_eyy(self, exx, eyy):
        self.add_byte(0x01)
        self.add_byte(0xC0 + exx + eyy * 8)

    def add_exx_ptr_eyy(self, exx, eyy):
        self.add_byte(0x03)
        self.add_byte(exx * 8 + eyy)

    def je_short_offset(self, val):
        self.add_byte(0x74)
        self.add_byte(val)

    def jl_offset(self, val):
        self.add_byte(0x7C)
        self.add_byte(val)

    def jle_offset(self, val):
        self.add_byte(0x7E)
        self.add_byte(val)

    def jnl_offset(self, val):
        self.add_byte(0x7D)
        self.add_byte(val)

    def jne(self, address):
        relative_offset = address - (self.startAddress + self.index + 6)
        # 将相对偏移量转换为32位有符号整数的字节序列
        # 使用 int.to_bytes 方法，并指定字节长度为4，使用小端字节序
        # 使用 signed=True 来允许负数的转换
        offset_bytes = relative_offset.to_bytes(4, byteorder="little", signed=True)
        self.add_byte(0x0F)
        self.add_byte(0x85)
        self.code[self.index : self.index + 4] = offset_bytes
        self.index += 4

    def jne_short_offset(self, val):
        self.add_byte(0x75)
        self.add_byte(val)

    def ja_offset(self, val):
        self.add_byte(0x77)
        self.add_byte(val)

    def jb_offset(self, val):
        self.add_byte(0x72)
        self.add_byte(val)

    def jg_offset(self, val):
        self.add_byte(0x7F)
        self.add_byte(val)

    def jg_long_offset(self, val):
        self.add_byte(0x0F)
        self.add_byte(0x8F)
        self.add_dword(val)

    def jng_dword_offset(self, val):
        self.add_byte(0x0F)
        self.add_byte(0x8E)
        self.add_dword(val)

    def jmp_short_offset(self, val):
        self.add_byte(0xEB)
        self.add_byte(val)

    def xor_dword_ptr_address_val(self, address, val):
        self.add_byte(0x83)
        self.add_byte(0x35)
        self.add_dword(address)
        self.add_byte(val)

    def nop_6(self):
        self.add_byte(0x66)
        self.add_byte(0x0F)
        self.add_byte(0x1F)
        self.add_byte(0x44)
        self.add_byte(0x00)
        self.add_byte(0x00)

    def nop_4(self):
        self.add_byte(0x0F)
        self.add_byte(0x1F)
        self.add_byte(0x40)
        self.add_byte(0x00)

    def pushad(self):
        self.add_byte(0x60)

    def popad(self):
        self.add_byte(0x61)

    def and_eax_dword(self, val):
        self.add_byte(0x25)
        self.add_dword(val)

    def and_exx_byte(self, exx, val):
        self.add_byte(0x83)
        self.add_byte(0xE0 + exx)
        self.add_byte(val)

    def shl_exx_byte(self, exx, val):
        self.add_byte(0xC1)
        self.add_byte(0xE0 + exx)
        self.add_byte(val)

    def inc_exx(self, exx):
        self.add_byte(0x40 + exx)

    def test_8(self, x, y):
        self.add_byte(0x84)
        self.add_byte(0xC0 + x * 8 + y)

    def create_label(self, label):
        self.labels[label] = self.index
        # 如果有待回填的跳转指向这个标签，现在回填它们
        if label in self.pending_jumps:
            for jump_index in self.pending_jumps[label]:
                self.jmp_dword_offset_at(jump_index, self.index - jump_index - 5)
            del self.pending_jumps[label]  # 清除已回填的跳转
        if label in self.pending_jothers:
            for jump_index in self.pending_jothers[label]:
                self.jother_dword_offset_at(jump_index, self.index - jump_index - 6)
            del self.pending_jothers[label]  # 清除已回填的跳转
        if label in self.pending_leas:
            for jump_index in self.pending_leas[label]:
                self.lea_dword_at(jump_index, self.index + self.startAddress)
            del self.pending_leas[label]  # 清除已回填的跳转
        if label in self.pending_pushs:
            for jump_index in self.pending_pushs[label]:
                self.push_dword_at(jump_index, self.index + self.startAddress)
            del self.pending_pushs[label]

    def jmp_dword_offset(self, val):
        if val < 0:
            # 将负数转换为32位无符号整数的等效值
            val += 2**32
        self.add_byte(0xE9)
        self.add_dword(val)

    def jmp_label(self, label):
        if label in self.labels:
            # 如果标签已存在，直接计算偏移并跳转
            self.jmp_dword_offset(self.labels[label] - self.index - 5)
        else:
            # 如果标签不存在，记录跳转位置以便回填
            if label not in self.pending_jumps:
                self.pending_jumps[label] = []
            self.pending_jumps[label].append(self.index)
            self.jmp_dword_offset(0)  # 使用占位符偏移量

    def jmp_dword_offset_at(self, index, offset):
        self.code[index + 1 : index + 5] = offset.to_bytes(
            4, byteorder="little", signed=True
        )

    def jother_dword_offset_at(self, index, offset):
        self.code[index + 2 : index + 6] = offset.to_bytes(
            4, byteorder="little", signed=True
        )

    def je_offset(self, val):
        if val < 0:
            # 将负数转换为32位无符号整数的等效值
            val += 2**32
        self.add_byte(0x0F)
        self.add_byte(0x84)
        self.add_dword(val)

    def je_label(self, label):
        if label in self.labels:
            # 如果标签已存在，直接计算偏移并跳转
            self.je_offset(self.labels[label] - self.index - 6)
        else:
            # 如果标签不存在，记录跳转位置以便回填
            if label not in self.pending_jothers:
                self.pending_jothers[label] = []
            self.pending_jothers[label].append(self.index)
            self.je(0)  # 使用占位符偏移量

    def jl_long_offset(self, val):
        if val < 0:
            # 将负数转换为32位无符号整数的等效值
            val += 2**32
        self.add_byte(0x0F)
        self.add_byte(0x8C)
        self.add_dword(val)

    def jl_label(self, label):
        if label in self.labels:
            # 如果标签已存在，直接计算偏移并跳转
            self.jl_long_offset(self.labels[label] - self.index - 6)
        else:
            # 如果标签不存在，记录跳转位置以便回填
            if label not in self.pending_jothers:
                self.pending_jothers[label] = []
            self.pending_jothers[label].append(self.index)
            self.jl_long_offset(0)  # 使用占位符偏移量

    def jnl_long_offset(self, val):
        if val < 0:
            # 将负数转换为32位无符号整数的等效值
            val += 2**32
        self.add_byte(0x0F)
        self.add_byte(0x8D)
        self.add_dword(val)

    def jnl_label(self, label):
        if label in self.labels:
            # 如果标签已存在，直接计算偏移并跳转
            self.jnl_long_offset(self.labels[label] - self.index - 6)
        else:
            # 如果标签不存在，记录跳转位置以便回填
            if label not in self.pending_jothers:
                self.pending_jothers[label] = []
            self.pending_jothers[label].append(self.index)
            self.jnl_long_offset(0)  # 使用占位符偏移量

    def jne_long_offset(self, val):
        if val < 0:
            # 将负数转换为32位无符号整数的等效值
            val += 2**32
        self.add_byte(0x0F)
        self.add_byte(0x85)
        self.add_dword(val)

    def jne_label(self, label):
        if label in self.labels:
            # 如果标签已存在，直接计算偏移并跳转
            self.jne_long_offset(self.labels[label] - self.index - 6)
        else:
            # 如果标签不存在，记录跳转位置以便回填
            if label not in self.pending_jothers:
                self.pending_jothers[label] = []
            self.pending_jothers[label].append(self.index)
            self.jne_long_offset(0)  # 使用占位符偏移量

    def jae_long_offset(self, val):
        if val < 0:
            # 将负数转换为32位无符号整数的等效值
            val += 2**32
        self.add_byte(0x0F)
        self.add_byte(0x83)
        self.add_dword(val)

    def jae_label(self, label):
        if label in self.labels:
            # 如果标签已存在，直接计算偏移并跳转
            self.jae_long_offset(self.labels[label] - self.index - 6)
        else:
            # 如果标签不存在，记录跳转位置以便回填
            if label not in self.pending_jothers:
                self.pending_jothers[label] = []
            self.pending_jothers[label].append(self.index)
            self.jae_long_offset(0)

    def jbe_long_offset(self, val):
        if val < 0:
            # 将负数转换为32位无符号整数的等效值
            val += 2**32
        self.add_byte(0x0F)
        self.add_byte(0x86)
        self.add_dword(val)

    def jbe_label(self, label):
        if label in self.labels:
            # 如果标签已存在，直接计算偏移并跳转
            self.jbe_long_offset(self.labels[label] - self.index - 6)
        else:
            # 如果标签不存在，记录跳转位置以便回填
            if label not in self.pending_jothers:
                self.pending_jothers[label] = []
            self.pending_jothers[label].append(self.index)
            self.jbe_long_offset(0)

    def call_dword_offset(self, offset):
        if offset < 0:
            # 将负数转换为32位无符号整数的等效值
            offset += 2**32
        self.add_byte(0xE8)  # call 指令的操作码
        self.add_dword(offset)

    def call_label(self, label):
        if label in self.labels:
            # 如果标签已存在，直接计算偏移并跳转
            self.call_dword_offset(self.labels[label] - self.index - 5)
        else:
            # 如果标签不存在，记录跳转位置以便回填
            if label not in self.pending_jumps:
                self.pending_jumps[label] = []
            self.pending_jumps[label].append(self.index)
            self.call_dword_offset(0)  # 使用占位符偏移量

    def lea_exx_label_add_byte(self, exx, label, val):
        if label in self.labels:
            self.lea_exx_dword_ptr(exx, self.labels[label] + val)
        else:
            print("Label not found: %s" % label)
            if label not in self.pending_leas:
                self.pending_leas[label] = []
            self.pending_leas[label].append(self.index)
            self.lea_exx_dword_ptr(exx, val)  # 使用占位符偏移量

    def lea_dword_at(self, index, address):
        print(index, address)
        val = self.code[index + 2 : index + 6]
        int_val = int.from_bytes(val, "little")  # 使用 'little' 如果字节是小端序
        print(int_val)
        val2 = int_val + address
        print(val2)
        self.code[index + 2 : index + 6] = val2.to_bytes(4, byteorder="little")

    def push_label(self, label):
        if label in self.labels:
            self.push_dword(self.labels[label])
        else:
            if label not in self.pending_pushs:
                self.pending_pushs[label] = []
            self.pending_pushs[label].append(self.index)
            self.push_dword(0)  # 使用占位符偏移量

    def push_dword_at(self, index, address):
        val = self.code[index + 1 : index + 5]
        int_val = int.from_bytes(val, "little")  # 使用 'little' 如果字节是小端序
        val2 = int_val + address
        self.code[index + 1 : index + 5] = val2.to_bytes(4, byteorder="little")


def runThread(cla):
    process_handle = pymem.process.open(data.PVZ_pid)
    startAddress = pymem.memory.allocate_memory(process_handle, 65536)
    # print(hex(startAddress))
    asm = cla.creat_asm(startAddress + 1)
    shellcode = b"\x60" + bytes(asm.code[: asm.index]) + b"\x61\xc3"
    data.PVZ_memory.write_bytes(startAddress, shellcode, asm.index + 3)
    data.PVZ_memory.write_bytes(0x00552014, b"\xfe", 1)
    thread_h = pymem.ressources.kernel32.CreateRemoteThread(
        process_handle,
        ctypes.cast(0, pymem.ressources.structure.LPSECURITY_ATTRIBUTES),
        0,
        startAddress,
        0,
        0,
        ctypes.byref(ctypes.c_ulong(0)),
    )
    exit_code = ctypes.c_ulong()
    while 1:
        pymem.ressources.kernel32.GetExitCodeThread(thread_h, ctypes.byref(exit_code))
        if exit_code.value == 259:
            pass
        else:
            data.PVZ_memory.write_bytes(0x00552014, b"\xdb", 1)
            break
        time.sleep(0.001)
    pymem.memory.free_memory(process_handle, startAddress)
