# ruff: noqa: F401,F403,F405,E402,F541,E722
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
newmem_zombiebeanHpynotized1 = None
newmem_zombiebeanHpynotized = None
newmem_autoCar = None
newmem_pauseProKey = None
newmem_drawTime = None
newmem_pause = None
newmem_draw = None
newmem_pauseFlag = None
newmem_setBulletSize = None
newmem_setBulletPosition = None
newmem_setPlantBullet = None
newmem_caption = None
newmem_setOneBullet = None
newmem_setBulletDamage = None
newmem_globalSpawModify = None
newmem_changeZombieHead = None
newmem_changeZombieDeadHead = None
newmem_deathrattleCallZombie = None
newmem_reserveMaterialDropAllCard = None
newmem_modifySpawNum = None
newmem_lockLevel = None
newmem_divzero = None
newmem_modifySpawMultiplier = None
newmem_spawisModified = None
newmem_bungeeTipFix = None
newmem_bungeePutFix = None


def calculate_call_address(ctypes_obj):
    """S
    计算函数调用地址
    """
    c_uint_obj = ctypes.c_uint(ctypes_obj)
    return ctypes.string_at(ctypes.addressof(c_uint_obj), ctypes.sizeof(c_uint_obj))


def getMap():
    try:
        map = data.PVZ_memory.read_int(
            data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x768)
            + 0x554C
        )
        if (
            map == 0
            or map == 1
            or map == 10
            or map == 13
            or map == 15
            or map == 16
            or map == 18
            or map == 19
            or map == 21
        ):
            return 5
        elif (
            map == 2
            or map == 11
            or map == 3
            or map == 12
            or map == 14
            or map == 17
            or map == 20
            or map == 22
            or map == 23
        ):
            return 6
        else:
            return False
    except:
        return False


def getDifficult():
    difficultAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x428
    )
    difficultValue = data.PVZ_memory.read_int(difficultAddr)
    if difficultValue == -1:
        return 1
    if difficultValue == 0:
        return 2
    if difficultValue == 1:
        return 3


def setDifficult(difficult):
    difficultAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x428
    )
    if difficult == 1:
        data.PVZ_memory.write_int(difficultAddr, 4294967295)
    if difficult == 2:
        data.PVZ_memory.write_int(difficultAddr, 0)
    if difficult == 3:
        data.PVZ_memory.write_int(difficultAddr, 1)


def getState():
    try:
        game_state = data.PVZ_memory.read_int(
            data.PVZ_memory.read_int(data.baseAddress) + 0x7FC
        )
        return game_state  # 1主菜单 2选局内  5帮助  7关卡选择
    except:
        return False


def getNowFlag():
    try:
        nowFlag = data.PVZ_memory.read_int(
            data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x768)
            + 0x557C
        )
        return nowFlag
    except:
        return False


def backGround(f):
    if f:
        data.PVZ_memory.write_bytes(0x0054EBEF, b"\xc3", 1)
    else:
        data.PVZ_memory.write_bytes(0x0054EBEF, b"\x57", 1)


def overPlant(f):
    addr = (
        int.from_bytes(
            data.PVZ_memory.read_bytes(0x40E2C2, 1)
            + data.PVZ_memory.read_bytes(0x40E2C1, 1)
            + data.PVZ_memory.read_bytes(0x40E2C0, 1)
            + data.PVZ_memory.read_bytes(0x40E2BF, 1)
        )
        + 0x40E2C3
    )
    if f:
        data.PVZ_memory.write_bytes(0x00425634, b"\xeb\x1b\x0f\x1f\x00", 5)
        data.PVZ_memory.write_bytes(0x0040E3C6, b"\xe9\x94\x00\x00\x00\x0f\x1f\x00", 8)
        data.PVZ_memory.write_bytes(0x0040FE2D, b"\xe9\x22\x09\x00\x00\x0f\x1f", 7)
        data.PVZ_memory.write_bytes(0x0042A2D6, b"\xe9\xe2\x00\x00\x00\x0f\x1f\x00", 8)
        data.PVZ_memory.write_bytes(0x00438E3E, b"\xeb\x34\x66\x90", 4)
        data.PVZ_memory.write_bytes(
            0x0040E263, b"\x8b\x5c\x24\x24\xeb\x2a\x0f\x1f\x00", 9
        )
        data.PVZ_memory.write_bytes(
            addr, b"\x0f\x1f\x00\x8b\x4c\x24\x2c\x66\x0f\x1f\x44\x00\x00", 13
        )
        data.PVZ_memory.write_bytes(
            0x00843D50, b"\xeb\x6a\x90\x90\x90\x90\x90\x90\x90", 9
        )
        data.PVZ_memory.write_bytes(0x00410908, b"\xeb\x12\x90\x90\x90", 5)
        data.PVZ_memory.write_bytes(0x00843DEE, b"\xe9\xe1\xcb\xbc\xff\x0f\x1f\x00", 8)
        data.PVZ_memory.write_bytes(0x00843E23, b"\xe9\xac\xcb\xbc\xff\x0f\x1f\x00", 8)
        data.PVZ_memory.write_bytes(0x00843E58, b"\xe9\x77\xcb\xbc\xff\x0f\x1f\x00", 8)
        data.PVZ_memory.write_bytes(0x00410958, b"\xeb\x7a\x90\x90", 4)
        data.PVZ_memory.write_bytes(0x00410960, b"\xeb\x72", 2)
        data.PVZ_memory.write_bytes(0x00410B11, b"\x90\x90", 2)
        data.PVZ_memory.write_bytes(0x00410B16, b"\xeb\x47", 2)
        data.PVZ_memory.write_bytes(0x0084A3EB, b"\xe9\x6a\x3f\xbc\xff\x90", 6)
        data.PVZ_memory.write_bytes(0x00410BA2, b"\xeb\x06", 2)
    else:
        data.PVZ_memory.write_bytes(0x00425634, b"\x83\xf8\xff\x74\x18", 5)
        data.PVZ_memory.write_bytes(0x0040FE2D, b"\x85\xc0\x0f\x84\x1f\x09\x00", 7)
        data.PVZ_memory.write_bytes(0x0040E3C6, b"\x85\xdb\x0f\x84\x91\x00\x00\x00", 8)
        data.PVZ_memory.write_bytes(0x0042A2D6, b"\x85\xc0\x0f\x84\xdf\x00\x00\x00", 8)
        data.PVZ_memory.write_bytes(0x00438E3E, b"\x85\xc0\x74\x32", 4)
        data.PVZ_memory.write_bytes(
            0x0040E263, b"\x83\xf9\x03\x8b\x5c\x24\x24\x75\x27", 9
        )
        data.PVZ_memory.write_bytes(
            addr,
            b"\x83\xf9\x02\x8b\x4c\x24\x2c\x0f\x84"
            + calculate_call_address(0x0040E2CD - addr - 0xD),
            13,
        )
        data.PVZ_memory.write_bytes(
            0x00843D50, b"\x83\xfb\x4c\x0f\x84\xb4\xcb\xbc\xff", 9
        )
        data.PVZ_memory.write_bytes(0x00410908, b"\x83\xfb\x17\x75\x0f", 5)
        data.PVZ_memory.write_bytes(0x00843DEE, b"\x85\xc0\x0f\x84\xde\xcb\xbc\xff", 8)
        data.PVZ_memory.write_bytes(0x00843E23, b"\x85\xc0\x0f\x84\xa9\xcb\xbc\xff", 8)
        data.PVZ_memory.write_bytes(0x00843E58, b"\x85\xc0\x0f\x84\x74\xcb\xbc\xff", 8)
        data.PVZ_memory.write_bytes(0x00410958, b"\x85\xc0\x73\x78", 4)
        data.PVZ_memory.write_bytes(0x00410960, b"\x75\x72", 2)
        data.PVZ_memory.write_bytes(0x00410B11, b"\x74\x05", 2)
        data.PVZ_memory.write_bytes(0x00410B16, b"\x75\x47", 2)
        data.PVZ_memory.write_bytes(0x0084A3EB, b"\x0f\x85\x69\x3f\xbc\xff", 6)
        data.PVZ_memory.write_bytes(0x00410BA2, b"\x75\x06", 2)


def getSun():
    sunAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x768)
        + 0x5560
    )
    sunNow = data.PVZ_memory.read_int(sunAddr)
    return sunNow


def addSun(sunIncrement):
    sunAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x768)
        + 0x5560
    )
    sunNow = data.PVZ_memory.read_int(sunAddr)
    data.PVZ_memory.write_int(sunAddr, sunNow + int(sunIncrement))


def subSun(sunDecrement):
    sunAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x768)
        + 0x5560
    )
    sunNow = data.PVZ_memory.read_int(sunAddr)
    sun = sunNow - int(sunDecrement)
    data.PVZ_memory.write_int(sunAddr, sun)


def setSun(sun):
    sunAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x768)
        + 0x5560
    )
    data.PVZ_memory.write_int(sunAddr, int(sun))


def cancalSunFall(f):
    if f:
        data.PVZ_memory.write_bytes(0x00413B7C, b"\x90\x90\x90\x90\x90\x90\x90", 7)
    else:
        data.PVZ_memory.write_bytes(0x00413B7C, b"\x83\x86\x38\x55\x00\x00\xff", 7)


def getSilver():
    silverAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x208
    )
    silverNow = data.PVZ_memory.read_int(silverAddr)
    return silverNow


def addSilver(silverIncrement):
    silverAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x208
    )
    silverNow = data.PVZ_memory.read_int(silverAddr)
    data.PVZ_memory.write_int(silverAddr, silverNow + int(silverIncrement))


def setSilver(silver):
    silverAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x208
    )
    data.PVZ_memory.write_int(silverAddr, int(silver))


def getGold():
    goldAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x20C
    )
    goldNow = data.PVZ_memory.read_int(goldAddr)
    return goldNow


def addGold(goldIncrement):
    goldAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x20C
    )
    goldNow = data.PVZ_memory.read_int(goldAddr)
    data.PVZ_memory.write_int(goldAddr, goldNow + int(goldIncrement))


def setGold(gold):
    goldAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x20C
    )
    data.PVZ_memory.write_int(goldAddr, int(gold))


def getDiamond():
    diamondAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x210
    )
    diamondNow = data.PVZ_memory.read_int(diamondAddr)
    return diamondNow


def addDiamond(diamondIncrement):
    diamondAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x210
    )
    diamondNow = data.PVZ_memory.read_int(diamondAddr)
    data.PVZ_memory.write_int(diamondAddr, diamondNow + int(diamondIncrement))


def setDiamond(diamond):
    diamondAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x210
    )
    data.PVZ_memory.write_int(diamondAddr, int(diamond))


def upperLimit(f):
    if f:
        data.PVZ_memory.write_bytes(0x00430A23, b"\xeb", 1)
        data.PVZ_memory.write_bytes(0x00430A78, b"\xeb", 1)
        data.PVZ_memory.write_bytes(0x0048CAB0, b"\xeb", 1)
    else:
        data.PVZ_memory.write_bytes(0x00430A23, b"\x7e", 1)
        data.PVZ_memory.write_bytes(0x00430A78, b"\x7e", 1)
        data.PVZ_memory.write_bytes(0x0048CAB0, b"\x7e", 1)


def pausePro(f):
    if f:
        data.PVZ_memory.write_bytes(
            0x415DF0, b"\x0f\x1f\x80\x00\x00\x00\x00\x66\x90", 9
        )
    else:
        data.PVZ_memory.write_bytes(
            0x415DF0, b"\x80\xbd\x64\x01\x00\x00\x00\x74\x35", 9
        )


def ignoreSun(f):
    if f:
        data.PVZ_memory.write_bytes(0x0041BA70, b"\x90\x90\x90\x90\x90\x90", 6)
        data.PVZ_memory.write_bytes(0x0048881B, b"\xe9\x97\x01\x00\x00\x0f\x1f\x00", 8)
        data.PVZ_memory.write_bytes(0x0048847F, b"\xeb", 1)
        data.PVZ_memory.write_bytes(0x0040F8A2, b"\xeb", 1)
        data.PVZ_memory.write_bytes(0x00488565, b"\xeb\x0e\x90\x90", 4)
    else:
        data.PVZ_memory.write_bytes(0x0041BA70, b"\x39\xc3\x7f\x0c\x29\xde", 6)
        data.PVZ_memory.write_bytes(0x0048881B, b"\x84\xc0\x0f\x85\x94\x01\x00\x00", 8)
        data.PVZ_memory.write_bytes(0x0048847F, b"\x75", 1)
        data.PVZ_memory.write_bytes(0x0040F8A2, b"\x75", 1)
        data.PVZ_memory.write_bytes(0x00488565, b"\x84\xc0\x75\x0c", 4)


def cancelCd(f):
    # if f:
    #     data.PVZ_memory.write_bytes(0x487293, b'\x3b\x47\x28\x90\x90', 5)
    # else:
    #     data.PVZ_memory.write_bytes(0x487296, b'\x7e\x14', 2)
    if f:
        data.PVZ_memory.write_bytes(0x487296, b"\x70", 1)
        data.PVZ_memory.write_bytes(0x00488250, b"\xeb", 1)
        data.PVZ_memory.write_bytes(0x00488E73, b"\xc6\x45\x48\x01", 4)
    else:
        data.PVZ_memory.write_bytes(0x487296, b"\x7e", 1)
        data.PVZ_memory.write_bytes(0x00488250, b"\x75", 1)
        data.PVZ_memory.write_bytes(0x00488E73, b"\xc6\x45\x48\x00", 4)


def zombieInvisible(f):
    if f:
        data.PVZ_memory.write_bytes(0x0052E357, b"\x70", 1)
        data.PVZ_memory.write_bytes(0x0053402B, b"\x70", 1)
    else:
        data.PVZ_memory.write_bytes(0x0052E357, b"\x75", 1)
        data.PVZ_memory.write_bytes(0x0053402B, b"\x75", 1)


def killAllZombies():
    zomNum = data.PVZ_memory.read_int(
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x768)
        + 0xA0
    )
    i = 0
    j = 0
    while i < zomNum:
        zomAddresss = (
            data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(
                    data.PVZ_memory.read_int(data.baseAddress) + 0x768
                )
                + 0x90
            )
            + 0x204 * j
        )
        zomExist = data.PVZ_memory.read_bytes(zomAddresss + 0xEC, 1)
        if zomExist == b"\x00":
            data.PVZ_memory.write_int(zomAddresss + 0x28, 3)
            i = i + 1
        j = j + 1


def autoCollect(f):
    if f:
        data.PVZ_memory.write_bytes(0x43158B, b"\x80\x7b\x50\x00\xeb\x08", 6)
    else:
        data.PVZ_memory.write_bytes(0x43158B, b"\x80\x7b\x50\x00\x75\x08", 6)


def changeSlot(n, type):
    slotAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x768)
        + 0x144
    )
    data.PVZ_memory.write_int(
        data.PVZ_memory.read_int(slotAddr) + 0x5C + 0x50 * (n - 1), type
    )


def win():
    winAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x768)
        + 0x55FC
    )
    data.PVZ_memory.write_int(winAddr, 1)


def advacedPause(f):
    if f:
        data.PVZ_memory.write_bytes(
            0x415DF0, b"\x0f\x1f\x80\x00\x00\x00\x00\x66\x90", 9
        )
    else:
        data.PVZ_memory.write_bytes(
            0x415DF0, b"\x80\xbd\x64\x01\x00\x00\x00\x74\x35", 9
        )


def column(f):
    global column1addr
    global column2addr
    if f:
        column1addr = data.PVZ_memory.read_bytes(0x00410ADF, 5)
        column2addr = data.PVZ_memory.read_bytes(0x00439035, 5)
        data.PVZ_memory.write_bytes(0x00410ADF, b"\xeb\x0b\x90\x90\x90", 5)
        data.PVZ_memory.write_bytes(0x00439035, b"\xeb\x0b\x90\x90\x90", 5)
    else:
        data.PVZ_memory.write_bytes(0x00410ADF, column1addr, 5)
        data.PVZ_memory.write_bytes(0x00439035, column2addr, 5)


def unlock():
    addr = (
        int.from_bytes(
            data.PVZ_memory.read_bytes(0x00453B24, 1)
            + data.PVZ_memory.read_bytes(0x00453B23, 1)
            + data.PVZ_memory.read_bytes(0x00453B22, 1)
            + data.PVZ_memory.read_bytes(0x00453B21, 1)
        )
        + 0x00453B25
    )
    newmem_unlock = pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 128)
    shellcode = asm.Asm(newmem_unlock)
    shellcode.push_exx(asm.ESI)
    shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ESI, asm.EDI, 0x82C)
    shellcode.mov_ptr_exx_add_dword_dword(asm.ESI, 0x1C0, 1)
    shellcode.pop_exx(asm.ESI)
    shellcode.add_byte(0xB0)
    shellcode.add_byte(0x01)  # mov al,01
    shellcode.ret()
    shellcode.jmp(0x00840A77)

    data.PVZ_memory.write_bytes(
        newmem_unlock, bytes(shellcode.code[: shellcode.index]), shellcode.index
    )
    data.PVZ_memory.write_bytes(
        addr,
        b"\xe9" + calculate_call_address(newmem_unlock - addr - 5) + b"\x90\x90",
        7,
    )


def shovelpro(f):
    global newmem_shovelpro
    addr = (
        int.from_bytes(
            data.PVZ_memory.read_bytes(0x411141, 1)
            + data.PVZ_memory.read_bytes(0x411140, 1)
            + data.PVZ_memory.read_bytes(0x41113F, 1)
            + data.PVZ_memory.read_bytes(0x41113E, 1)
        )
        + 0x411142
    )
    print(hex(addr))
    if f:
        data.PVZ_memory.write_bytes(addr + 0x15, b"\xeb\x6a\x90", 3)
        newmem_shovelpro = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 100
        )
        print(hex(newmem_shovelpro))
        byte_data = (
            b"\x60\x8b\x45\x24\x8b\x7d\x04\xba\xff\xff\xff\xff\xe8"
            + calculate_call_address(0x0041DAE0 - newmem_shovelpro - 0x11)
            + b"\x01\x85\x2c\x01\x00\x00\x61\x83\xbd\x2c\x01\x00\x00\x32\x7c\x1d\x83\xad\x2c\x01\x00\x00\x32"
            b"\x60\x8b\x4d\x04\x6a\x02\x6a\x06\xff\x75\x0c\xff\x75\x08\xe8"
            + calculate_call_address(0x0040CB10 - newmem_shovelpro - 0x3B)
            + b"\x61\xeb\xda\x83\xbd\x2c\x01\x00\x00\x19\x7c\x1d\x83\xad\x2c\x01\x00\x00\x19\x60\x8b\x4d\x04"
            b"\x6a\x02\x6a\x04\xff\x75\x0c\xff\x75\x08\xe8"
            + calculate_call_address(0x0040CB10 - newmem_shovelpro - 0x61)
            + b"\x61\xeb\xb4\x83\xbd\x2c\x01\x00\x00\x0f\x7c\x1d\x83\xad\x2c\x01\x00\x00\x0f\x60\x8b\x4d\x04"
            b"\x6a\x02\x6a\x05\xff\x75\x0c\xff\x75\x08\xe8"
            + calculate_call_address(0x0040CB10 - newmem_shovelpro - 0x87)
            + b"\x61\xeb\x8e\x01\x9f\x9c\x57\x00\x00\xe9"
            + calculate_call_address(0x004111DE - newmem_shovelpro - 0x95)
        )
        data.PVZ_memory.write_bytes(newmem_shovelpro, byte_data, 149)
        data.PVZ_memory.write_bytes(
            0x004111D8,
            b"\xe9" + calculate_call_address(newmem_shovelpro - 0x004111DD) + b"\x90",
            6,
        )
    else:
        data.PVZ_memory.write_bytes(addr + 0x15, b"\x83\xf8\x17", 3)
        data.PVZ_memory.write_bytes(0x004111D8, b"\x01\x9f\x9c\x57\x00\x00", 6)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_shovelpro)


def randomSlots_operstion(randomSlots_event, haszombie):
    while not randomSlots_event.is_set():
        plant1addr = (
            data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x768)
            + 0x144
        )
        for i in range(0, 14):
            if haszombie is False:
                plant = random.randint(0, 96)
                if plant >= 48:
                    plant = plant + 27
            else:
                plant = random.randint(257, 297)
            data.PVZ_memory.write_int(
                data.PVZ_memory.read_int(plant1addr) + 0x5C + 0x50 * i, plant
            )


randomSlots_event = Event()
randomSlots_thread = None


def randomSlots(f, haszombie):
    global randomSlots_thread
    if f:
        if not randomSlots_thread or not randomSlots_thread.is_alive():
            randomSlots_event.clear()
            randomSlots_thread = Thread(
                target=randomSlots_operstion, args=(randomSlots_event, haszombie)
            )
            randomSlots_thread.start()
    else:
        # 设置事件标志，通知线程停止
        randomSlots_event.set()
        randomSlots_thread.join()  # 等待线程结束


def ignoreZombies(f):
    if f:
        data.PVZ_memory.write_bytes(0x413431, b"\xe9\x7f\x04\x00\x00\x90", 6)
    else:
        data.PVZ_memory.write_bytes(0x413431, b"\x0f\x84\x7f\x04\x00\x00", 6)


def pauseSpawn(f):
    if f:
        data.PVZ_memory.write_bytes(0x004265DC, b"\xeb", 1)
    else:
        data.PVZ_memory.write_bytes(0x004265DC, b"\x74", 1)


def changeGameSpeed(s):
    FrameDurationAddr = data.PVZ_memory.read_int(data.baseAddress) + 0x454
    if s == 0:
        data.PVZ_memory.write_int(FrameDurationAddr, 10)
        data.PVZ_memory.write_bytes(0x6A9EAA, b"\x01", 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b"\x00", 1)
    elif s == 1:
        data.PVZ_memory.write_int(FrameDurationAddr, 20)
        data.PVZ_memory.write_bytes(0x6A9EAA, b"\x00", 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b"\x00", 1)
    elif s == 2:
        data.PVZ_memory.write_int(FrameDurationAddr, 10)
        data.PVZ_memory.write_bytes(0x6A9EAA, b"\x00", 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b"\x00", 1)
    elif s == 3:
        data.PVZ_memory.write_int(FrameDurationAddr, 5)
        data.PVZ_memory.write_bytes(0x6A9EAA, b"\x00", 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b"\x00", 1)
    elif s == 4:
        data.PVZ_memory.write_int(FrameDurationAddr, 2)
        data.PVZ_memory.write_bytes(0x6A9EAA, b"\x00", 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b"\x00", 1)
    elif s == 5:
        data.PVZ_memory.write_int(FrameDurationAddr, 1)
        data.PVZ_memory.write_bytes(0x6A9EAA, b"\x00", 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b"\x00", 1)
    elif s == 6:
        data.PVZ_memory.write_int(FrameDurationAddr, 10)
        data.PVZ_memory.write_bytes(0x6A9EAA, b"\x00", 1)
        data.PVZ_memory.write_bytes(0x6A9EAB, b"\x01", 1)


def completeAdvanture(level):
    advantureAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x42C
    )
    data.PVZ_memory.write_int(advantureAddr + level * 4, 1)


def lockAdvanture(level):
    advantureAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x42C
    )
    data.PVZ_memory.write_int(advantureAddr + level * 4, 0)


def completeChallenge(level):
    challengeAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x82C
    )
    data.PVZ_memory.write_int(challengeAddr + level * 4, 1)


def lockChallenge(level):
    challengeAddr = (
        data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x82C)
        + 0x82C
    )
    data.PVZ_memory.write_int(challengeAddr + level * 4, 0)


def noHole(d, t, b):
    global newmem_noHole
    if d and not b and not t:
        data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 0)
        shellcode.jne_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if d and b and not t:
        data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 2)
        shellcode.je_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if d and b and t:
        data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 0)
        shellcode.add_byte(0x90)
        shellcode.add_byte(0x90)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if not d and b and not t:
        data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 1)
        shellcode.jne_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if not d and b and t:
        data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 0)
        shellcode.je_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if not d and not b and t:
        data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 2)
        shellcode.jne_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if d and not b and t:
        data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 64)
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 1)
        shellcode.je_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if not d and not b and not t:
        data.PVZ_memory.write_bytes(0x00466668, b"\x84\xc0\x74\x2e", 4)
        data.PVZ_memory.write_bytes(
            0x0041D790, b"\x83\x7e\x18\x00\x7e\x08\x83\x46\x18\xff", 10
        )
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_noHole)


def zombiebeanHpynotized(f):
    global newmem_zombiebeanHpynotized1
    global newmem_zombiebeanHpynotized
    if f:
        newmem_zombiebeanHpynotized1 = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64
        )
        newmem_zombiebeanHpynotized = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_zombiebeanHpynotized)
        shellcode.jmp(0x0086E267)
        data.PVZ_memory.write_bytes(
            newmem_zombiebeanHpynotized,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x0086E243,
            b"\xe9"
            + calculate_call_address(newmem_zombiebeanHpynotized - 0x0086E248)
            + b"\x90",
            6,
        )

        shellcode1 = asm.Asm(newmem_zombiebeanHpynotized1)
        shellcode1.mov_exx_dword_ptr_eyy_add_byte(asm.EAX, asm.ESI, 4)
        shellcode1.call(0x0040DDC0)
        shellcode1.mov_byte_ptr_exx_add_dword_byte(asm.EAX, 0xB8, 1)
        shellcode1.jmp(0x0084F687)
        data.PVZ_memory.write_bytes(
            newmem_zombiebeanHpynotized1,
            bytes(shellcode1.code[: shellcode1.index]),
            shellcode1.index,
        )
        data.PVZ_memory.write_bytes(
            0x0084F684,
            b"\xe9"
            + calculate_call_address(newmem_zombiebeanHpynotized1 - 0x0084F689)
            + b"\x90\x90\x90",
            8,
        )

    else:
        data.PVZ_memory.write_bytes(0x084F684, b"\x8b\x46\x04\xe8\x34\xe7\xbb\xff", 8)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_zombiebeanHpynotized
        )
        data.PVZ_memory.write_bytes(0x0086E243, b"\x0f\x84\x1e\x00\x00\x00", 6)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_zombiebeanHpynotized1
        )


def scrapHelmetControlled(f):
    if f:
        data.PVZ_memory.write_bytes(0x0084AB3F, b"\x90\xe9", 2)
    else:
        data.PVZ_memory.write_bytes(0x0084AB3F, b"\x0f\x85", 2)


def conveyorBeltFull(f):
    if f:
        data.PVZ_memory.write_bytes(0x00422D1F, b"\x0f\x80", 2)
        data.PVZ_memory.write_bytes(0x00489CA1, b"\x33\xc0", 2)
    else:
        data.PVZ_memory.write_bytes(0x00422D1F, b"\x0f\x8f", 2)
        data.PVZ_memory.write_bytes(0x00489CA1, b"\x85\xc0", 2)


def getEndlessRound():
    try:
        endlessRoundAddr = (
            data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(
                    data.PVZ_memory.read_int(data.baseAddress) + 0x768
                )
                + 0x160
            )
            + 0x6C
        )
        return data.PVZ_memory.read_int(endlessRoundAddr)
    except:
        return "未知"


def setEndlessRound(endlessRound):
    try:
        endlessRoundAddr = (
            data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(
                    data.PVZ_memory.read_int(data.baseAddress) + 0x768
                )
                + 0x160
            )
            + 0x6C
        )
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
            ladder_asm.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
            ladder_asm.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x768)
            ladder_asm.mov_exx(asm.EDI, self.row)
            ladder_asm.push_byte(self.col)
            ladder_asm.call(0x00408F40)
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
            zombiePut_asm.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
            zombiePut_asm.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
            zombiePut_asm.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x160)
            zombiePut_asm.call(0x0042A0F0)
            return zombiePut_asm

    asm.runThread(zombiePut(row, col, type))


def putBoss():
    class bossPut:
        def __init__(self):
            pass

        def creat_asm(self, startAddress):
            bossPut_asm = asm.Asm(startAddress)
            bossPut_asm.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
            bossPut_asm.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x768)
            bossPut_asm.push_byte(0)
            bossPut_asm.push_byte(25)
            bossPut_asm.call(0x0040DDC0)
            return bossPut_asm

    print("boss")
    asm.runThread(bossPut())


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
            plantPut_asm.mov_exx_dword_ptr(asm.EBP, 0x006A9EC0)
            plantPut_asm.mov_exx_dword_ptr_eyy_add_dword(asm.EBP, asm.EBP, 0x768)
            plantPut_asm.push_exx(asm.EBP)
            plantPut_asm.call(0x0040D120)
            return plantPut_asm

    asm.runThread(plautPut(row, col, type))


def putcard(row, col, type):
    address = pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 100)
    shellcode = (
        b"\x60"
        b"\xb9\xc0\x9e\x6a\x00\x8b\x09\x8b\x89\x68\x07\x00\x00"
        b"\x6a\x02\x6a\x10"
        b"\x68"
        + (0x50 + 0x64 * row).to_bytes(
            length=4, byteorder="little", signed=False
        )  # 行坐标
        + b"\x68"
        + (0x28 + 0x50 * col).to_bytes(
            length=4, byteorder="little", signed=False
        )  # 列坐标
        + b"\xba\x10\xcb\x40\x00\xff\xd2"
        b"\xc7\x40\x68"
        + type.to_bytes(length=4, byteorder="little", signed=False)  # 类型
        + b"\x61\xc3"
    )
    print("卡片", row, col, type)
    data.PVZ_memory.write_bytes(address, shellcode, 44)
    data.PVZ_memory.write_bytes(0x00552014, b"\xfe", 1)
    thread_h = pymem.ressources.kernel32.CreateRemoteThread(
        data.PVZ_memory.process_handle,
        ctypes.cast(0, pymem.ressources.structure.LPSECURITY_ATTRIBUTES),
        0,
        address,
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
        time.sleep(0.005)
    pymem.memory.free_memory(data.PVZ_memory.process_handle, address)


def creatCaption(str, time, type):
    global newmem_caption
    newmem_caption = pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 1024)
    byte_array = str.encode("gbk")
    data.PVZ_memory.write_bytes(
        newmem_caption, byte_array + b"\x00", len(byte_array) + 1
    )

    class captionCreat:
        def __init__(self, time, type):
            self.time = time
            self.type = type

        def creat_asm(self, startAddress):
            captionCreat_asm = asm.Asm(startAddress)
            captionCreat_asm.push_dword(newmem_caption)
            captionCreat_asm.lea_exx_ptr_eyy_add_byte(asm.ECX, asm.ESP, 0x30)
            captionCreat_asm.call(0x00404450)
            captionCreat_asm.mov_exx_dword_ptr(asm.EDI, 0x006A9EC0)
            captionCreat_asm.mov_exx_dword_ptr_eyy_add_dword(
                asm.EDI, asm.EDI, 0x00000768
            )
            captionCreat_asm.mov_exx_dword_ptr_eyy_add_dword(
                asm.ESI, asm.EDI, 0x00000140
            )
            captionCreat_asm.mov_exx(asm.ECX, 6)
            captionCreat_asm.lea_exx_ptr_eyy_add_byte(asm.EDX, asm.ESP, 0x2C)
            captionCreat_asm.call(0x00459010)
            captionCreat_asm.mov_ptr_exx_add_dword_dword(asm.ESI, 0x88, self.time)
            captionCreat_asm.mov_ptr_exx_add_dword_dword(
                asm.ESI, 0x8C, self.type
            )  # 1 下端 较宽 3 最下端 较窄  6  最下端 窄 9 最下端 宽  12 中端  宽  14 下端 白色字体 15 红色中间字体 16 黄色顶端字体
            return captionCreat_asm

    asm.runThread(captionCreat(time, type))


def selectCard(type):
    class cardSelect:
        def __init__(self, type):
            self.type = type

        def creat_asm(self, startAddress):
            cardSelect_asm = asm.Asm(startAddress)
            cardSelect_asm.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
            cardSelect_asm.mov_exx_dword_ptr_eyy_add_dword(asm.ESI, asm.EAX, 0x00000774)
            cardSelect_asm.mov_exx(asm.EBX, self.type)
            cardSelect_asm.imul_exx_eyy_byte(asm.EDX, asm.EBX, 0xF)
            cardSelect_asm.lea_exx_byte_dword(asm.EAX, 0x96, 0xA4)
            cardSelect_asm.push_exx(asm.EAX)
            cardSelect_asm.mov_exx_eyy(asm.EAX, asm.ESI)
            cardSelect_asm.call(0x00486030)
            return cardSelect_asm

    asm.runThread(cardSelect(type))


def deselectCard(type):
    global newmem_endlessCar

    class cardDeselect:
        def __init__(self, type):
            self.type = type

        def creat_asm(self, startAddress):
            cardDeselect_asm = asm.Asm(startAddress)
            cardDeselect_asm.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
            cardDeselect_asm.mov_exx_dword_ptr_eyy_add_dword(
                asm.ESI, asm.EAX, 0x00000774
            )
            cardDeselect_asm.mov_exx(asm.EBX, self.type)
            cardDeselect_asm.imul_exx_eyy_byte(asm.EDX, asm.EBX, 0xF)
            cardDeselect_asm.lea_exx_byte_dword(asm.EAX, 0x96, 0xA4)
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
            Defeat_asm.mov_exx(asm.EDX, 0x2D)
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
            start = data.PVZ_memory.read_bool(
                data.PVZ_memory.read_int(
                    data.PVZ_memory.read_int(
                        data.PVZ_memory.read_int(data.baseAddress) + 0x774
                    )
                    + 0x88
                )
                + 0x1A
            )
            if start is True:
                data.PVZ_memory.write_bool(
                    data.PVZ_memory.read_int(
                        data.PVZ_memory.read_int(
                            data.PVZ_memory.read_int(data.baseAddress) + 0x774
                        )
                        + 0x88
                    )
                    + 0x1A,
                    False,
                )
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
            noSlot_thread = Thread(target=noSlot_operstion, args=(noSlot_event,))
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
            Save_asm.call(0x408C30)
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
            Load_asm.call(0x44F7A0)
            return Load_asm

    asm.runThread(Load())


def spoils(spoils_config):
    global newmem_spoils
    global newmem_spoils2
    print(spoils_config)
    if spoils_config is not False:
        data.PVZ_memory.write_bytes(0x00530275, b"\x70", 1)
        newmem_spoils = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256
        )
        newmem_spoils2 = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 32
        )
        print(hex(newmem_spoils))
        print(hex(newmem_spoils2))
        shellcode = asm.Asm(newmem_spoils)
        shellcode.mov_exx_dword_ptr_eyy(asm.EAX, asm.EBX)
        shellcode.mov_exx(asm.ESI, 4)
        shellcode.call(0x00453630)
        if len(spoils_config) > 0:
            shellcode.random(100)
            shellcode.cmp_exx_byte(asm.EDX, spoils_config[0]["percent"])
            shellcode.add_byte(0x72)  # jb
            shellcode.add_byte(0x05)  # 小于则后移5位
            shellcode.add_byte(0xE9)  # 大于则jmp
            shellcode.add_dword(0x1F)
            shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ESI, asm.ESP, 0x0C)
            shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ECX, asm.EBX, 0x04)
            shellcode.push_byte(0x03)
            if spoils_config[0]["type"] <= 6:
                shellcode.push_byte(spoils_config[0]["type"])
            elif spoils_config[0]["type"] == 7:
                shellcode.push_byte(0x8)
            elif spoils_config[0]["type"] == 8:
                shellcode.push_byte(0xF)
            elif spoils_config[0]["type"] == 9:
                shellcode.push_byte(0x10)
            elif spoils_config[0]["type"] == 10:
                shellcode.push_byte(0x12)
            if spoils_config[0]["card"] == -1:
                shellcode.mov_dword_ptr_dword(0x00751EC0, 0)
            else:
                shellcode.mov_dword_ptr_dword(0x00751EC0, spoils_config[0]["card"])
            shellcode.push_exx(asm.ESI)
            shellcode.lea_exy_byte(0x47, 0xEC)
            shellcode.push_exx(asm.EAX)
            shellcode.call(0x0040CB10)
            if len(spoils_config) > 1:
                shellcode.random(100)
                shellcode.cmp_exx_byte(asm.EDX, spoils_config[1]["percent"])
                shellcode.add_byte(0x72)  # jb
                shellcode.add_byte(0x05)  # 小于则后移5位
                shellcode.add_byte(0xE9)  # 大于则jmp
                shellcode.add_dword(0x1B)
                shellcode.push_byte(0x03)
                if spoils_config[1]["type"] <= 6:
                    shellcode.push_byte(spoils_config[1]["type"])
                elif spoils_config[1]["type"] == 7:
                    shellcode.push_byte(0x8)
                elif spoils_config[1]["type"] == 8:
                    shellcode.push_byte(0xF)
                elif spoils_config[1]["type"] == 9:
                    shellcode.push_byte(0x10)
                elif spoils_config[1]["type"] == 10:
                    shellcode.push_byte(0x12)
                if spoils_config[1]["card"] == -1:
                    shellcode.mov_dword_ptr_dword(0x00751EC0, 0)
                else:
                    shellcode.mov_dword_ptr_dword(0x00751EC0, spoils_config[1]["card"])
                shellcode.push_exx(asm.ESI)
                shellcode.lea_exy_byte(0x4F, 0xE2)
                shellcode.push_exx(asm.ECX)
                shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ECX, asm.EBX, 0x04)
                shellcode.call(0x0040CB10)
                if len(spoils_config) > 2:
                    shellcode.random(100)
                    shellcode.cmp_exx_byte(asm.EDX, spoils_config[2]["percent"])
                    shellcode.add_byte(0x72)  # jb
                    shellcode.add_byte(0x05)  # 小于则后移5位
                    shellcode.add_byte(0xE9)  # 大于则jmp
                    shellcode.add_dword(0x1B)
                    shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ECX, asm.EBX, 0x04)
                    shellcode.push_byte(0x03)
                    if spoils_config[2]["type"] <= 6:
                        shellcode.push_byte(spoils_config[2]["type"])
                    elif spoils_config[2]["type"] == 7:
                        shellcode.push_byte(0x8)
                    elif spoils_config[2]["type"] == 8:
                        shellcode.push_byte(0xF)
                    elif spoils_config[2]["type"] == 9:
                        shellcode.push_byte(0x10)
                    elif spoils_config[2]["type"] == 10:
                        shellcode.push_byte(0x12)
                    if spoils_config[2]["card"] == -1:
                        shellcode.mov_dword_ptr_dword(0x00751EC0, 0)
                    else:
                        shellcode.mov_dword_ptr_dword(
                            0x00751EC0, spoils_config[2]["card"]
                        )
                    shellcode.push_exx(asm.ESI)
                    shellcode.lea_exy_byte(0x57, 0xD8)
                    shellcode.push_exx(asm.EDX)
                    shellcode.call(0x0040CB10)
                    if len(spoils_config) > 3:
                        shellcode.random(100)
                        shellcode.cmp_exx_byte(asm.EDX, spoils_config[3]["percent"])
                        shellcode.add_byte(0x72)  # jb
                        shellcode.add_byte(0x05)  # 小于则后移5位
                        shellcode.add_byte(0xE9)  # 大于则jmp
                        shellcode.add_dword(0x1B)
                        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ECX, asm.EBX, 0x04)
                        shellcode.push_byte(0x03)
                        if spoils_config[3]["type"] <= 6:
                            shellcode.push_byte(spoils_config[2]["type"])
                        elif spoils_config[3]["type"] == 7:
                            shellcode.push_byte(0x8)
                        elif spoils_config[3]["type"] == 8:
                            shellcode.push_byte(0xF)
                        elif spoils_config[3]["type"] == 9:
                            shellcode.push_byte(0x10)
                        elif spoils_config[3]["type"] == 10:
                            shellcode.push_byte(0x12)
                        if spoils_config[3]["card"] == -1:
                            shellcode.mov_dword_ptr_dword(0x00751EC0, 0)
                        else:
                            shellcode.mov_dword_ptr_dword(
                                0x00751EC0, spoils_config[3]["card"]
                            )
                        shellcode.push_exx(asm.ESI)
                        shellcode.add_exx_byte(asm.EDI, 0xCE)
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

        data.PVZ_memory.write_bytes(
            newmem_spoils2, bytes(tempcode.code[: tempcode.index]), tempcode.index
        )
        data.PVZ_memory.write_bytes(
            0x42FFB6,
            b"\xe9" + calculate_call_address(newmem_spoils2 - 0x0042FFBB) + b"\x66\x90",
            7,
        )
        data.PVZ_memory.write_bytes(
            newmem_spoils, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        data.PVZ_memory.write_bytes(
            0x00530277, b"\xe9" + calculate_call_address(newmem_spoils - 0x0053027C), 5
        )
    else:
        data.PVZ_memory.write_bytes(0x00530275, b"\x75", 1)
        data.PVZ_memory.write_bytes(0x42FFB6, b"\xc7\x45\x68\x00\x00\x00\x00", 7)
        data.PVZ_memory.write_bytes(0x00530277, b"\x8b\x03\xbe\x04\x00", 5)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_spoils)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_spoils2)


def slotKey(slot_key_list):
    if slot_key_list is not False:
        global newmem_slotKey
        print(slot_key_list)
        newmem_slotKey = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 2048
        )
        print(hex(newmem_slotKey))
        shellcode = asm.Asm(newmem_slotKey)
        shellcode.pushad()
        if slot_key_list["1"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["1"]])
            shellcode.je_offset(0xD8)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["2"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["2"]])
            shellcode.je_offset(0xD8 + 0x56)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["3"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["3"]])
            shellcode.je_offset(0xD8 + 0x56 * 2)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["4"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["4"]])
            shellcode.je_offset(0xD8 + 0x56 * 3)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["5"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["5"]])
            shellcode.je_offset(0xD8 + 0x56 * 4)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["6"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["6"]])
            shellcode.je_offset(0xD8 + 0x56 * 5)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["7"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["7"]])
            shellcode.je_offset(0xD8 + 0x56 * 6)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["8"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["8"]])
            shellcode.je_offset(0xD8 + 0x56 * 7)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["9"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["9"]])
            shellcode.je_offset(0xD8 + 0x56 * 8)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["10"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["10"]])
            shellcode.je_offset(0xD8 + 0x56 * 9)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["11"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["11"]])
            shellcode.je_offset(0xD8 + 0x56 * 10)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["12"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["12"]])
            shellcode.je_offset(0xD8 + 0x56 * 11)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["13"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["13"]])
            shellcode.je_offset(0xD8 + 0x56 * 12)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["14"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["14"]])
            shellcode.je_offset(0xD8 + 0x56 * 13)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["shovel"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["shovel"]])
            shellcode.je_offset(0xD8 + 0x56 * 14)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["zombie_hp"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["zombie_hp"]])
            shellcode.je_offset(0x5AC)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["top"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["top"]])
            shellcode.je_offset(0x5DF)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["plant_hp"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, data.keyCode[slot_key_list["plant_hp"]])
            shellcode.je_offset(0x60E)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 0)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 1)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 2)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 3)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 4)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 5)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 6)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 7)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 8)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 9)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 10)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 11)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 12)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx(asm.EDX, 13)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
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
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx_dword_ptr(asm.EBX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EBX, 0x768)
        shellcode.mov_exx_eyy(asm.EAX, asm.EBX)
        shellcode.call(0x0040CD80)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EBX, 0x138)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EBX, 0x30, 0x6)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx_dword_ptr(asm.EDX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.EDX, 0x82C)
        shellcode.cmp_dword_ptr_exx_add_dword_byte(asm.EDX, 0x1CA0, 0x1)
        shellcode.je_offset(0x10)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EDX, 0x1CA0, 0x1)
        shellcode.popad()
        shellcode.jmp_dword_offest(0xB)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EDX, 0x1CA0, 0x0)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx_dword_ptr(asm.EDX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.EDX, 0x768)
        shellcode.cmp_dword_ptr_exx_add_dword_byte(asm.EDX, 0x57BC, 0x1)
        shellcode.je_offset(0xC)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EDX, 0x57BC, 0x1)
        shellcode.jmp_offest(0x0A)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EDX, 0x57BC, 0x0)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx_dword_ptr(asm.EDX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.EDX, 0x82C)
        shellcode.cmp_dword_ptr_exx_add_dword_byte(asm.EDX, 0x1CA4, 0x1)
        shellcode.je_offset(0x10)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EDX, 0x1CA4, 0x1)
        shellcode.popad()
        shellcode.jmp_dword_offest(0xB)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EDX, 0x1CA4, 0x0)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)

        data.PVZ_memory.write_bytes(
            newmem_slotKey, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        data.PVZ_memory.write_bytes(
            0x0041B272,
            b"\xe9" + calculate_call_address(newmem_slotKey - 0x0041B277) + b"\x90",
            6,
        )
        data.PVZ_memory.write_bytes(0x00539660, b"\x90\x90\x90\x90\x90\x90", 6)

    else:
        data.PVZ_memory.write_bytes(0x0041B272, b"\x8b\x96\x8c\x00\x00\x00", 6)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_slotKey)
        data.PVZ_memory.write_bytes(0x00539660, b"\xe9\x9b\x5c\x33\x00\x90", 6)


def setAllBullet(f, type):
    global newmem_setAllBullet
    if f:
        print(type)
        newmem_setAllBullet = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64
        )
        shellcode = (
            b"\xc7\x46\x5c"
            + type.to_bytes(4, byteorder="little")
            + b"\xda\x64\x24\x18\x57\xe9"
            + calculate_call_address(0x0046E8E1 - newmem_setAllBullet - 0x11)
        )
        data.PVZ_memory.write_bytes(newmem_setAllBullet, shellcode, 17)
        data.PVZ_memory.write_bytes(
            0x0046E8DC,
            b"\xe9" + calculate_call_address(newmem_setAllBullet - 0x0046E8E1),
            5,
        )
    else:
        data.PVZ_memory.write_bytes(0x0046E8DC, b"\xda\x64\x24\x18\x57", 5)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_setAllBullet)


def setOneBullet(f, type1, type2):
    global newmem_setOneBullet
    if f:
        newmem_setOneBullet = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_setOneBullet)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x5C, type1)
        shellcode.jne_long_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x5C, type2)
        shellcode.add_byte(0xDA)
        shellcode.add_byte(0x64)
        shellcode.add_byte(0x24)
        shellcode.add_byte(0x18)
        shellcode.add_byte(0x57)
        shellcode.jmp(0x0046E8E1)
        data.PVZ_memory.write_bytes(
            newmem_setOneBullet,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x0046E8DC,
            b"\xe9" + calculate_call_address(newmem_setOneBullet - 0x0046E8E1),
            5,
        )
    else:
        data.PVZ_memory.write_bytes(0x0046E8DC, b"\xda\x64\x24\x18\x57", 5)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_setOneBullet)


def randomBullet(f, hasDoom, hasMine, hasPepper):
    global newmem_randomBullet
    if f:
        newmem_randomBullet = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_randomBullet)
        shellcode.random(25)
        shellcode.cmp_exx_dword(asm.EDX, 13)
        shellcode.je_offset(0x29)
        if hasDoom:
            shellcode.nop_6()
            shellcode.nop_6()
        else:
            shellcode.cmp_exx_dword(asm.EDX, 11)
            shellcode.je_offset(0x1D)
        if hasMine:
            shellcode.nop_6()
            shellcode.nop_6()
        else:
            shellcode.cmp_exx_dword(asm.EDX, 22)
            shellcode.je_offset(0x11)
        if hasPepper:
            shellcode.nop_6()
            shellcode.nop_6()
        else:
            shellcode.cmp_exx_dword(asm.EDX, 24)
            shellcode.je_offset(0x3)
        shellcode.mov_ptr_exx_add_byte_eyy(asm.ESI, 0x5C, asm.EDX)
        shellcode.add_byte(0xDA)
        shellcode.add_byte(0x64)
        shellcode.add_byte(0x24)
        shellcode.add_byte(0x18)
        shellcode.add_byte(0x57)
        shellcode.jmp(0x0046E8E1)
        data.PVZ_memory.write_bytes(
            newmem_randomBullet,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x0046E8DC,
            b"\xe9" + calculate_call_address(newmem_randomBullet - 0x0046E8E1),
            5,
        )
    else:
        data.PVZ_memory.write_bytes(0x0046E8DC, b"\xda\x64\x24\x18\x57", 5)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_randomBullet)


def setAttackSpeed(multiple):
    data.PVZ_memory.write_uchar(0x045F8AC, 256 - 1 * multiple)


def cancelAttackAnimation(f):
    if f:
        data.PVZ_memory.write_bytes(0x00464A96, b"\x90\x90\x90\x90\x90\x90", 6)
        data.PVZ_memory.write_bytes(0x00464A62, b"\x90\x90\x90\x90\x90\x90\x90", 7)
    else:
        data.PVZ_memory.write_bytes(0x00464A96, b"\x0f\x85\x98\xfe\xff\xff", 6)
        data.PVZ_memory.write_bytes(0x00464A62, b"\x83\xbf\x90\x00\x00\x00\x13", 7)


def setBulletSize(f, size):
    global newmem_setBulletSize
    global newmem_setBulletPosition
    if f:
        newmem_setBulletSize = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64
        )
        setBulletSizeCode = asm.Asm(newmem_setBulletSize)
        setBulletSizeCode.imul_exx_eyy_byte(asm.EBX, asm.EBX, size)
        setBulletSizeCode.mov_ptr_exx_add_byte_eyy(asm.ESP, 0x44, asm.EBX)
        setBulletSizeCode.mov_exx(asm.EBX, size)
        setBulletSizeCode.imul_exx_eyy(asm.EBX, asm.EDI)
        setBulletSizeCode.mov_ptr_exx_add_byte_eyy(asm.ESP, 0x40, asm.EBX)
        setBulletSizeCode.jmp(0x0046E77A)
        data.PVZ_memory.write_bytes(
            newmem_setBulletSize,
            bytes(setBulletSizeCode.code[: setBulletSizeCode.index]),
            setBulletSizeCode.index,
        )
        data.PVZ_memory.write_bytes(
            0x0046E772,
            b"\xe9"
            + calculate_call_address(newmem_setBulletSize - 0x0046E777)
            + b"\x90\x90\x90",
            8,
        )

        newmem_setBulletPosition = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64
        )
        movement = int(size / 2)
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
        data.PVZ_memory.write_bytes(
            newmem_setBulletPosition,
            bytes(setBulletPositionCode.code[: setBulletPositionCode.index]),
            setBulletPositionCode.index,
        )
        data.PVZ_memory.write_bytes(
            0x0046E765,
            b"\xe9"
            + calculate_call_address(newmem_setBulletPosition - 0x0046E76A)
            + b"\x90\x90\x90",
            8,
        )

    else:
        data.PVZ_memory.write_bytes(0x0046E772, b"\x89\x7c\x24\x40\x89\x5c\x24\x44", 8)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_setBulletSize)
        data.PVZ_memory.write_bytes(0x0046E765, b"\x89\x44\x24\x34\x89\x44\x24\x38", 8)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_setBulletPosition
        )


def setPlantBullet(f, plantType, bulletType, mode):
    global newmem_setPlantBullet
    if f:
        newmem_setPlantBullet = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_setPlantBullet)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBP, 0x24, plantType)
        shellcode.jne_offset(0xE)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EAX, 0x5C, bulletType)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EAX, 0x58, mode)
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EDX, asm.ESP, 0x3C)
        shellcode.mov_exx_eyy(asm.ECX, asm.EAX)
        shellcode.jmp(0x004672BB)
        data.PVZ_memory.write_bytes(
            newmem_setPlantBullet,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x004672B5,
            b"\xe9"
            + calculate_call_address(newmem_setPlantBullet - 0x004672BA)
            + b"\x90",
            6,
        )
    else:
        data.PVZ_memory.write_bytes(0x004672B5, b"\x8b\x54\x24\x3c\x8b\xc8", 6)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_setPlantBullet)


def startCar(addr):
    class carStart:
        def __init__(self, addr):
            self.addr = addr

        def creat_asm(self, startAddress):
            carStart_asm = asm.Asm(startAddress)
            carStart_asm.mov_exx(asm.ESI, self.addr)
            carStart_asm.call(0x00458DA0)
            return carStart_asm

    asm.runThread(carStart(addr))


def recoveryCars():
    class carsRecovery:
        def __init__(self) -> None:
            pass

        def creat_asm(self, startAddress):
            carsRecovery_asm = asm.Asm(startAddress)
            carsRecovery_asm.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
            carsRecovery_asm.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x768)
            carsRecovery_asm.push_exx(asm.EAX)
            carsRecovery_asm.call(0x0040BC70)
            return carsRecovery_asm

    data.PVZ_memory.write_bytes(0x0040BC98, b"\xeb\x60", 2)
    data.PVZ_memory.write_bytes(0x00458002, b"\xfc\x99", 2)
    data.PVZ_memory.write_bytes(0x0040BD17, b"\x01", 1)
    asm.runThread(carsRecovery())
    data.PVZ_memory.write_bytes(0x0040BC98, b"\x75\x09", 2)
    data.PVZ_memory.write_bytes(0x00458002, b"\xf8\x9b", 2)
    data.PVZ_memory.write_bytes(0x0040BD17, b"\x00", 1)


def endlessCar(f):
    global newmem_endlessCar
    if f:
        newmem_endlessCar = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_endlessCar)
        shellcode.add_byte(0xD9)
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
        shellcode.mov_ptr_exx_add_byte_dword(asm.EBX, 0x08, 0xC2C80000)
        shellcode.jmp(0x00458AF2)
        data.PVZ_memory.write_bytes(
            newmem_endlessCar, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        data.PVZ_memory.write_bytes(
            0x00458AEC,
            b"\xe9" + calculate_call_address(newmem_endlessCar - 0x00458AF1) + b"\x90",
            6,
        )
    else:
        data.PVZ_memory.write_bytes(0x00458AEC, b"\xd9\x43\x08\x8b\x43\x34", 6)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_endlessCar)


def initCar(f):
    if f:
        data.PVZ_memory.write_bytes(0x0040BCA3, b"\x83\xfa\x14\x7a\x70", 5)
    else:
        data.PVZ_memory.write_bytes(0x0040BCA3, b"\x83\xfa\x14\x7a\x70", 5)


def autoCar(f):
    global newmem_autoCar  # 声明 newmem 为全局变量
    if f:
        # if enable_LawnMowers==1:
        newmem_autoCar = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 128
        )
        # print(f"无限小车 by 妥妥的 2024-4-9 08:30:45, allocated memory: {hex(newmem)},patch addr: {hex(0x458d99)}")
        data.PVZ_memory.write_bytes(
            0x458D99, b"\xe9" + calculate_call_address(newmem_autoCar - 0x0458D9E), 5
        )
        byte_data = (
            b"\x60\x9c\xbf\x00\x00\x00\x00\x8b\x35\xc0\x9e\x6a\x00\x8b\xae"
            b"\x68\x07\x00\x00\x8d\xb5\x00\x01\x00\x00\x89\x7e\x04\x89\x7e"
            b"\x0c\x89\x7e\x10\xb8\x77\xd1\x00\x00\x01\xf8\x89\x46\x14\xe8"
            # pm.write_uint(newmem+45,0x41E120 - newmem - 0x31)
            + calculate_call_address(0x41E120 - newmem_autoCar - 0x31)
            + b"\x8b\xf0\x56\x8b\xc7\xe8"
            + calculate_call_address(0x00458000 - newmem_autoCar - 0x3B)
            + b"\xb8\x00\x00\xa8\xc1\x89\x46\x08\x83\xc7\x01\x83\xc3\x04\x83"
            b"\xff\x06\x7c\xb9\x9d\x61\xc3"
        )
        data.PVZ_memory.write_bytes(newmem_autoCar, byte_data, 81)
    else:
        data.PVZ_memory.write_bytes(0x458D99, b"\xc3\xcc\xcc\xcc\xcc", 5)
        # process_handle = pymem.process.open(pid[1])
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_autoCar)


def setPausePro(f):
    global newmem_pauseFlag
    if f:
        try:
            data.PVZ_memory.write_bytes(newmem_pauseFlag, b"\x01", 1)
        except:
            pass
    else:
        try:
            print(data.PVZ_memory.read_bool(newmem_pauseFlag))
            data.PVZ_memory.write_bytes(newmem_pauseFlag, b"\x00", 1)
        except:
            pass


def pauseProKey(key, r, g, b, a):
    global newmem_pauseProKey
    global newmem_drawTime
    global newmem_pause
    global newmem_pauseFlag
    global newmem_draw
    if key is not False:
        newmem_pauseProKey = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64
        )
        print(hex(newmem_pauseProKey))
        newmem_pause = pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 128)
        print(hex(newmem_pause))
        newmem_draw = pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 256)
        print(hex(newmem_draw))
        newmem_drawTime = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 4
        )
        print(hex(newmem_drawTime))
        newmem_pauseFlag = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 1
        )
        print(hex(newmem_pauseFlag))
        shell_code_key = asm.Asm(newmem_pauseProKey)
        shell_code_key.push_exx(asm.EDX)
        shell_code_key.call(0x0051C5A0)
        shell_code_key.cmp_exx_byte(asm.EDI, data.keyCode[key])
        shell_code_key.jne_offset(7)
        shell_code_key.xor_dword_ptr_address_val(newmem_pauseFlag, 1)
        shell_code_key.jmp(0x0041B2A1)
        data.PVZ_memory.write_bytes(
            newmem_pauseProKey,
            bytes(shell_code_key.code[: shell_code_key.index]),
            shell_code_key.index,
        )
        data.PVZ_memory.write_bytes(
            0x0041B29B,
            b"\xe9" + calculate_call_address(newmem_pauseProKey - 0x0041B2A0) + b"\x90",
            6,
        )

        pause_key = asm.Asm(newmem_pause)
        pause_key.cmp_dword_ptr_address_byte(newmem_pauseFlag, 1)
        pause_key.jne_offset(0x1F)
        pause_key.add_dword_ptr_address_byte(newmem_drawTime, 24)
        pause_key.cmp_dword_ptr_address_dword(newmem_drawTime, 1000)
        pause_key.jl_offset(0x29)
        pause_key.mov_dword_ptr_dword(newmem_drawTime, 1000)
        pause_key.jmp_offest(0x1D)
        pause_key.sub_dword_ptr_address_byte(newmem_drawTime, 32)
        pause_key.cmp_dword_ptr_address_dword(newmem_drawTime, 0)
        pause_key.jg_offset(0x0A)
        pause_key.mov_dword_ptr_dword(newmem_drawTime, 0)
        pause_key.cmp_dword_ptr_address_dword(newmem_drawTime, 0)
        pause_key.jle_offset(0x45)
        pause_key.pushad()
        pause_key.mov_exx_dword_ptr_eyy_add_dword(asm.ESI, asm.EBP, 0x148)
        pause_key.call(0x00448330)
        pause_key.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.EBP, 0x13C)
        pause_key.call(0x00438DA0)
        pause_key.mov_exx_dword_ptr_eyy_add_dword(asm.ESI, asm.EBP, 0x138)
        pause_key.call(0x00438780)
        pause_key.popad()
        pause_key.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.EBP, 0x13C)
        pause_key.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EBP, 0x138)
        pause_key.pop_exx(asm.EBP)
        pause_key.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ESP, 0x104)
        pause_key.mov_fs_offset_exx(0, asm.ECX)
        pause_key.add_exx_dword(asm.ESP, 0x110)
        pause_key.ret()
        pause_key.cmp_dword_ptr_exx_add_dword_byte(asm.EBP, 0x164, 1)
        pause_key.je(0x00415DF9)
        pause_key.jmp(0x00415E2E)
        data.PVZ_memory.write_bytes(
            newmem_pause, bytes(pause_key.code[: pause_key.index]), pause_key.index
        )
        data.PVZ_memory.write_bytes(
            0x00415DF0,
            b"\xe9" + calculate_call_address(newmem_pause - 0x00415DF5) + b"\x90\x90",
            7,
        )

        shellcode_draw = asm.Asm(newmem_draw)
        shellcode_draw.cmp_dword_ptr_address_byte(newmem_drawTime, 0)
        shellcode_draw.jng_dword_offset(0xB3)
        shellcode_draw.pushad()
        shellcode_draw.mov_exx_dword_ptr(asm.EAX, newmem_drawTime)
        shellcode_draw.mov_ptr_exx_add_byte_dword(asm.EDI, 0x30, r)
        shellcode_draw.mov_ptr_exx_add_byte_dword(asm.EDI, 0x34, g)
        shellcode_draw.mov_ptr_exx_add_byte_dword(asm.EDI, 0x38, b)
        shellcode_draw.mov_ptr_exx_add_byte_dword(asm.EDI, 0x3C, a)
        shellcode_draw.push_exx(asm.EAX)
        shellcode_draw.push_dword(300)
        shellcode_draw.push_dword(400)
        shellcode_draw.mov_exx_eyy(asm.EAX, asm.EDI)
        shellcode_draw.call_dword_offset(6)
        shellcode_draw.popad()
        shellcode_draw.jmp_dword_offest(0x78)
        shellcode_draw.pushad()
        shellcode_draw.code[shellcode_draw.index : shellcode_draw.index + 94] = (
            b"\x8b\xf0\x8b\x44\x24\x24\x8b\x5c\x24\x28\x8b\x4c\x24\x2c\x8d\x2c\x4d\x00\x00\x00\x00\x31\xd2\xdb\x44\x24\x2c\xd8\xc8\xd9\x5c\x24\xfc\x8b\x4c\x24\x2c\x29\xd1\x89\x4c\x24\xf8\xdb\x44\x24\xf8\xd8\xc8\xd9\x5c\x24\xf8\xd9\x44\x24\xfc\xd8\x64\x24\xf8\xd9\xfa\xdb\x5c\x24\xfc\x8b\x44\x24\xfc\x8d\x1c\x45\x00\x00\x00\x00\x8b\x4c\x24\x24\x29\xc1\x8b\x7c\x24\x28\x2b\x7c\x24\x2c\x01\xd7"
        )
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
        shellcode_draw.jle_offset(0xA4)
        shellcode_draw.popad()
        shellcode_draw.ret_word(0xC)
        shellcode_draw.cmp_dword_ptr_exx_add_dword_byte(asm.EBP, 0x5748, 0)
        shellcode_draw.jmp(0x0041AAC5)
        data.PVZ_memory.write_bytes(
            newmem_draw,
            bytes(shellcode_draw.code[: shellcode_draw.index]),
            shellcode_draw.index,
        )
        data.PVZ_memory.write_bytes(
            0x0041AABE,
            b"\xe9" + calculate_call_address(newmem_draw - 0x0041AAC3) + b"\x90\x90",
            7,
        )
    else:
        data.PVZ_memory.write_bytes(0x0041B29B, b"\x52\xe8\xff\x12\x10\x00", 6)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_pauseProKey)

        data.PVZ_memory.write_bytes(0x00415DF0, b"\x80\x8d\x64\x01\x00\x00\x00", 7)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_pause)

        data.PVZ_memory.write_bytes(0x0041AABE, b"\x83\xbd\x48\x57\x00\x00\x00", 7)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_draw)


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
            specialEffects_asm.mov_exx_dword_ptr(asm.ESI, 0x006A9EC0)
            specialEffects_asm.mov_exx_dword_ptr_eyy_add_dword(asm.ESI, asm.ESI, 0x820)
            specialEffects_asm.mov_exx_dword_ptr_eyy(asm.ESI, asm.ESI)
            specialEffects_asm.call(0x00518A70)
            return specialEffects_asm

    asm.runThread(specialEffects(id, x, y))


def morph_all_plant():
    print(1)
    plant_list = []
    try:
        plant_num = data.PVZ_memory.read_int(
            data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x768)
            + 0xBC
        )
    except:
        return
    i = 0
    j = 0
    while i < plant_num:
        plant_addresss = (
            data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(
                    data.PVZ_memory.read_int(data.baseAddress) + 0x768
                )
                + 0xAC
            )
            + 0x204 * j
        )
        plant_exist = data.PVZ_memory.read_bytes(plant_addresss + 0x141, 1)
        if plant_exist == b"\x00":
            plant_list.append(data.plant(plant_addresss))
            i = i + 1
        j = j + 1
    for p in plant_list:
        plantType = random.randint(0, 96)
        if plantType >= 48:
            plantType = plantType + 27
        if plantType == 118:
            plantType = 123
        if plantType == 11:
            plantType = 123
        if plantType == 45:
            plantType = 123
        if plantType == 110:
            plantType = 38
        if plantType == 105:
            plantType = 21
        if plantType == 108:
            plantType = 10
        if plantType == 112:
            plantType = 43
        if plantType == 113:
            plantType = 78
        putPlant(p.row, p.col, plantType)
        p.setExist(True)


def plantInvincible(f):
    PlantsConotExplodeDeath(f)
    PlantConnotBurnedDeath(f)
    PlantConnotBitedDeath(f)
    PlantConnotCrushedDeath(f)
    PlantConnotHitedDeath(f)
    PlantConnotStolen(f)


def PlantsConotExplodeDeath(f):
    if f:
        data.PVZ_memory.write_bytes(0x0041CC2F, b"\xeb", 1)
    else:
        data.PVZ_memory.write_bytes(0x0041CC2F, b"\x74", 1)


def PlantConnotBurnedDeath(f):
    if f:
        data.PVZ_memory.write_bytes(0x005276EA, b"\xeb", 1)
    else:
        data.PVZ_memory.write_bytes(0x005276EA, b"\x75", 1)


def PlantConnotBitedDeath(f):
    if f:
        data.PVZ_memory.write_bytes(0x0052FCF3, b"\x00", 1)
    else:
        data.PVZ_memory.write_bytes(0x0052FCF3, b"\xfc", 1)


def PlantConnotCrushedDeath(f):
    if f:
        data.PVZ_memory.write_bytes(0x0052E93B, b"\xeb", 1)
    else:
        data.PVZ_memory.write_bytes(0x0052E93B, b"\x74", 1)


def PlantConnotHitedDeath(f):
    if f:
        data.PVZ_memory.write_bytes(0x0046CFEB, b"\x90\x90\x90", 3)
        data.PVZ_memory.write_bytes(0x0046D7A6, b"\x90\x90\x90", 3)
        data.PVZ_memory.write_bytes(0x0084F15D, b"\x90\x90\x90", 3)
        data.PVZ_memory.write_bytes(0x0046CFEB, b"\x90\x90\x90", 3)
    else:
        data.PVZ_memory.write_bytes(0x0046CFEB, b"\x29\x50\x40", 3)
        data.PVZ_memory.write_bytes(0x0046D7A6, b"\x29\x50\x40", 3)
        data.PVZ_memory.write_bytes(0x0084F15D, b"\x29\x50\x40", 3)
        data.PVZ_memory.write_bytes(0x0046CFEB, b"\x29\x50\x40", 3)


def PlantConnotStolen(f):
    if f:
        data.PVZ_memory.write_bytes(0x00524D33, b"\xeb", 1)
    else:
        data.PVZ_memory.write_bytes(0x00524D33, b"\x74", 1)


def fogDraw(f):
    if f:
        data.PVZ_memory.write_bytes(0x0086E521, b"\x0f\x80", 2)
    else:
        data.PVZ_memory.write_bytes(0x0086E521, b"\x0f\x84", 2)


def invisibleDraw(f):
    if f:
        data.PVZ_memory.write_bytes(0x0086E56C, b"\x70", 1)
    else:
        data.PVZ_memory.write_bytes(0x0086E56C, b"\x74", 1)


def bossHPDraw(f):
    global newmem_resetBossNum
    global newmem_bossNum
    global newmem_bossHPDraw
    if f:
        newmem_resetBossNum = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 64
        )
        newmem_bossNum = pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 4)
        newmem_bossHPDraw = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 512
        )
        resetBossNumcode = asm.Asm(newmem_resetBossNum)
        resetBossNumcode.mov_dword_ptr_dword(newmem_bossNum, 0)
        resetBossNumcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.EDX, 0x768)
        resetBossNumcode.jmp(0x0086E553)
        data.PVZ_memory.write_bytes(
            newmem_resetBossNum,
            bytes(resetBossNumcode.code[: resetBossNumcode.index]),
            resetBossNumcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x0086E54D,
            b"\xe9"
            + calculate_call_address(newmem_resetBossNum - 0x0086E552)
            + b"\x90",
            6,
        )
        bossHPDrawcode = asm.Asm(newmem_bossHPDraw)
        bossHPDrawcode.jne_long_offset(0x95)
        bossHPDrawcode.push_exx(asm.EAX)
        bossHPDrawcode.mov_exx(asm.EAX, 0)
        bossHPDrawcode.add_exx_ptr_dword(asm.EAX, 0x00700104)
        bossHPDrawcode.sub_exx_ptr_dword(asm.EAX, 0x00700100)
        bossHPDrawcode.mov_dword_ptr_exx(0x00700B40, asm.EAX)
        bossHPDrawcode.pop_exx(asm.EAX)
        bossHPDrawcode.pushad()
        bossHPDrawcode.pushad()
        bossHPDrawcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EBX, 0xC8)
        bossHPDrawcode.mov_exx_eyy(asm.ECX, asm.EAX)
        bossHPDrawcode.lea_exx_dword_ptr(asm.EDX, newmem_bossHPDraw + 0xA9)
        bossHPDrawcode.call(0x5B0280)
        bossHPDrawcode.popad()
        bossHPDrawcode.push_dword(newmem_bossHPDraw + 0xA4)
        bossHPDrawcode.mov_exx(asm.ECX, 0x00700B00)
        bossHPDrawcode.call(0x00404300)
        bossHPDrawcode.popad()
        bossHPDrawcode.pushad()
        bossHPDrawcode.mov_exx_dword_ptr(asm.EAX, newmem_bossNum)
        bossHPDrawcode.inc_exx(asm.EAX)
        bossHPDrawcode.mov_dword_ptr_exx(newmem_bossNum, asm.EAX)
        bossHPDrawcode.mov_exx_eyy(asm.EBX, asm.EAX)
        bossHPDrawcode.mov_exx_eyy(asm.EDX, asm.EBX)
        bossHPDrawcode.imul_exx_eyy_byte(asm.EDX, asm.EDX, 20)
        bossHPDrawcode.add_exx_dword(asm.EDX, 250)
        bossHPDrawcode.push_exx(asm.EDX)
        bossHPDrawcode.push_dword(640)
        bossHPDrawcode.push_dword(0x00700B00)
        bossHPDrawcode.mov_exx_eyy(asm.EAX, asm.EDI)
        bossHPDrawcode.mov_exx_dword_ptr(asm.EBX, 0x006A7314)
        bossHPDrawcode.mov_ptr_exx_add_byte_eyy(asm.EDI, 0x40, asm.EBX)
        bossHPDrawcode.mov_ptr_exx_add_byte_dword(asm.EDI, 0x30, 0xFF)
        bossHPDrawcode.mov_ptr_exx_add_byte_dword(asm.EDI, 0x34, 0x00)
        bossHPDrawcode.mov_ptr_exx_add_byte_dword(asm.EDI, 0x38, 0x00)
        bossHPDrawcode.mov_ptr_exx_add_byte_dword(asm.EDI, 0x3C, 0xFF)
        bossHPDrawcode.call(0x00587120)
        bossHPDrawcode.popad()
        bossHPDrawcode.jmp(0x0086E553)
        bossHPDrawcode.cmp_byte_ptr_exx_add_byte_byte(asm.EBX, 0x18, 0)
        bossHPDrawcode.jmp(0x0086E56C)
        bossHPDrawcode.add_byte(0xBD)
        bossHPDrawcode.add_byte(0xA9)
        bossHPDrawcode.add_byte(0xCD)
        bossHPDrawcode.add_byte(0xF5)
        bossHPDrawcode.add_byte(0xD1)
        bossHPDrawcode.add_byte(0xAA)
        bossHPDrawcode.add_byte(0xC1)
        bossHPDrawcode.add_byte(0xBF)
        bossHPDrawcode.add_byte(0x3A)
        bossHPDrawcode.add_byte(0x00)
        data.PVZ_memory.write_bytes(
            newmem_bossHPDraw,
            bytes(bossHPDrawcode.code[: bossHPDrawcode.index]),
            bossHPDrawcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x0086E566,
            b"\xe9" + calculate_call_address(newmem_bossHPDraw - 0x0086E56B) + b"\x90",
            6,
        )
    else:
        data.PVZ_memory.write_bytes(0x0086E54D, b"\x8b\x92\x68\x07\x00\x00", 6)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_resetBossNum)
        data.PVZ_memory.write_bytes(0x0086E566, b"\x74\xeb\x80\x7b\x18\x00", 6)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_bossHPDraw)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_bossNum)


def spawisModified():
    global newmem_spawisModified
    if (
        newmem_modifySpawNum is not None
        or newmem_globalSpawModify is not None
        or newmem_modifySpawMultiplier is not None
    ):
        newmem_spawisModified = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_spawisModified)
        shellcode.push_exx(asm.EAX)
        shellcode.mov_exx(asm.EAX, 0)
        shellcode.add_exx_ptr_dword(asm.EAX, 0x00700104)
        shellcode.sub_exx_ptr_dword(asm.EAX, 0x00700100)
        shellcode.mov_dword_ptr_exx(0x00700B40, asm.EAX)
        shellcode.pop_exx(asm.EAX)
        shellcode.pushad()
        shellcode.push_dword(newmem_spawisModified + 0x79)
        shellcode.mov_exx(asm.ECX, 0x00700B00)
        shellcode.call(0x00404300)
        shellcode.popad()
        shellcode.pushad()
        shellcode.push_dword(550)
        shellcode.push_dword(720)
        shellcode.push_dword(0x00700B00)
        shellcode.mov_exx_eyy(asm.EAX, asm.EDI)
        shellcode.mov_exx_dword_ptr(asm.EBX, 0x006A7314)
        shellcode.mov_ptr_exx_add_byte_eyy(asm.EDI, 0x40, asm.EBX)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EDI, 0x30, 0x66)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EDI, 0x34, 0xCC)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EDI, 0x38, 0xFF)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EDI, 0x3C, 0xFF)
        shellcode.call(0x00587120)
        shellcode.popad()
        shellcode.jmp_dword_offest(0)
        shellcode.push_exx(asm.EDI)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESP, 0x7C, 0xF)
        shellcode.jmp(0x00417DC9)
        shellcode.add_byte(0xB9)
        shellcode.add_byte(0xD8)
        shellcode.add_byte(0xBF)
        shellcode.add_byte(0xA8)
        shellcode.add_byte(0xB3)
        shellcode.add_byte(0xF6)
        shellcode.add_byte(0xB9)
        shellcode.add_byte(0xD6)
        shellcode.add_byte(0xD2)
        shellcode.add_byte(0xD1)
        shellcode.add_byte(0xB8)
        shellcode.add_byte(0xFC)
        shellcode.add_byte(0xB8)
        shellcode.add_byte(0xC4)
        shellcode.add_byte(0x00)
        data.PVZ_memory.write_bytes(
            newmem_spawisModified,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x00417DC0,
            b"\xe9"
            + calculate_call_address(newmem_spawisModified - 0x00417DC5)
            + b"\x90\x90\x90\x90",
            9,
        )
    else:
        data.PVZ_memory.write_bytes(
            0x00417DC0, b"\x57\xc7\x44\x24\x7c\x0f\x00\x00\x00", 9
        )
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_spawisModified)


def modifySpawNum(f, num):
    global newmem_modifySpawNum
    if f:
        newmem_modifySpawNum = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_modifySpawNum)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EAX, 0x5564, num * 10)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.EAX, 0x5564)
        shellcode.jmp(0x0043A25A)
        data.PVZ_memory.write_bytes(
            newmem_modifySpawNum,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x0043A254,
            b"\xe9"
            + calculate_call_address(newmem_modifySpawNum - 0x0043A259)
            + b"\x90",
            6,
        )
        spawisModified()
    else:
        data.PVZ_memory.write_bytes(0x0043A254, b"\x8b\x88\x64\x55\x00\x00", 6)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_modifySpawNum)
        # newmem_modifySpawNum = None


def modifySpawMultiplier(f, mult):
    divzero(1)
    unlimitedMonsterSpawning(1)
    global newmem_modifySpawMultiplier
    if f:
        newmem_modifySpawMultiplier = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_modifySpawMultiplier)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESP, 0x24, mult)
        shellcode.jmp(0x00409968)
        data.PVZ_memory.write_bytes(
            newmem_modifySpawMultiplier,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x00409893,
            b"\xe9"
            + calculate_call_address(newmem_modifySpawMultiplier - 0x00409898)
            + b"\x90",
            6,
        )
        spawisModified()
    else:
        data.PVZ_memory.write_bytes(0x00409893, b"\xe9\x68\x37\x46\x00\x90", 6)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_modifySpawMultiplier
        )


def globalSpawModify(f, zombieTypes):
    divzero(1)
    unlimitedMonsterSpawning(1)
    global newmem_globalSpawModify
    if f:
        data.PVZ_memory.write_bytes(0x00425855, b"\xeb", 1)
        data.PVZ_memory.write_bytes(0x0042584E, b"\x90\x90\x90\x90\x90", 5)
        newmem_globalSpawModify = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_globalSpawModify)
        for i in range(0, 42):
            if str(i) in zombieTypes:
                shellcode.mov_byte_ptr_exx_add_dword_byte(asm.EDX, 0x57D4 + i, 1)
            else:
                shellcode.mov_byte_ptr_exx_add_dword_byte(asm.EDX, 0x57D4 + i, 0)

        shellcode.jmp(0x00425D1D)
        data.PVZ_memory.write_bytes(
            newmem_globalSpawModify,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x00820CFF,
            b"\xe9"
            + calculate_call_address(newmem_globalSpawModify - 0x00820D04)
            + b"\x90",
            6,
        )
        spawisModified()
    else:
        data.PVZ_memory.write_bytes(0x00425855, b"\x7f", 1)
        data.PVZ_memory.write_bytes(0x0042584E, b"\xe9\xed\x9f\x42\x00", 5)
        data.PVZ_memory.write_bytes(0x00820CFF, b"\x0f\x85\x21\x00\x00\x00", 6)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_globalSpawModify
        )
        # newmem_globalSpawModify = None


def changeZombieHead(f, zombieType):
    print("changehead" + str(f))
    global newmem_changeZombieHead
    global newmem_changeZombieDeadHead
    if f:
        newmem_changeZombieHead = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_changeZombieHead)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x24, zombieType)
        shellcode.jne_long_offset(0x4E)
        shellcode.pushad()
        shellcode.mov_exx_eyy(asm.EAX, asm.ESI)
        shellcode.push_byte(0xFF)
        shellcode.push_dword(0x0065851C)
        shellcode.call(0x005331C0)
        shellcode.mov_exx_eyy(asm.EAX, asm.ESI)
        shellcode.push_byte(0xFF)
        shellcode.push_dword(0x00658110)
        shellcode.call(0x005331C0)
        shellcode.mov_exx_dword_ptr_eyy(asm.EAX, asm.ESI)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.EAX, 0x820)
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EDX, asm.ECX, 0x8)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ESI, 0x118)
        shellcode.and_eax_dword(0xFFFF)
        shellcode.lea_exx_eyy_ezz_times(asm.EBX, asm.EAX, asm.EAX, 4)
        shellcode.shl_exx_byte(asm.EBX, 5)
        shellcode.add_exx_ptr_eyy(asm.EBX, asm.EDX)
        shellcode.push_dword_ptr(0x006A7A08)
        shellcode.mov_exx(asm.EAX, 0x00658500)
        shellcode.mov_exx_eyy(asm.ECX, asm.EBX)
        shellcode.call(0x00473490)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EAX, asm.ESI, 0x58)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x54, 0xFF)
        shellcode.jmp(0x0052AF92)
        data.PVZ_memory.write_bytes(
            newmem_changeZombieHead,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x0052AF8B,
            b"\xe9"
            + calculate_call_address(newmem_changeZombieHead - 0x0052AF90)
            + b"\x90\x90",
            7,
        )
        newmem_changeZombieDeadHead = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256
        )
        shellcode2 = asm.Asm(newmem_changeZombieDeadHead)
        shellcode2.cmp_exx_byte(asm.EAX, zombieType)
        shellcode2.jne_long_offset(0xB)
        shellcode2.mov_exx_dword_ptr(asm.ESI, 0x006A7A08)
        shellcode2.jmp(0x00529D07)
        shellcode2.cmp_exx_byte(asm.EAX, 0x23)
        shellcode2.jne(0x0084E4E4)
        shellcode2.jmp(0x0084E4D9)
        data.PVZ_memory.write_bytes(
            newmem_changeZombieDeadHead,
            bytes(shellcode2.code[: shellcode2.index]),
            shellcode2.index,
        )
        data.PVZ_memory.write_bytes(
            0x0084E4D0,
            b"\xe9"
            + calculate_call_address(newmem_changeZombieDeadHead - 0x0084E4D5)
            + b"\x90\x90\x90\x90",
            9,
        )
    else:
        data.PVZ_memory.write_bytes(0x0052AF8B, b"\x8b\x46\x58\x83\x46\x54\xff", 7)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_changeZombieHead
        )
        data.PVZ_memory.write_bytes(
            0x0084E4D0, b"\x83\xf8\x23\x0f\x85\x0b\x00\x00\x00", 9
        )
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_changeZombieDeadHead
        )


def deathrattleCallZombie(f, deadZombieType):
    global newmem_deathrattleCallZombie
    if f:
        newmem_deathrattleCallZombie = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_deathrattleCallZombie)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBP, 0x24, deadZombieType)
        shellcode.jne_long_offset(0xB0)
        shellcode.pushad()
        shellcode.push_byte(0x47)
        shellcode.push_dword(0x00061A80)
        shellcode.sub_exx_byte(asm.ESP, 0x10)
        shellcode.mov_ptr_exx_dword(asm.ESP, 0x28)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESP, 4, 0x28)
        shellcode.fild_dword_ptr_exx_add_byte(asm.EBP, 0x0C)
        shellcode.fiadd_ptr_exx(asm.ESP)
        shellcode.fstp_dword_ptr_exx_add_byte(asm.ESP, 0xC)
        shellcode.fild_dword_ptr_exx_add_byte(asm.EBP, 0x08)
        shellcode.fiadd_ptr_exx_add_byte(asm.ESP, 4)
        shellcode.fstp_dword_ptr_exx_add_byte(asm.ESP, 0x8)
        shellcode.mov_exx_dword_ptr(asm.ESI, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ESI, asm.ESI, 0x820)
        shellcode.mov_exx_dword_ptr_eyy(asm.ESI, asm.ESI)
        shellcode.add_exx_byte(asm.ESP, 8)
        shellcode.call(0x00518A70)
        shellcode.popad()
        shellcode.pushad()
        shellcode.mov_exx_eyy(asm.EDI, asm.EBP)
        shellcode.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
        shellcode.cmp_dword_ptr_exx_add_dword_byte(asm.EAX, 0x7FC, 3)
        shellcode.jne_long_offset(0x4C)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x768)
        shellcode.cmp_byte_ptr_exx_add_dword_byte(asm.EAX, 0x164, 1)
        shellcode.je_offset(0x39)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EDI, 0x24, deadZombieType)
        shellcode.jne_long_offset(0x2F)
        shellcode.mov_exx(asm.EAX, 42)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_byte(asm.EAX, 25)
        shellcode.je_offset(0x1C)
        shellcode.push_ptr_exx_add_byte(asm.EDI, 0x1C)
        shellcode.push_exx(asm.EAX)
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EAX, asm.EDI, 4)
        shellcode.call(0x0040DDC0)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EDI, 0x2C)
        shellcode.fstp_dword_ptr_exx_add_byte(asm.EAX, 0x2C)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EAX, 0x1B0, 1)
        shellcode.popad()
        shellcode.mov_ptr_exx_add_byte_dword(asm.EBP, 0x28, 3)
        shellcode.push_exx(asm.EBP)
        shellcode.mov_exx_eyy(asm.EBP, asm.ESP)
        shellcode.add_byte(0x83)
        shellcode.add_byte(0xE4)
        shellcode.add_byte(0xF8)
        shellcode.jmp(0x00529A36)
        data.PVZ_memory.write_bytes(
            newmem_deathrattleCallZombie,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x00529A30,
            b"\xe9"
            + calculate_call_address(newmem_deathrattleCallZombie - 0x00529A35)
            + b"\x90",
            6,
        )
    else:
        data.PVZ_memory.write_bytes(0x00529A30, b"\x55\x8b\xec\x83\xe4\xf8", 6)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_deathrattleCallZombie
        )


def reserveMaterialDropAllCard(f, zombieWeight, lmpWeight):
    global newmem_reserveMaterialDropAllCard
    if f:
        newmem_reserveMaterialDropAllCard = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_reserveMaterialDropAllCard)
        shellcode.mov_exx(asm.EAX, 99)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_byte(asm.EAX, zombieWeight)
        shellcode.jl_long_offset(0x34)
        shellcode.mov_exx(asm.EAX, 99)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_byte(asm.EAX, 50)
        shellcode.jl_long_offset(0x12)
        shellcode.mov_exx(asm.EAX, 49)
        shellcode.call(0x005AF400)
        shellcode.add_exx_byte(asm.EAX, 75)
        shellcode.jmp_dword_offest(0x3B)
        shellcode.mov_exx(asm.EAX, 48)
        shellcode.call(0x005AF400)
        shellcode.jmp_dword_offest(0x2C)
        shellcode.mov_exx(asm.EAX, 99)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_byte(asm.EAX, lmpWeight)
        shellcode.jl_long_offset(0x14)
        shellcode.mov_exx(asm.EAX, 42)
        shellcode.call(0x005AF400)
        shellcode.add_exx_dword(asm.EAX, 0x100)
        shellcode.jmp_dword_offest(0x5)
        shellcode.mov_exx(asm.EAX, 0x118)
        shellcode.cmp_exx_byte(asm.EAX, 18)
        shellcode.je_offset(0xFFFFFF84)
        shellcode.cmp_exx_byte(asm.EAX, 47)
        shellcode.je_offset(0xFFFFFF7B)
        shellcode.cmp_exx_byte(asm.EAX, 112)
        shellcode.je_offset(0xFFFFFF72)
        shellcode.cmp_exx_byte(asm.EAX, 113)
        shellcode.je_offset(0xFFFFFF69)
        shellcode.cmp_exx_byte(asm.EAX, 114)
        shellcode.je_offset(0xFFFFFF60)
        shellcode.cmp_exx_byte(asm.EAX, 118)
        shellcode.je_offset(0xFFFFFF57)
        shellcode.mov_ptr_exx_add_byte_eyy(asm.EBX, 0x68, asm.EAX)
        shellcode.popad()
        shellcode.pushad()
        shellcode.jmp(0x008689F7)
        data.PVZ_memory.write_bytes(
            newmem_reserveMaterialDropAllCard,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x008689F2,
            b"\xe9"
            + calculate_call_address(newmem_reserveMaterialDropAllCard - 0x008689F7),
            5,
        )
    else:
        data.PVZ_memory.write_bytes(0x008689F2, b"\x89\x43\x68\x61\x60", 5)
        pymem.memory.free_memory(
            data.PVZ_memory.process_handle, newmem_reserveMaterialDropAllCard
        )


def creatBullet(bullets_list):
    class bulletCreat:
        def __init__(self, bullets_list):
            pass

        def creat_asm(self, startAddress):
            bulletCreat_asm = asm.Asm(startAddress)
            for bullet_params in bullets_list:
                # 提取子弹的参数
                bullet_type, x, y, v_x, v_y = bullet_params
                bulletCreat_asm.pushad()
                bulletCreat_asm.push_byte(bullet_type)
                bulletCreat_asm.push_byte(0)
                bulletCreat_asm.push_dword(400000)
                bulletCreat_asm.push_dword(y)
                bulletCreat_asm.push_dword(x)
                bulletCreat_asm.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
                bulletCreat_asm.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x768)
                bulletCreat_asm.call(0x0040D620)
                bulletCreat_asm.mov_ptr_exx_add_byte_dword(asm.EAX, 0x58, 7)
                bulletCreat_asm.mov_ptr_exx_add_byte_float(asm.EAX, 0x3C, v_x)
                bulletCreat_asm.mov_ptr_exx_add_byte_float(asm.EAX, 0x40, v_y)
                bulletCreat_asm.mov_ptr_exx_add_dword_dword(asm.EAX, 0x88, 1)
                bulletCreat_asm.mov_byte_ptr_exx_add_byte_byte(asm.EAX, 0x74, 1)
                bulletCreat_asm.popad()
            return bulletCreat_asm

    asm.runThread(bulletCreat(bullets_list))


def clearCards(type):
    try:
        card_num = data.PVZ_memory.read_int(
            data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x768)
            + 0xF4
        )
        print(card_num)
    except:
        return
    i = 0
    j = 0
    while i < card_num:
        card_addresss = (
            data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(
                    data.PVZ_memory.read_int(data.baseAddress) + 0x768
                )
                + 0xE4
            )
            + 0x104 * j
        )
        card_exist = data.PVZ_memory.read_bytes(card_addresss + 0x38, 1)
        if card_exist == b"\x00":
            card_plant_type = data.PVZ_memory.read_int(card_addresss + 0x68)
            if type == 0:
                if card_plant_type < 255:
                    data.PVZ_memory.write_bytes(card_addresss + 0x38, b"\x01", 1)
                    data.PVZ_memory.write_bytes(card_addresss + 0x3C, b"\x01", 1)
            elif type == 1:
                if card_plant_type > 255:
                    data.PVZ_memory.write_bytes(card_addresss + 0x38, b"\x01", 1)
                    data.PVZ_memory.write_bytes(card_addresss + 0x3C, b"\x01", 1)
            i = i + 1
        j = j + 1


def cardsNotDisappear(f):
    if f:
        data.PVZ_memory.write_bytes(0x00430DD1, b"\x00", 1)
    else:
        data.PVZ_memory.write_bytes(0x00430DD1, b"\x01", 1)


def lockLevel(f, level):
    divzero(1)
    unlimitedMonsterSpawning(1)
    global newmem_lockLevel
    if f:
        newmem_lockLevel = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_lockLevel)
        shellcode.mov_exx(asm.EAX, level)
        shellcode.mov_ptr_exx_add_dword_eyy(asm.ESI, 0x7F8, asm.EAX)
        shellcode.jmp(0x0044F587)
        data.PVZ_memory.write_bytes(
            newmem_lockLevel,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x0044F581,
            b"\xe9" + calculate_call_address(newmem_lockLevel - 0x0044F586) + b"\x90",
            6,
        )
    else:
        data.PVZ_memory.write_bytes(0x0044F581, b"\x89\x86\xf8\x07\x00\x00", 6)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_lockLevel)


def divzero(f):
    global newmem_divzero
    if f:
        print("divzero")
        newmem_divzero = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256
        )
        shellcode2 = asm.Asm(newmem_divzero)
        shellcode2.cmp_dword_ptr_exx_add_byte_byte(asm.ESP, 0x4, 0)
        shellcode2.jne_long_offset(0x8)
        shellcode2.mov_ptr_exx_add_byte_dword(asm.ESP, 0x4, 1)
        shellcode2.add_byte(0xF7)
        shellcode2.add_byte(0x74)
        shellcode2.add_byte(0x24)
        shellcode2.add_byte(0x04)  # div [esp+4]
        shellcode2.mov_exx_eyy(asm.EAX, asm.EDX)
        shellcode2.jmp(0x005A9A4D)
        data.PVZ_memory.write_bytes(
            newmem_divzero,
            bytes(shellcode2.code[: shellcode2.index]),
            shellcode2.index,
        )
        data.PVZ_memory.write_bytes(
            0x005A9A47,
            b"\xe9" + calculate_call_address(newmem_divzero - 0x005A9A4C) + b"\x90",
            6,
        )
    else:
        data.PVZ_memory.write_bytes(0x005A9A47, b"\xf7\x74\x24\x04\x8b\xc2", 6)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_divzero)


def unlimitedMonsterSpawning(f):
    if f:
        data.PVZ_memory.write_bytes(0x0041C078, b"\xeb", 1)
        data.PVZ_memory.write_bytes(0x0040D91F, b"\xeb", 1)
    else:
        data.PVZ_memory.write_bytes(0x0041C078, b"\x74", 1)
        data.PVZ_memory.write_bytes(0x0040D91F, b"\x74", 1)


def bungeeFix(f):
    global newmem_bungeeTipFix
    global newmem_bungeePutFix
    if f:
        newmem_bungeeTipFix = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_bungeeTipFix)
        shellcode.cmp_dword_ptr_exx_add_byte_dword(asm.ECX, 0x28, 276)
        shellcode.jne(0x0042A35A)
        shellcode.jmp(0x0042A2F5)
        data.PVZ_memory.write_bytes(
            newmem_bungeeTipFix,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        data.PVZ_memory.write_bytes(
            0x0042A2EF,
            b"\xe9"
            + calculate_call_address(newmem_bungeeTipFix - 0x0042A2F4)
            + b"\x90",
            6,
        )
        newmem_bungeePutFix = pymem.memory.allocate_memory(
            data.PVZ_memory.process_handle, 256
        )
        shellcode2 = asm.Asm(newmem_bungeePutFix)
        shellcode2.cmp_exx_dword(asm.EBP, 276)
        shellcode2.jne(0x004255F2)
        shellcode2.jmp(0x004255E6)
        data.PVZ_memory.write_bytes(
            newmem_bungeePutFix,
            bytes(shellcode2.code[: shellcode2.index]),
            shellcode2.index,
        )
        data.PVZ_memory.write_bytes(
            0x004255E1,
            b"\xe9" + calculate_call_address(newmem_bungeePutFix - 0x004255E6),
            5,
        )
    else:
        data.PVZ_memory.write_bytes(0x0042A2EF, b"\x83\x79\x28\x42\x75\x65", 6)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_bungeeTipFix)
        data.PVZ_memory.write_bytes(0x004255E1, b"\x83\xfd\x42\x75\x0c", 5)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_bungeePutFix)


def setZombieRedLine(row):
    print(row)
    data.PVZ_memory.write_int(0x004255DD, row)
    data.PVZ_memory.write_int(0x004253F7, 20 + row * 80)


def findBoss():
    bossList = []
    try:
        zombie_num = data.PVZ_memory.read_int(
            data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress) + 0x768)
            + 0xA0
        )
    except:
        return
    i = 0
    j = 0
    while i < zombie_num:
        zombie_addresss = (
            data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(
                    data.PVZ_memory.read_int(data.baseAddress) + 0x768
                )
                + 0x90
            )
            + 0x204 * j
        )
        zombie_exist = data.PVZ_memory.read_bytes(zombie_addresss + 0xEC, 1)
        if zombie_exist == b"\x00":
            z = data.zombie(zombie_addresss)
            if z.type == 25:
                bossList.append(z)
            i = i + 1
        j = j + 1
    return bossList


def nightSun(f):
    if f:
        data.PVZ_memory.write_bytes(0x0040B196, b"\xeb\x14", 2)
        data.PVZ_memory.write_bytes(
            0x00413A76, b"\x90\x90\x90\x53\x57\xeb\x28\x90\x90\x90\x90", 11
        )
    else:
        data.PVZ_memory.write_bytes(0x0040B196, b"\x74\x29", 2)
        data.PVZ_memory.write_bytes(
            0x00413A76, b"\x83\xf8\x01\x53\x57\x0f\x84\x70\x01\x00\x00", 11
        )
