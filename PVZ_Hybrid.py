import ctypes
import PVZ_data as data
import pymem.ressources.kernel32
import pymem.ressources.structure
import pymem.thread
import pymem.memory
from threading import Thread, Event
import random
import time
import PVZ_asm as asm

column1addr = None
column2addr = None
newmem_shovelpro = None
newmem_spoils = None
newmem_spoils2 = None
newmem_slotKey = None
newmem_setAllBullet = None
newmem_endlessCar = None
newmem_noHole = None
newmem_zombiebeanHpynotized = None
newmem_getZombieAddress = None
newmem_zombieAddress = None
newmem_autoCar = None
newmem_pauseProKey = None
newmem_drawTime = None
newmem_pause = None
newmem_draw = None
newmem_pauseFlag = None
newmem_setBulletSize = None
newmem_setBulletPosition = None
newmem_setPlantBullet = None


def calculate_call_address(ctypes_obj):
    """S
    计算函数调用地址
    """
    c_uint_obj = ctypes.c_uint(ctypes_obj)
    return ctypes.string_at(ctypes.addressof(c_uint_obj), ctypes.sizeof(c_uint_obj))


def getMap():
    try:
        map = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
            data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x554c)
        if (map == 0 or map == 1 or map == 10 or map == 13 or map == 15 or map == 16 or map == 18 or map == 19 or map == 21):
            return 5
        elif (map == 2 or map == 11 or map == 3 or map == 12 or map == 14 or map == 17 or map == 20 or map == 22 or map == 23):
            return 6
        else:
            return False
    except:
        return False


def getDifficult():
    difficultAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x428
    difficultValue = data.PVZ_memory.read_int(difficultAddr)
    if (difficultValue == -1):
        return 1
    if (difficultValue == 0):
        return 2
    if (difficultValue == 1):
        return 3


def setDifficult(difficult):
    difficultAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x428
    if (difficult == 1):
        data.PVZ_memory.write_int(difficultAddr, 4294967295)
    if (difficult == 2):
        data.PVZ_memory.write_int(difficultAddr, 0)
    if (difficult == 3):
        data.PVZ_memory.write_int(difficultAddr, 1)


def getState():
    try:
        game_state = data.PVZ_memory.read_int(
            data.PVZ_memory.read_int(data.baseAddress)+0x7fc)
        return game_state  # 1主菜单 2选局内  5帮助  7关卡选择
    except:
        return False


def backGround(f):
    if f:
        data.PVZ_memory.write_bytes(0x0054EBEF, b'\xc3', 1)
    else:
        data.PVZ_memory.write_bytes(0x0054EBEF, b'\x57', 1)


def overPlant(f):
    addr = int.from_bytes(data.PVZ_memory.read_bytes(0x40e2c2, 1)+data.PVZ_memory.read_bytes(
        0x40e2c1, 1)+data.PVZ_memory.read_bytes(0x40e2c0, 1)+data.PVZ_memory.read_bytes(0x40e2bf, 1))+0x40e2c3
    if f:
        data.PVZ_memory.write_bytes(0x00425634, b'\xeb\x1b\x0f\x1f\x00', 5)
        data.PVZ_memory.write_bytes(
            0x0040e3c6, b'\xe9\x94\x00\x00\x00\x0f\x1f\x00', 8)
        data.PVZ_memory.write_bytes(
            0x0040FE2D, b'\xe9\x22\x09\x00\x00\x0f\x1f', 7)
        data.PVZ_memory.write_bytes(
            0x0042a2d6, b'\xe9\xe2\x00\x00\x00\x0f\x1f\x00', 8)
        data.PVZ_memory.write_bytes(0x00438e3e, b'\xeb\x34\x66\x90', 4)
        data.PVZ_memory.write_bytes(
            0x0040e263, b'\x8b\x5c\x24\x24\xeb\x2a\x0f\x1f\x00', 9)
        data.PVZ_memory.write_bytes(
            addr, b'\x0f\x1f\x00\x8b\x4c\x24\x2c\x66\x0f\x1f\x44\x00\x00', 13)
    else:
        data.PVZ_memory.write_bytes(0x00425634, b'\x83\xf8\xff\x74\x18', 5)
        data.PVZ_memory.write_bytes(
            0x0040FE2D, b'\x85\xc0\x0f\x84\x1f\x09\x00', 7)
        data.PVZ_memory.write_bytes(
            0x0040e3c6, b'\x85\xdb\x0f\x84\x91\x00\x00\x00', 8)
        data.PVZ_memory.write_bytes(
            0x0042a2d6, b'\x85\xc0\x0f\x84\xdf\x00\x00\x00', 8)
        data.PVZ_memory.write_bytes(0x00438e3e, b'\x85\xc0\x74\x32', 4)
        data.PVZ_memory.write_bytes(
            0x0040e263, b'\x83\xf9\x03\x8b\x5c\x24\x24\x75\x27', 9)
        data.PVZ_memory.write_bytes(
            addr, b'\x83\xf9\x02\x8b\x4c\x24\x2c\x0f\x84'+calculate_call_address(0x0040e2cd-addr-0xd), 13)


def getSun():
    sunAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x5560
    sunNow = data.PVZ_memory.read_int(sunAddr)
    return sunNow


def addSun(sunIncrement):
    sunAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x5560
    sunNow = data.PVZ_memory.read_int(sunAddr)
    data.PVZ_memory.write_int(sunAddr, sunNow+int(sunIncrement))


def setSun(sun):
    sunAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x5560
    data.PVZ_memory.write_int(sunAddr, int(sun))


def getSilver():
    silverAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x208
    silverNow = data.PVZ_memory.read_int(silverAddr)
    return silverNow


def addSilver(silverIncrement):
    silverAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x208
    silverNow = data.PVZ_memory.read_int(silverAddr)
    data.PVZ_memory.write_int(silverAddr, silverNow+int(silverIncrement))


def setSilver(silver):
    silverAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x208
    data.PVZ_memory.write_int(silverAddr, int(silver))


def getGold():
    goldAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x20c
    goldNow = data.PVZ_memory.read_int(goldAddr)
    return goldNow


def addGold(goldIncrement):
    goldAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x20c
    goldNow = data.PVZ_memory.read_int(goldAddr)
    data.PVZ_memory.write_int(goldAddr, goldNow+int(goldIncrement))


def setGold(gold):
    goldAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x20c
    data.PVZ_memory.write_int(goldAddr, int(gold))


def getDiamond():
    diamondAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x210
    diamondNow = data.PVZ_memory.read_int(diamondAddr)
    return diamondNow


def addDiamond(diamondIncrement):
    diamondAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x210
    diamondNow = data.PVZ_memory.read_int(diamondAddr)
    data.PVZ_memory.write_int(diamondAddr, diamondNow+int(diamondIncrement))


def setDiamond(diamond):
    diamondAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x210
    data.PVZ_memory.write_int(diamondAddr, int(diamond))


def upperLimit(f):
    if f:
        data.PVZ_memory.write_bytes(0x00430A23, b'\xeb', 1)
        data.PVZ_memory.write_bytes(0x00430A78, b'\xeb', 1)
        data.PVZ_memory.write_bytes(0x0048CAB0, b'\xeb', 1)
    else:
        data.PVZ_memory.write_bytes(0x00430A23, b'\x7e', 1)
        data.PVZ_memory.write_bytes(0x00430A78, b'\x7e', 1)
        data.PVZ_memory.write_bytes(0x0048CAB0, b'\x7e', 1)


def pausePro(f):
    if f:
        data.PVZ_memory.write_bytes(
            0x415df0, b'\x0f\x1f\x80\x00\x00\x00\x00\x66\x90', 9)
    else:
        data.PVZ_memory.write_bytes(
            0x415df0, b'\x80\xbd\x64\x01\x00\x00\x00\x74\x35', 9)


def ignoreSun(f):
    if f:
        data.PVZ_memory.write_bytes(0x0041ba70, b'\x90\x90\x90\x90\x90\x90', 6)
        data.PVZ_memory.write_bytes(
            0x0048881B, b'\xe9\x97\x01\x00\x00\x0f\x1f\x00', 8)
        data.PVZ_memory.write_bytes(0x0048847f, b'\xeb', 1)
        data.PVZ_memory.write_bytes(0x0040f8a2, b'\xeb', 1)
        data.PVZ_memory.write_bytes(0x00488565, b'\xeb\x0e\x90\x90', 4)
    else:
        data.PVZ_memory.write_bytes(0x0041ba70, b'\x39\xc3\x7f\x0c\x29\xde', 6)
        data.PVZ_memory.write_bytes(
            0x0048881B, b'\x84\xc0\x0f\x85\x94\x01\x00\x00', 8)
        data.PVZ_memory.write_bytes(0x0048847f, b'\x75', 1)
        data.PVZ_memory.write_bytes(0x0040f8a2, b'\x75', 1)
        data.PVZ_memory.write_bytes(0x00488565, b'\x84\xc0\x75\x0c', 4)


def cancelCd(f):
    # if f:
    #     data.PVZ_memory.write_bytes(0x487293, b'\x3b\x47\x28\x90\x90', 5)
    # else:
    #     data.PVZ_memory.write_bytes(0x487296, b'\x7e\x14', 2)
    if f:
        data.PVZ_memory.write_bytes(0x487296, b'\x70', 1)
        data.PVZ_memory.write_bytes(0x00488250, b'\xeb', 1)
        data.PVZ_memory.write_bytes(0x00488E73, b'\xc6\x45\x48\x01', 4)
    else:
        data.PVZ_memory.write_bytes(0x487296, b'\x7e', 1)
        data.PVZ_memory.write_bytes(0x00488250, b'\x75', 1)
        data.PVZ_memory.write_bytes(0x00488E73, b'\xc6\x45\x48\x00', 4)


def killAllZombies():
    zomNum = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xa0)
    i = 0
    j = 0
    while i < zomNum:
        zomAddresss = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
            data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x90)+0x204*j
        zomExist = data.PVZ_memory.read_bytes(zomAddresss+0xec, 1)
        if (zomExist == b'\x00'):
            data.PVZ_memory.write_int(zomAddresss+0x28, 3)
            i = i+1
        j = j+1


def autoCollect(f):
    if f:
        data.PVZ_memory.write_bytes(0x43158B, b'\x80\x7B\x50\x00\xEB\x08', 6)
    else:
        data.PVZ_memory.write_bytes(0x43158B, b'\x80\x7B\x50\x00\x75\x08', 6)


def changeSlot(n, type):
    slotAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x144
    data.PVZ_memory.write_int(
        data.PVZ_memory.read_int(slotAddr)+0x5c+0x50*(n-1), type)


def win():
    winAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x55fc
    data.PVZ_memory.write_int(winAddr, 1)


def advacedPause(f):
    if f:
        data.PVZ_memory.write_bytes(
            0x415df0, b'\x0f\x1f\x80\x00\x00\x00\x00\x66\x90', 9)
    else:
        data.PVZ_memory.write_bytes(
            0x415df0, b'\x80\xbd\x64\x01\x00\x00\x00\x74\x35', 9)


def column(f):
    global column1addr
    global column2addr
    if f:
        column1addr = data.PVZ_memory.read_bytes(0x00410adf, 5)
        column2addr = data.PVZ_memory.read_bytes(0x00439035, 5)
        data.PVZ_memory.write_bytes(0x00410adf, b'\xeb\x0b\x90\x90\x90', 5)
        data.PVZ_memory.write_bytes(0x00439035, b'\xeb\x0b\x90\x90\x90', 5)
    else:
        data.PVZ_memory.write_bytes(0x00410adf, column1addr, 5)
        data.PVZ_memory.write_bytes(0x00439035, column2addr, 5)


def unlock():
    addr = int.from_bytes(data.PVZ_memory.read_bytes(0x00453B24, 1)+data.PVZ_memory.read_bytes(0x00453B23, 1) +
                          data.PVZ_memory.read_bytes(0x00453B22, 1)+data.PVZ_memory.read_bytes(0x00453B21, 1))+0x00453B25
    newmem_unlock = pymem.memory.allocate_memory(
        data.PVZ_memory.process_handle, 128)
    shellcode = asm.Asm(newmem_unlock)
    shellcode.push_exx(asm.ESI)
    shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ESI, asm.EDI, 0x82c)
    shellcode.mov_ptr_exx_add_dowrd_dword(asm.ESI, 0x1c0, 1)
    shellcode.pop_exx(asm.ESI)
    shellcode.add_byte(0xb0)
    shellcode.add_byte(0x01)  # mov al,01
    shellcode.ret()
    shellcode.jmp(0x00840a77)

    data.PVZ_memory.write_bytes(newmem_unlock, bytes(
        shellcode.code[:shellcode.index]), shellcode.index)
    data.PVZ_memory.write_bytes(
        addr, b'\xe9'+calculate_call_address(newmem_unlock-addr-5)+b'\x90\x90', 7)


def shovelpro(f):
    global newmem_shovelpro
    addr = int.from_bytes(data.PVZ_memory.read_bytes(0x411141, 1)+data.PVZ_memory.read_bytes(0x411140, 1) +
                          data.PVZ_memory.read_bytes(0x41113f, 1)+data.PVZ_memory.read_bytes(0x41113e, 1))+0x411142
    print(hex(addr))
    if f:
        data.PVZ_memory.write_bytes(
            addr+0x15, b'\xeb\x6a\x90', 3)
        newmem_shovelpro = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 100)
        print(hex(newmem_shovelpro))
        byte_data = (
            b'\x60\x8b\x45\x24\x8b\x7d\x04\xba\xff\xff\xff\xff\xe8'
            + calculate_call_address(0x0041dae0-newmem_shovelpro-0x11) +
            b'\x01\x85\x2c\x01\x00\x00\x61\x83\xbd\x2c\x01\x00\x00\x32\x7c\x1d\x83\xad\x2c\x01\x00\x00\x32'
            b'\x60\x8b\x4d\x04\x6a\x02\x6a\x06\xff\x75\x0c\xff\x75\x08\xe8'
            + calculate_call_address(0x0040cb10-newmem_shovelpro-0x3b) +
            b'\x61\xeb\xda\x83\xbd\x2c\x01\x00\x00\x19\x7c\x1d\x83\xad\x2c\x01\x00\x00\x19\x60\x8b\x4d\x04'
            b'\x6a\x02\x6a\x04\xff\x75\x0c\xff\x75\x08\xe8'
            + calculate_call_address(0x0040cb10-newmem_shovelpro-0x61) +
            b'\x61\xeb\xb4\x83\xbd\x2c\x01\x00\x00\x0f\x7c\x1d\x83\xad\x2c\x01\x00\x00\x0f\x60\x8b\x4d\x04'
            b'\x6a\x02\x6a\x05\xff\x75\x0c\xff\x75\x08\xe8'
            + calculate_call_address(0x0040cb10-newmem_shovelpro-0x87) +
            b'\x61\xeb\x8e\x01\x9f\x9c\x57\x00\x00\xe9'
            + calculate_call_address(0x004111de-newmem_shovelpro-0x95)
        )
        data.PVZ_memory.write_bytes(newmem_shovelpro, byte_data, 149)
        data.PVZ_memory.write_bytes(
            0x004111d8, b'\xe9'+calculate_call_address(newmem_shovelpro-0x004111dd)+b'\x90', 6)
    else:
        data.PVZ_memory.write_bytes(
            addr+0x15, b'\x83\xf8\x17', 3)
        data.PVZ_memory.write_bytes(0x004111d8, b'\x01\x9f\x9c\x57\x00\x00', 6)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_shovelpro)


def randomSlots_operstion(randomSlots_event):
    while not randomSlots_event.is_set():
        plant1addr = data.PVZ_memory.read_int(
            data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x144
        for i in range(0, 14):
            plant = random.randint(0, 86)
            if (plant >= 48):
                plant = plant+27
            data.PVZ_memory.write_int(
                data.PVZ_memory.read_int(plant1addr)+0x5c+0x50*i, plant)


randomSlots_event = Event()
randomSlots_thread = None


def randomSlots(f):
    global randomSlots_thread
    if (f):
        if not randomSlots_thread or not randomSlots_thread.is_alive():
            randomSlots_event.clear()
            randomSlots_thread = Thread(
                target=randomSlots_operstion, args=(randomSlots_event,))
            randomSlots_thread.start()
    else:
        # 设置事件标志，通知线程停止
        randomSlots_event.set()
        randomSlots_thread.join()  # 等待线程结束


def ignoreZombies(f):
    if f:
        data.PVZ_memory.write_bytes(0x413431, b'\xe9\x7f\x04\x00\x00\x90', 6)
    else:
        data.PVZ_memory.write_bytes(0x413431, b'\x0f\x84\x7f\x04\x00\x00', 6)


def pauseSpawn(f):
    if f:
        data.PVZ_memory.write_bytes(0x004265DC, b'\xeb', 1)
    else:
        data.PVZ_memory.write_bytes(0x004265DC, b'\x74', 1)


def changeGameSpeed(s):
    FrameDurationAddr = data.PVZ_memory.read_int(data.baseAddress)+0x454
    if (s == 0):
        data.PVZ_memory.write_int(FrameDurationAddr, 10)
        data.PVZ_memory.write_bytes(0x6A9EAA, b'\x01', 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b'\x00', 1)
    elif (s == 1):
        data.PVZ_memory.write_int(FrameDurationAddr, 20)
        data.PVZ_memory.write_bytes(0x6A9EAA, b'\x00', 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b'\x00', 1)
    elif (s == 2):
        data.PVZ_memory.write_int(FrameDurationAddr, 10)
        data.PVZ_memory.write_bytes(0x6A9EAA, b'\x00', 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b'\x00', 1)
    elif (s == 3):
        data.PVZ_memory.write_int(FrameDurationAddr, 5)
        data.PVZ_memory.write_bytes(0x6A9EAA, b'\x00', 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b'\x00', 1)
    elif (s == 4):
        data.PVZ_memory.write_int(FrameDurationAddr, 2)
        data.PVZ_memory.write_bytes(0x6A9EAA, b'\x00', 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b'\x00', 1)
    elif (s == 5):
        data.PVZ_memory.write_int(FrameDurationAddr, 1)
        data.PVZ_memory.write_bytes(0x6A9EAA, b'\x00', 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b'\x00', 1)
    elif (s == 6):
        data.PVZ_memory.write_int(FrameDurationAddr, 10)
        data.PVZ_memory.write_bytes(0x6A9EAA, b'\x00', 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b'\x01', 1)


def completeAdvanture(level):
    advantureAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x42c
    data.PVZ_memory.write_int(advantureAddr+level*4, 1)


def lockAdvanture(level):
    advantureAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x42c
    data.PVZ_memory.write_int(advantureAddr+level*4, 0)


def completeChallenge(level):
    challengeAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x82c
    data.PVZ_memory.write_int(challengeAddr+level*4, 1)


def lockChallenge(level):
    challengeAddr = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.baseAddress)+0x82c)+0x82c
    data.PVZ_memory.write_int(challengeAddr+level*4, 0)


def noHole(d, t, b):
    global newmem_noHole
    if (d and not b and not t):
        data.PVZ_memory.write_bytes(0x00466668, b'\x90\x90\xeb\x2e', 4)

        newmem_noHole = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 0)
        shellcode.jne_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xff)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(newmem_noHole, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
        data.PVZ_memory.write_bytes(
            0x0041D790, b'\xe9'+calculate_call_address(newmem_noHole-0x0041D795)+b'\x90\x90\x90\x90\x90', 10)
    if (d and b and not t):
        data.PVZ_memory.write_bytes(0x00466668, b'\x90\x90\xeb\x2e', 4)

        newmem_noHole = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 2)
        shellcode.je_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xff)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(newmem_noHole, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
        data.PVZ_memory.write_bytes(
            0x0041D790, b'\xe9'+calculate_call_address(newmem_noHole-0x0041D795)+b'\x90\x90\x90\x90\x90', 10)
    if (d and b and t):
        data.PVZ_memory.write_bytes(0x00466668, b'\x90\x90\xeb\x2e', 4)

        newmem_noHole = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 0)
        shellcode.add_byte(0x90)
        shellcode.add_byte(0x90)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xff)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(newmem_noHole, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
        data.PVZ_memory.write_bytes(
            0x0041D790, b'\xe9'+calculate_call_address(newmem_noHole-0x0041D795)+b'\x90\x90\x90\x90\x90', 10)
    if (not d and b and not t):
        data.PVZ_memory.write_bytes(0x00466668, b'\x90\x90\xeb\x2e', 4)

        newmem_noHole = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 1)
        shellcode.jne_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xff)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(newmem_noHole, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
        data.PVZ_memory.write_bytes(
            0x0041D790, b'\xe9'+calculate_call_address(newmem_noHole-0x0041D795)+b'\x90\x90\x90\x90\x90', 10)
    if (not d and b and t):
        data.PVZ_memory.write_bytes(0x00466668, b'\x90\x90\xeb\x2e', 4)

        newmem_noHole = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 0)
        shellcode.je_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xff)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(newmem_noHole, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
        data.PVZ_memory.write_bytes(
            0x0041D790, b'\xe9'+calculate_call_address(newmem_noHole-0x0041D795)+b'\x90\x90\x90\x90\x90', 10)
    if (not d and not b and t):
        data.PVZ_memory.write_bytes(0x00466668, b'\x90\x90\xeb\x2e', 4)

        newmem_noHole = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 2)
        shellcode.jne_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xff)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(newmem_noHole, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
        data.PVZ_memory.write_bytes(
            0x0041D790, b'\xe9'+calculate_call_address(newmem_noHole-0x0041D795)+b'\x90\x90\x90\x90\x90', 10)
    if (d and not b and t):
        data.PVZ_memory.write_bytes(0x00466668, b'\x90\x90\xeb\x2e', 4)

        newmem_noHole = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 1)
        shellcode.je_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xff)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(newmem_noHole, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
        data.PVZ_memory.write_bytes(
            0x0041D790, b'\xe9'+calculate_call_address(newmem_noHole-0x0041D795)+b'\x90\x90\x90\x90\x90', 10)
    if (not d and not b and not t):
        data.PVZ_memory.write_bytes(0x00466668, b'\x84\xc0\x74\x2e', 4)
        data.PVZ_memory.write_bytes(
            0x0041D790, b'\x83\x7e\x18\x00\x7e\x08\x83\x46\x18\xff', 10)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_noHole)


def zombiebeanHpynotized(f):
    global newmem_zombiebeanHpynotized
    global newmem_getZombieAddress
    global newmem_zombieAddress
    if f:
        newmem_zombiebeanHpynotized = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        newmem_getZombieAddress = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        newmem_zombieAddress = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 4)
        shellcode = asm.Asm(newmem_getZombieAddress)
        shellcode.mov_dword_ptr_exx(newmem_zombieAddress, asm.EDI)
        shellcode.push_dword(0x204)
        shellcode.jmp(0x0041DDDA)
        data.PVZ_memory.write_bytes(newmem_getZombieAddress, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
        data.PVZ_memory.write_bytes(
            0x0041DDD5, b'\xe9'+calculate_call_address(newmem_getZombieAddress-0x0041DDDA), 5)

        shellcode1 = asm.Asm(newmem_zombiebeanHpynotized)
        shellcode1.push_exx(asm.EAX)
        shellcode1.mov_exx_dword_ptr(asm.EAX, newmem_zombieAddress)
        shellcode1.cmp_dword_ptr_exx_add_byte_byte(asm.EAX, 0x24, 0x8)
        shellcode1.jne_offset(4)
        shellcode1.mov_byte_ptr_exx_add_byte_byte(asm.EAX, 0x51, 1)
        shellcode1.mov_byte_ptr_exx_add_dword_byte(asm.EAX, 0xb8, 1)
        shellcode1.pop_exx(asm.EAX)
        shellcode1.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EBP, 0x138)
        shellcode1.jmp(0x0084F5E9)
        data.PVZ_memory.write_bytes(newmem_zombiebeanHpynotized, bytes(
            shellcode1.code[:shellcode1.index]), shellcode1.index)
        data.PVZ_memory.write_bytes(
            0x0084F5E3, b'\xe9'+calculate_call_address(newmem_zombiebeanHpynotized-0x0084F5E8)+b'\x90', 6)

    else:
        data.PVZ_memory.write_bytes(0x0041DDD5, b'\x68\x04\x02\x00\x00', 5)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_getZombieAddress)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_zombieAddress)
        data.PVZ_memory.write_bytes(0x0084F5E3, b'\x8b\x85\x38\x01\x00\x00', 6)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_zombiebeanHpynotized)


def conveyorBeltFull(f):
    if f:
        data.PVZ_memory.write_bytes(0x00422D1F, b'\x0f\x80', 2)
        data.PVZ_memory.write_bytes(0x00489CA1, b'\x33\xc0', 2)
    else:
        data.PVZ_memory.write_bytes(0x00422D1F, b'\x0f\x8f', 2)
        data.PVZ_memory.write_bytes(0x00489CA1, b'\x85\xc0', 2)


def getEndlessRound():
    try:
        endlessRoundAddr = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
            data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x160)+0x6c
        return data.PVZ_memory.read_int(endlessRoundAddr)
    except:
        return '未知'


def setEndlessRound(endlessRound):
    try:
        endlessRoundAddr = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
            data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x160)+0x6c
        data.PVZ_memory.write_int(endlessRoundAddr, endlessRound)
    except:
        return


def putLadder(row, col):
    class ladder:
        def __init__(self, row, col):
            self.row = row
            self.col = col

        def creat_asm(self, startAddress):
            ladder_asm = asm.Asm(startAddress)
            ladder_asm.mov_exx_dword_ptr(asm.EAX, 0x006a9ec0)
            ladder_asm.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x768)
            ladder_asm.mov_exx(asm.EDI, self.row)
            ladder_asm.push_byte(self.col)
            ladder_asm.call(0x00408f40)
            return ladder_asm

    asm.runThread(ladder(row, col))


def putZombie(row, col, type):
    class zombiePut:
        def __init__(self, row, col, type):
            self.row = row
            self.col = col
            self.type = type

        def creat_asm(self, startAddress):
            zombiePut_asm = asm.Asm(startAddress)
            zombiePut_asm.push_byte(self.col)
            zombiePut_asm.push_byte(self.type)
            zombiePut_asm.mov_exx(asm.EAX, self.row)
            zombiePut_asm.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
            zombiePut_asm.mov_exx_dword_ptr_eyy_add_dword(
                asm.ECX, asm.ECX, 0x768)
            zombiePut_asm.mov_exx_dword_ptr_eyy_add_dword(
                asm.ECX, asm.ECX, 0x160)
            zombiePut_asm.call(0x0042a0f0)
            return zombiePut_asm

    asm.runThread(zombiePut(row, col, type))


def putBoss(row, col, type):
    class bossPut:
        def __init__(self, row, col, type):
            self.row = row
            self.col = col
            self.type = type

        def creat_asm(self, startAddress):
            bossPut_asm = asm.Asm(startAddress)
            bossPut_asm.mov_exx_dword_ptr(asm.EAX, 0x006a9ec0)
            bossPut_asm.mov_exx_dword_ptr_eyy_add_dword(
                asm.EAX, asm.EAX,  0x768)
            bossPut_asm.push_byte(0)
            bossPut_asm.push_byte(25)
            bossPut_asm.call(0x0040ddc0)
            return bossPut_asm

    asm.runThread(bossPut(row, col, type))


def putPlant(row, col, type):
    class plautPut:
        def __init__(self, row, col, type):
            self.row = row
            self.col = col
            self.type = type

        def creat_asm(self, startAddress):
            plantPut_asm = asm.Asm(startAddress)
            plantPut_asm.push_byte(255)
            plantPut_asm.push_byte(self.type)
            plantPut_asm.mov_exx(asm.EAX, self.row)
            plantPut_asm.push_byte(self.col)
            plantPut_asm.mov_exx_dword_ptr(asm.EBP, 0x006a9ec0)
            plantPut_asm.mov_exx_dword_ptr_eyy_add_dword(
                asm.EBP, asm.EBP, 0x768)
            plantPut_asm.push_exx(asm.EBP)
            plantPut_asm.call(0x0040d120)
            return plantPut_asm

    asm.runThread(plautPut(row, col, type))


def selectCard(type):
    class cardSelect:
        def __init__(self, type):
            self.type = type

        def creat_asm(self, startAddress):
            cardSelect_asm = asm.Asm(startAddress)
            cardSelect_asm.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
            cardSelect_asm.mov_exx_dword_ptr_eyy_add_dword(
                asm.ESI, asm.EAX, 0x00000774)
            cardSelect_asm.mov_exx(asm.EBX, self.type)
            cardSelect_asm.imul_exx_eyy_byte(asm.EDX, asm.EBX, 0xf)
            cardSelect_asm.lea_exx_byte_dword(asm.EAX, 0x96, 0xa4)
            cardSelect_asm.push_exx(asm.EAX)
            cardSelect_asm.mov_exx_eyy(asm.EAX, asm.ESI)
            cardSelect_asm.call(0x00486030)
            return cardSelect_asm

    asm.runThread(cardSelect(type))


def deselectCard(type):
    class cardDeselect:
        def __init__(self, type):
            self.type = type

        def creat_asm(self, startAddress):
            cardDeselect_asm = asm.Asm(startAddress)
            cardDeselect_asm.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
            cardDeselect_asm.mov_exx_dword_ptr_eyy_add_dword(
                asm.ESI, asm.EAX, 0x00000774)
            cardDeselect_asm.mov_exx(asm.EBX, self.type)
            cardDeselect_asm.imul_exx_eyy_byte(asm.EDX, asm.EBX, 0xf)
            cardDeselect_asm.lea_exx_byte_dword(asm.EAX, 0x96, 0xa4)
            cardDeselect_asm.push_exx(asm.EAX)
            cardDeselect_asm.mov_exx_eyy(asm.EAX, asm.ESI)
            cardDeselect_asm.call(0x00485E90)
            return cardDeselect_asm

    asm.runThread(cardDeselect(type))


def defeat():
    class Defeat:
        def __init__(self) -> None:
            pass

        def creat_asm(self, startAddress):
            Defeat_asm = asm.Asm(startAddress)
            Defeat_asm.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
            Defeat_asm.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x768)
            Defeat_asm.mov_exx_dword_ptr_eyy_add_dword(asm.ESI, asm.EAX, 0x90)
            Defeat_asm.mov_exx_dword_ptr_eyy(asm.EBX, asm.ESI)
            Defeat_asm.mov_exx(asm.EDX, 0x2d)
            Defeat_asm.mov_exx_eyy(asm.ECX, asm.ESI)
            Defeat_asm.mov_exx(asm.EDI, 0xFFFFFF9C)
            Defeat_asm.mov_exx_dword_ptr_eyy_add_byte(asm.EAX, asm.ESI, 0x04)
            Defeat_asm.push_exx(asm.ESI)
            Defeat_asm.push_exx(asm.EAX)
            Defeat_asm.call(0x413400)
            return Defeat_asm

    asm.justRunThread(Defeat())


def noSlot_operstion(noSlot_event):
    while not noSlot_event.is_set():
        try:
            start = data.PVZ_memory.read_bool(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x774)+0x88)+0x1a)
            if start == True:
                data.PVZ_memory.write_bool(data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                    data.PVZ_memory.read_int(data.baseAddress)+0x774)+0x88)+0x1a, False)
        except:
            pass
        time.sleep(1)


noSlot_event = Event()
noSlot_thread = None


def noSolt(f):
    global noSlot_thread
    if f:
        if not noSlot_thread or not noSlot_thread.is_alive():
            noSlot_event.clear()
            noSlot_thread = Thread(
                target=noSlot_operstion, args=(noSlot_event,))
            noSlot_thread.start()
    else:
        # 设置事件标志，通知线程停止
        noSlot_event.set()
        noSlot_thread.join()  # 等待线程结束


def save():
    class Save:
        def __init__(self) -> None:
            pass

        def creat_asm(self, startAddress):
            Save_asm = asm.Asm(startAddress)
            Save_asm.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
            Save_asm.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
            Save_asm.push_exx(asm.ECX)
            Save_asm.call(0x408c30)
            return Save_asm

    asm.runThread(Save())


def load():
    class Load:
        def __init__(self) -> None:
            pass

        def creat_asm(self, startAddress):
            Load_asm = asm.Asm(startAddress)
            Load_asm.mov_exx_dword_ptr(asm.ESI, 0x006A9EC0)
            Load_asm.push_exx(asm.ESI)
            Load_asm.call(0x44f7a0)
            return Load_asm

    asm.runThread(Load())


def spoils(spoils_config):
    global newmem_spoils
    global newmem_spoils2
    print(spoils_config)
    if (spoils_config != False):
        data.PVZ_memory.write_bytes(0x00530275, b'\x70', 1)
        newmem_spoils = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256)
        newmem_spoils2 = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 32)
        print(hex(newmem_spoils))
        print(hex(newmem_spoils2))
        shellcode = asm.Asm(newmem_spoils)
        shellcode.mov_exx_dword_ptr_eyy(asm.EAX, asm.EBX)
        shellcode.mov_exx(asm.ESI, 4)
        shellcode.call(0x00453630)
        if (len(spoils_config) > 0):
            shellcode.random(100)
            shellcode.cmp_exx_byte(asm.EDX, spoils_config[0]["percent"])
            shellcode.add_byte(0x72)  # jb
            shellcode.add_byte(0x05)  # 小于则后移5位
            shellcode.add_byte(0xe9)  # 大于则jmp
            shellcode.add_dword(0x1f)
            shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ESI, asm.ESP, 0x0c)
            shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ECX, asm.EBX, 0x04)
            shellcode.push_byte(0x03)
            if (spoils_config[0]["type"] <= 6):
                shellcode.push_byte(spoils_config[0]["type"])
            elif (spoils_config[0]["type"] == 7):
                shellcode.push_byte(0x8)
            elif (spoils_config[0]["type"] == 8):
                shellcode.push_byte(0xf)
            elif (spoils_config[0]["type"] == 9):
                shellcode.push_byte(0x10)
            elif (spoils_config[0]["type"] == 10):
                shellcode.push_byte(0x12)
            if (spoils_config[0]["card"] == -1):
                shellcode.mov_dword_ptr_dword(0x00751EC0, 0)
            else:
                shellcode.mov_dword_ptr_dword(
                    0x00751EC0, spoils_config[0]["card"])
            shellcode.push_exx(asm.ESI)
            shellcode.lea_exy_byte(0x47, 0xec)
            shellcode.push_exx(asm.EAX)
            shellcode.call(0x0040CB10)
            if (len(spoils_config) > 1):
                shellcode.random(100)
                shellcode.cmp_exx_byte(asm.EDX, spoils_config[1]["percent"])
                shellcode.add_byte(0x72)  # jb
                shellcode.add_byte(0x05)  # 小于则后移5位
                shellcode.add_byte(0xe9)  # 大于则jmp
                shellcode.add_dword(0x1b)
                shellcode.push_byte(0x03)
                if (spoils_config[1]["type"] <= 6):
                    shellcode.push_byte(spoils_config[1]["type"])
                elif (spoils_config[1]["type"] == 7):
                    shellcode.push_byte(0x8)
                elif (spoils_config[1]["type"] == 8):
                    shellcode.push_byte(0xf)
                elif (spoils_config[1]["type"] == 9):
                    shellcode.push_byte(0x10)
                elif (spoils_config[1]["type"] == 10):
                    shellcode.push_byte(0x12)
                if (spoils_config[1]["card"] == -1):
                    shellcode.mov_dword_ptr_dword(0x00751EC0, 0)
                else:
                    shellcode.mov_dword_ptr_dword(
                        0x00751EC0, spoils_config[1]["card"])
                shellcode.push_exx(asm.ESI)
                shellcode.lea_exy_byte(0x4f, 0xe2)
                shellcode.push_exx(asm.ECX)
                shellcode.mov_exx_dword_ptr_eyy_add_byte(
                    asm.ECX, asm.EBX, 0x04)
                shellcode.call(0x0040CB10)
                if (len(spoils_config) > 2):
                    shellcode.random(100)
                    shellcode.cmp_exx_byte(
                        asm.EDX, spoils_config[2]["percent"])
                    shellcode.add_byte(0x72)  # jb
                    shellcode.add_byte(0x05)  # 小于则后移5位
                    shellcode.add_byte(0xe9)  # 大于则jmp
                    shellcode.add_dword(0x1b)
                    shellcode.mov_exx_dword_ptr_eyy_add_byte(
                        asm.ECX, asm.EBX, 0x04)
                    shellcode.push_byte(0x03)
                    if (spoils_config[2]["type"] <= 6):
                        shellcode.push_byte(spoils_config[2]["type"])
                    elif (spoils_config[2]["type"] == 7):
                        shellcode.push_byte(0x8)
                    elif (spoils_config[2]["type"] == 8):
                        shellcode.push_byte(0xf)
                    elif (spoils_config[2]["type"] == 9):
                        shellcode.push_byte(0x10)
                    elif (spoils_config[2]["type"] == 10):
                        shellcode.push_byte(0x12)
                    if (spoils_config[2]["card"] == -1):
                        shellcode.mov_dword_ptr_dword(0x00751EC0, 0)
                    else:
                        shellcode.mov_dword_ptr_dword(
                            0x00751EC0, spoils_config[2]["card"])
                    shellcode.push_exx(asm.ESI)
                    shellcode.lea_exy_byte(0x57, 0xd8)
                    shellcode.push_exx(asm.EDX)
                    shellcode.call(0x0040CB10)
                    if (len(spoils_config) > 3):
                        shellcode.random(100)
                        shellcode.cmp_exx_byte(
                            asm.EDX, spoils_config[3]["percent"])
                        shellcode.add_byte(0x72)  # jb
                        shellcode.add_byte(0x05)  # 小于则后移5位
                        shellcode.add_byte(0xe9)  # 大于则jmp
                        shellcode.add_dword(0x1b)
                        shellcode.mov_exx_dword_ptr_eyy_add_byte(
                            asm.ECX, asm.EBX, 0x04)
                        shellcode.push_byte(0x03)
                        if (spoils_config[3]["type"] <= 6):
                            shellcode.push_byte(spoils_config[2]["type"])
                        elif (spoils_config[3]["type"] == 7):
                            shellcode.push_byte(0x8)
                        elif (spoils_config[3]["type"] == 8):
                            shellcode.push_byte(0xf)
                        elif (spoils_config[3]["type"] == 9):
                            shellcode.push_byte(0x10)
                        elif (spoils_config[3]["type"] == 10):
                            shellcode.push_byte(0x12)
                        if (spoils_config[3]["card"] == -1):
                            shellcode.mov_dword_ptr_dword(0x00751EC0, 0)
                        else:
                            shellcode.mov_dword_ptr_dword(
                                0x00751EC0, spoils_config[3]["card"])
                        shellcode.push_exx(asm.ESI)
                        shellcode.add_exx_byte(asm.EDI, 0xce)
                        shellcode.push_exx(asm.EDI)
                        shellcode.call(0x0040CB10)
            shellcode.pop_exx(asm.EDI)
            shellcode.pop_exx(asm.ESI)
            shellcode.pop_exx(asm.EBX)
            shellcode.mov_exx_eyy(asm.ESP, asm.EBP)
            shellcode.pop_exx(asm.EBP)
            shellcode.ret()
            shellcode.jmp(0x005302D2)

        tempcode = asm.Asm(newmem_spoils2)
        tempcode.mov_exx_dword_ptr(asm.EAX, 0x00751EC0)
        tempcode.add_byte(0x89)
        tempcode.add_byte(0x45)
        tempcode.add_byte(0x68)
        tempcode.jmp(0x0042FFBD)

        data.PVZ_memory.write_bytes(newmem_spoils2, bytes(
            tempcode.code[:tempcode.index]), tempcode.index)
        data.PVZ_memory.write_bytes(
            0x42ffb6, b'\xe9'+calculate_call_address(newmem_spoils2-0x0042ffbb)+b'\x66\x90', 7)
        data.PVZ_memory.write_bytes(newmem_spoils, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
        data.PVZ_memory.write_bytes(
            0x00530277, b'\xe9'+calculate_call_address(newmem_spoils-0x0053027c), 5)
    else:
        data.PVZ_memory.write_bytes(0x00530275, b'\x75', 1)
        data.PVZ_memory.write_bytes(
            0x42ffb6, b'\xc7\x45\x68\x00\x00\x00\x00', 7)
        data.PVZ_memory.write_bytes(0x00530277, b'\x8b\x03\xbe\x04\x00', 5)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_spoils)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_spoils2)


def slotKey(slot_key_list):
    if (slot_key_list != False):
        global newmem_slotKey
        print(slot_key_list)
        newmem_slotKey = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 2048)
        print(hex(newmem_slotKey))
        shellcode = asm.Asm(newmem_slotKey)
        shellcode.pushad()
        if (slot_key_list["1"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["1"]])
            shellcode.je_offset(0xcc)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["2"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["2"]])
            shellcode.je_offset(0xcc+0x56)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["3"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["3"]])
            shellcode.je_offset(0xcc+0x56*2)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["4"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["4"]])
            shellcode.je_offset(0xcc+0x56*3)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["5"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["5"]])
            shellcode.je_offset(0xcc+0x56*4)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["6"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["6"]])
            shellcode.je_offset(0xcc+0x56*5)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["7"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["7"]])
            shellcode.je_offset(0xcc+0x56*6)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["8"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["8"]])
            shellcode.je_offset(0xcc+0x56*7)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["9"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["9"]])
            shellcode.je_offset(0xcc+0x56*8)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["10"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["10"]])
            shellcode.je_offset(0xcc+0x56*9)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["11"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["11"]])
            shellcode.je_offset(0xcc+0x56*10)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["12"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["12"]])
            shellcode.je_offset(0xcc+0x56*11)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["13"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["13"]])
            shellcode.je_offset(0xcc+0x56*12)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["14"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["14"]])
            shellcode.je_offset(0xcc+0x56*13)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["shovel"] > 0):
            shellcode.cmp_exx_dword(
                asm.EDI, data.keyCode[slot_key_list["shovel"]])
            shellcode.je_offset(0xcc+0x56*14)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["hp"] > 0):
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["hp"]])
            shellcode.je_offset(0x5a0)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if (slot_key_list["top"] > 0):
            shellcode.cmp_exx_dword(
                asm.EDI, data.keyCode[slot_key_list["top"]])
            shellcode.je_offset(0x5cf)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 0)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 1)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 2)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 3)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 4)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 5)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 6)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 7)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 8)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 9)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 10)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 11)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 12)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 13)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3a)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xff)
        shellcode.jne_offset(0x2e)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2c, 0xff)
        shellcode.jne_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_offset(0x22)
        shellcode.imul_exx_eyy_dword(asm.EDX, asm.EDX, 0x50)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x144)
        shellcode.add_exx_eyy(asm.EAX, asm.EDX)
        shellcode.lea_exy_byte(0x40, 0x28)
        shellcode.push_exx(asm.EAX)
        shellcode.call(0x00488590)
        shellcode.call(0x0040E520)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx_dword_ptr(asm.EBX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EBX, 0x768)
        shellcode.mov_exx_eyy(asm.EAX, asm.EBX)
        shellcode.call(0x0040CD80)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EBX, 0x138)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EBX, 0x30, 0x6)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx_dword_ptr(asm.EDX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.EDX, 0x768)
        shellcode.cmp_dword_ptr_exx_add_dword_byte(asm.EDX, 0x57b8, 0x1)
        shellcode.je_offset(0xc)
        shellcode.mov_ptr_exx_add_dowrd_dword(asm.EDX, 0x57b8, 0x1)
        shellcode.jmp_offest(0x0a)
        shellcode.mov_ptr_exx_add_dowrd_dword(asm.EDX, 0x57b8, 0x0)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx_dword_ptr(asm.EDX, 0x006a9ec0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.EDX, 0x768)
        shellcode.cmp_dword_ptr_exx_add_dword_byte(asm.EDX, 0x57bc, 0x1)
        shellcode.je_offset(0xc)
        shellcode.mov_ptr_exx_add_dowrd_dword(asm.EDX, 0x57bc, 0x1)
        shellcode.jmp_offest(0x0a)
        shellcode.mov_ptr_exx_add_dowrd_dword(asm.EDX, 0x57bc, 0x0)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8c)
        shellcode.jmp(0x0041B278)

        data.PVZ_memory.write_bytes(newmem_slotKey, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
        data.PVZ_memory.write_bytes(
            0x0041B272, b'\xe9'+calculate_call_address(newmem_slotKey-0x0041B277)+b'\x90', 6)
        data.PVZ_memory.write_bytes(
            0x00539660, b'\x90\x90\x90\x90\x90\x90', 6)

    else:
        data.PVZ_memory.write_bytes(
            0x0041B272, b'\x8b\x96\x8c\x00\x00\x00', 6)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_slotKey)


def setAllBullet(f, type):
    global newmem_setAllBullet
    if (f):
        newmem_setAllBullet = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        shellcode = (
            b'\xc7\x46\x5c'+type.to_bytes(4, byteorder='little')
            + b'\xda\x64\x24\x18\x57\xe9' +
            calculate_call_address(0x0046e8e1-newmem_setAllBullet-0x11)
        )
        data.PVZ_memory.write_bytes(newmem_setAllBullet, shellcode, 17)
        data.PVZ_memory.write_bytes(
            0x0046e8dc, b'\xe9'+calculate_call_address(newmem_setAllBullet-0x0046e8e1), 5)
    else:
        data.PVZ_memory.write_bytes(0x0046e8dc, b'\xda\x64\x24\x18\x57', 5)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_setAllBullet)


def randomBullet(f, hasDoom, hasMine, hasPepper):
    global newmem_randomBullet
    if (f):
        newmem_randomBullet = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_randomBullet)
        shellcode.random(25)
        shellcode.cmp_exx_dword(asm.EDX, 13)
        shellcode.je_offset(0x29)
        if (hasDoom):
            shellcode.nop_6()
            shellcode.nop_6()
        else:
            shellcode.cmp_exx_dword(asm.EDX, 11)
            shellcode.je_offset(0x1d)
        if (hasMine):
            shellcode.nop_6()
            shellcode.nop_6()
        else:
            shellcode.cmp_exx_dword(asm.EDX, 22)
            shellcode.je_offset(0x11)
        if (hasPepper):
            shellcode.nop_6()
            shellcode.nop_6()
        else:
            shellcode.cmp_exx_dword(asm.EDX, 24)
            shellcode.je_offset(0x3)
        shellcode.mov_ptr_exx_add_byte_eyy(asm.ESI, 0x5c, asm.EDX)
        shellcode.add_byte(0xda)
        shellcode.add_byte(0x64)
        shellcode.add_byte(0x24)
        shellcode.add_byte(0x18)
        shellcode.add_byte(0x57)
        shellcode.jmp(0x0046e8e1)
        data.PVZ_memory.write_bytes(newmem_randomBullet, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
        data.PVZ_memory.write_bytes(
            0x0046e8dc, b'\xe9'+calculate_call_address(newmem_randomBullet-0x0046e8e1), 5)
    else:
        data.PVZ_memory.write_bytes(0x0046e8dc, b'\xda\x64\x24\x18\x57', 5)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_randomBullet)


def setAttackSpeed(multiple):
    data.PVZ_memory.write_uchar(0x045f8ac, 256-1*multiple)


def cancelAttackAnimation(f):
    if (f):
        data.PVZ_memory.write_bytes(0x00464A96, b'\x90\x90\x90\x90\x90\x90', 6)
        data.PVZ_memory.write_bytes(
            0x00464A62, b'\x90\x90\x90\x90\x90\x90\x90', 7)
    else:
        data.PVZ_memory.write_bytes(0x00464A96, b'\x0f\x85\x98\xfe\xff\xff', 6)
        data.PVZ_memory.write_bytes(
            0x00464A62, b'\x83\xbf\x90\x00\x00\x00\x13', 7)


def setBulletSize(f, size):
    global newmem_setBulletSize
    global newmem_setBulletPosition
    if (f):
        newmem_setBulletSize = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        setBulletSizeCode = asm.Asm(newmem_setBulletSize)
        setBulletSizeCode.imul_exx_eyy_byte(asm.EBX, asm.EBX, size)
        setBulletSizeCode.mov_ptr_exx_add_byte_eyy(asm.ESP, 0x44, asm.EBX)
        setBulletSizeCode.mov_exx(asm.EBX, size)
        setBulletSizeCode.imul_exx_eyy(asm.EBX, asm.EDI)
        setBulletSizeCode.mov_ptr_exx_add_byte_eyy(asm.ESP, 0x40, asm.EBX)
        setBulletSizeCode.jmp(0x0046E77A)
        data.PVZ_memory.write_bytes(newmem_setBulletSize, bytes(
            setBulletSizeCode.code[:setBulletSizeCode.index]), setBulletSizeCode.index)
        data.PVZ_memory.write_bytes(
            0x0046E772, b'\xe9'+calculate_call_address(newmem_setBulletSize-0x0046E777)+b'\x90\x90\x90', 8)

        newmem_setBulletPosition = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        movement = int(size/2)
        setBulletPositionCode = asm.Asm(newmem_setBulletPosition)
        setBulletPositionCode.mov_exx(asm.EAX, movement)
        setBulletPositionCode.imul_exx_eyy(asm.EAX, asm.EDI)
        setBulletPositionCode.neg_exx(asm.EAX)
        setBulletPositionCode.mov_ptr_exx_add_byte_eyy(asm.ESP, 0x34, asm.EAX)
        setBulletPositionCode.mov_exx(asm.EAX, movement)
        setBulletPositionCode.imul_exx_eyy(asm.EAX, asm.EBX)
        setBulletPositionCode.neg_exx(asm.EAX)
        setBulletPositionCode.mov_ptr_exx_add_byte_eyy(asm.ESP, 0x38, asm.EAX)
        setBulletPositionCode.xor_exx_eyy(asm.EAX, asm.EAX)
        setBulletPositionCode.jmp(0x0046E76D)
        data.PVZ_memory.write_bytes(newmem_setBulletPosition, bytes(
            setBulletPositionCode.code[:setBulletPositionCode.index]), setBulletPositionCode.index)
        data.PVZ_memory.write_bytes(
            0x0046E765, b'\xe9'+calculate_call_address(newmem_setBulletPosition-0x0046E76A)+b'\x90\x90\x90', 8)

    else:
        data.PVZ_memory.write_bytes(
            0x0046E772, b'\x89\x7c\x24\x40\x89\x5c\x24\x44', 8)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_setBulletSize)
        data.PVZ_memory.write_bytes(
            0x0046E765, b'\x89\x44\x24\x34\x89\x44\x24\x38', 8)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_setBulletPosition)


def setPlantBullet(f, plantType, bulletType, mode):
    global newmem_setPlantBullet
    if (f):
        newmem_setPlantBullet = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_setPlantBullet)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBP, 0x24, plantType)
        shellcode.jne_offset(0xe)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EAX, 0x5c, bulletType)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EAX, 0x58, mode)
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EDX, asm.ESP, 0x3c)
        shellcode.mov_exx_eyy(asm.ECX, asm.EAX)
        shellcode.jmp(0x004672BB)
        data.PVZ_memory.write_bytes(newmem_setPlantBullet, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
        data.PVZ_memory.write_bytes(
            0x004672B5, b'\xe9'+calculate_call_address(newmem_setPlantBullet-0x004672BA)+b'\x90', 6)
    else:
        data.PVZ_memory.write_bytes(
            0x004672B5, b'\x8b\x54\x24\x3c\x8b\xc8', 6)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_setPlantBullet)


def startCar(addr):
    class carStart:
        def __init__(self, addr):
            self.addr = addr

        def creat_asm(self, startAddress):
            carStart_asm = asm.Asm(startAddress)
            carStart_asm.mov_exx(asm.ESI, self.addr)
            carStart_asm.call(0x00458da0)
            return carStart_asm

    asm.runThread(carStart(addr))


def recoveryCars():
    class carsRecovery:
        def __init__(self) -> None:
            pass

        def creat_asm(self, startAddress):
            carsRecovery_asm = asm.Asm(startAddress)
            carsRecovery_asm.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
            carsRecovery_asm.mov_exx_dword_ptr_eyy_add_dword(
                asm.EAX, asm.EAX, 0x768)
            carsRecovery_asm.push_exx(asm.EAX)
            carsRecovery_asm.call(0x0040bc70)
            return carsRecovery_asm

    data.PVZ_memory.write_bytes(0x0040bc98, b'\xeb\x60', 2)
    data.PVZ_memory.write_bytes(0x00458002, b'\xfc\x99', 2)
    data.PVZ_memory.write_bytes(0x0040bd17, b'\x01', 1)
    asm.runThread(carsRecovery())
    data.PVZ_memory.write_bytes(0x0040bc98, b'\x75\x09', 2)
    data.PVZ_memory.write_bytes(0x00458002, b'\xf8\x9b', 2)
    data.PVZ_memory.write_bytes(0x0040bd17, b'\x00', 1)


def endlessCar(f):
    global newmem_endlessCar
    if (f):
        newmem_endlessCar = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_endlessCar)
        shellcode.add_byte(0xd9)
        shellcode.add_byte(0x43)
        shellcode.add_byte(0x08)
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EAX, asm.EBX, 0x34)
        shellcode.cmp_dword_ptr_exx_add_byte_dword(asm.EBX, 0x8, 0x44480000)
        shellcode.jb_offset(0x09)
        shellcode.nop_4()
        shellcode.jmp(0x00458AF2)
        shellcode.cmp_dword_ptr_exx_add_byte_dword(asm.EBX, 0x8, 0x44444000)
        shellcode.ja_offset(0x9)
        shellcode.nop_4()
        shellcode.jmp(0x00458AF2)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EBX, 0x08, 0xc2c80000)
        shellcode.jmp(0x00458AF2)
        data.PVZ_memory.write_bytes(newmem_endlessCar, bytes(
            shellcode.code[:shellcode.index]), shellcode.index)
        data.PVZ_memory.write_bytes(
            0x00458AEC, b'\xe9'+calculate_call_address(newmem_endlessCar-0x00458AF1)+b'\x90', 6)
    else:
        data.PVZ_memory.write_bytes(0x00458AEC, b'\xd9\x43\x08\x8b\x43\x34', 6)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_endlessCar)


def initCar(f):
    if f:
        data.PVZ_memory.write_bytes(0x0040BCA3, b'\x83\xfa\x14\x7a\x70', 5)
    else:
        data.PVZ_memory.write_bytes(0x0040BCA3, b'\x83\xfa\x14\x7a\x70', 5)


def autoCar(f):
    global newmem_autoCar  # 声明 newmem 为全局变量
    if f:
        # if enable_LawnMowers==1:
        newmem_autoCar = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 128)
        # print(f"无限小车 by 妥妥的 2024-4-9 08:30:45, allocated memory: {hex(newmem)},patch addr: {hex(0x458d99)}")
        data.PVZ_memory.write_bytes(
            0x458d99, b'\xe9' + calculate_call_address(newmem_autoCar-0x0458D9E), 5)
        byte_data = (
            b'\x60\x9C\xBF\x00\x00\x00\x00\x8B\x35\xC0\x9E\x6A\x00\x8B\xAE'
            b'\x68\x07\x00\x00\x8D\xB5\x00\x01\x00\x00\x89\x7E\x04\x89\x7E'
            b'\x0C\x89\x7E\x10\xB8\x77\xD1\x00\x00\x01\xF8\x89\x46\x14\xE8'
            # pm.write_uint(newmem+45,0x41E120 - newmem - 0x31)
            + calculate_call_address(0x41E120 - newmem_autoCar - 0x31) +
            b'\x8B\xF0\x56\x8B\xC7\xE8'
            + calculate_call_address(0x00458000 - newmem_autoCar - 0x3B) +
            b'\xB8\x00\x00\xA8\xC1\x89\x46\x08\x83\xC7\x01\x83\xC3\x04\x83'
            b'\xFF\x06\x7C\xB9\x9D\x61\xC3'
        )
        data.PVZ_memory.write_bytes(newmem_autoCar, byte_data, 81)
    else:
        data.PVZ_memory.write_bytes(0x458d99, b'\xC3\xCC\xCC\xCC\xCC', 5)
        # process_handle = pymem.process.open(pid[1])
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_autoCar)


def pauseProKey(key, r, g, b, a):
    global newmem_pauseProKey
    global newmem_drawTime
    global newmem_pause
    global newmem_pauseFlag
    global newmem_draw
    if key != False:
        newmem_pauseProKey = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64)
        print(hex(newmem_pauseProKey))
        newmem_pause = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 128)
        print(hex(newmem_pause))
        newmem_draw = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256)
        print(hex(newmem_draw))
        newmem_drawTime = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 4)
        print(hex(newmem_drawTime))
        newmem_pauseFlag = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 1)
        print(hex(newmem_pauseFlag))
        shell_code_key = asm.Asm(newmem_pauseProKey)
        shell_code_key.push_exx(asm.EDX)
        shell_code_key.call(0x0051C5A0)
        shell_code_key.cmp_exx_byte(asm.EDI, data.keyCode[key])
        shell_code_key.jne_offset(7)
        shell_code_key.xor_dword_ptr_address_val(newmem_pauseFlag, 1)
        shell_code_key.jmp(0x0041B2A1)
        data.PVZ_memory.write_bytes(newmem_pauseProKey, bytes(
            shell_code_key.code[:shell_code_key.index]), shell_code_key.index)
        data.PVZ_memory.write_bytes(
            0x0041B29B, b'\xe9'+calculate_call_address(newmem_pauseProKey-0x0041B2A0)+b'\x90', 6)

        pause_key = asm.Asm(newmem_pause)
        pause_key.cmp_dword_ptr_address_byte(newmem_pauseFlag, 1)
        pause_key.jne_offset(0x1f)
        pause_key.add_dword_ptr_address_byte(newmem_drawTime, 24)
        pause_key.cmp_dword_ptr_address_dword(newmem_drawTime, 1000)
        pause_key.jl_offset(0x29)
        pause_key.mov_dword_ptr_dword(newmem_drawTime, 1000)
        pause_key.jmp_offest(0x1d)
        pause_key.sub_dword_ptr_address_byte(newmem_drawTime, 32)
        pause_key.cmp_dword_ptr_address_dword(newmem_drawTime, 0)
        pause_key.jg_offset(0x0a)
        pause_key.mov_dword_ptr_dword(newmem_drawTime, 0)
        pause_key.cmp_dword_ptr_address_dword(newmem_drawTime, 0)
        pause_key.jle_offset(0x45)
        pause_key.pushad()
        pause_key.mov_exx_dword_ptr_eyy_add_dword(asm.ESI, asm.EBP, 0x148)
        pause_key.call(0x00448330)
        pause_key.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.EBP, 0x13c)
        pause_key.call(0x00438DA0)
        pause_key.mov_exx_dword_ptr_eyy_add_dword(asm.ESI, asm.EBP, 0x138)
        pause_key.call(0x00438780)
        pause_key.popad()
        pause_key.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.EBP, 0x13c)
        pause_key.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EBP, 0x138)
        pause_key.pop_exx(asm.EBP)
        pause_key.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ESP, 0x104)
        pause_key.mov_fs_offset_exx(0, asm.ECX)
        pause_key.add_exx_dword(asm.ESP, 0x110)
        pause_key.ret()
        pause_key.cmp_dword_ptr_exx_add_dword_byte(asm.EBP, 0x164, 1)
        pause_key.je(0x00415DF9)
        pause_key.jmp(0x00415E2E)
        data.PVZ_memory.write_bytes(newmem_pause, bytes(
            pause_key.code[:pause_key.index]), pause_key.index)
        data.PVZ_memory.write_bytes(
            0x00415DF0, b'\xe9'+calculate_call_address(newmem_pause-0x00415DF5)+b'\x90\x90', 7)

        shellcode_draw = asm.Asm(newmem_draw)
        shellcode_draw.cmp_dword_ptr_address_byte(newmem_drawTime, 0)
        shellcode_draw.jng_dword_offset(0xb3)
        shellcode_draw.pushad()
        shellcode_draw.mov_exx_dword_ptr(asm.EAX, newmem_drawTime)
        shellcode_draw.mov_ptr_exx_add_byte_dword(asm.EDI, 0x30, r)
        shellcode_draw.mov_ptr_exx_add_byte_dword(asm.EDI, 0x34, g)
        shellcode_draw.mov_ptr_exx_add_byte_dword(asm.EDI, 0x38, b)
        shellcode_draw.mov_ptr_exx_add_byte_dword(asm.EDI, 0x3c, a)
        shellcode_draw.push_exx(asm.EAX)
        shellcode_draw.push_dword(300)
        shellcode_draw.push_dword(400)
        shellcode_draw.mov_exx_eyy(asm.EAX, asm.EDI)
        shellcode_draw.call_dword_offset(6)
        shellcode_draw.popad()
        shellcode_draw.jmp_dword_offest(0x78)
        shellcode_draw.pushad()
        shellcode_draw.code[shellcode_draw.index:shellcode_draw.index + 94] = b'\x8B\xF0\x8B\x44\x24\x24\x8B\x5C\x24\x28\x8B\x4C\x24\x2C\x8D\x2C\x4D\x00\x00\x00\x00\x31\xD2\xDB\x44\x24\x2C\xD8\xC8\xD9\x5C\x24\xFC\x8B\x4C\x24\x2C\x29\xD1\x89\x4C\x24\xF8\xDB\x44\x24\xF8\xD8\xC8\xD9\x5C\x24\xF8\xD9\x44\x24\xFC\xD8\x64\x24\xF8\xD9\xFA\xDB\x5C\x24\xFC\x8B\x44\x24\xFC\x8D\x1C\x45\x00\x00\x00\x00\x8B\x4C\x24\x24\x29\xC1\x8B\x7C\x24\x28\x2B\x7C\x24\x2C\x01\xD7'
        shellcode_draw.index += 94
        shellcode_draw.pushad()
        shellcode_draw.push_byte(1)
        shellcode_draw.push_exx(asm.EBX)
        shellcode_draw.push_exx(asm.EDI)
        shellcode_draw.push_exx(asm.ECX)
        shellcode_draw.mov_exx_eyy(asm.EAX, asm.ESI)
        shellcode_draw.call(0x00586D50)
        shellcode_draw.popad()
        shellcode_draw.add_exx_byte(asm.EDX, 1)
        shellcode_draw.cmp_exx_eyy(asm.EDX, asm.EBP)
        shellcode_draw.jle_offset(0xa4)
        shellcode_draw.popad()
        shellcode_draw.ret_word(0xc)
        shellcode_draw.cmp_dword_ptr_exx_add_dword_byte(asm.EBP, 0x5748, 0)
        shellcode_draw.jmp(0x0041AAC5)
        data.PVZ_memory.write_bytes(newmem_draw, bytes(
            shellcode_draw.code[:shellcode_draw.index]), shellcode_draw.index)
        data.PVZ_memory.write_bytes(
            0x0041AABE, b'\xe9'+calculate_call_address(newmem_draw-0x0041AAC3)+b'\x90\x90', 7)
    else:
        data.PVZ_memory.write_bytes(
            0x0041B29B, b'\x52\xe8\xff\x12\x10\x00', 6)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_pauseProKey)

        data.PVZ_memory.write_bytes(
            0x00415DF0, b'\x80\x8d\x64\x01\x00\x00\x00', 7)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_pause)

        data.PVZ_memory.write_bytes(
            0x0041AABE, b'\x83\xbd\x48\x57\x00\x00\x00', 7)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_draw)


def creatSpecialEffects(id, x, y):
    class specialEffects:
        def __init__(self, id, x, y):
            self.id = id
            self.x = x
            self.y = y

        def creat_asm(self, startAddress):
            specialEffects_asm = asm.Asm(startAddress)
            specialEffects_asm.push_byte(self.id)
            specialEffects_asm.push_dword(400000)
            specialEffects_asm.push_float(y)
            specialEffects_asm.push_float(x)
            specialEffects_asm.mov_exx_dword_ptr(asm.ESI, 0x006a9ec0)
            specialEffects_asm.mov_exx_dword_ptr_eyy_add_dword(
                asm.ESI, asm.ESI, 0x820)
            specialEffects_asm.mov_exx_dword_ptr_eyy(asm.ESI, asm.ESI)
            specialEffects_asm.call(0x00518A70)
            return (specialEffects_asm)

    asm.runThread(specialEffects(id, x, y))
