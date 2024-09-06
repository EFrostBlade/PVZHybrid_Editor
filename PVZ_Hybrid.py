# ruff: noqa: E722
import ctypes
import pymem.ressources.kernel32
import pymem.ressources.structure
import pymem.thread
import pymem.memory
from threading import Thread, Event
import random
import time
import os
import struct

import PVZ_asm as asm
import PVZ_data


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
        map = PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(0x006A9EC0) + 0x768
            )
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
            or map == 24
            or map == 27
            or map == 30
            or map == 31
            or map == 32
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
            or map == 25
            or map == 26
        ):
            return 6
        else:
            return 5
    except:  # noqa: E722
        return False


def getDifficult():
    difficultAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x428
    )
    difficultValue = PVZ_data.PVZ_memory.read_int(difficultAddr)
    if difficultValue == -1:
        return 1
    if difficultValue == 0:
        return 2
    if difficultValue == 1:
        return 3


def setDifficult(difficult):
    difficultAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x428
    )
    if difficult == 1:
        PVZ_data.PVZ_memory.write_int(difficultAddr, 4294967295)
    if difficult == 2:
        PVZ_data.PVZ_memory.write_int(difficultAddr, 0)
    if difficult == 3:
        PVZ_data.PVZ_memory.write_int(difficultAddr, 1)


def getState():
    try:
        game_state = PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x7FC
        )
        return game_state  # 1主菜单 2选局内  5帮助  7关卡选择
    except:
        return False


def getNowFlag():
    try:
        nowFlag = PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
            )
            + 0x557C
        )
        return nowFlag
    except:
        return False


def getRandomZombie(hasBoss=False):
    if PVZ_data.PVZ_version == 0:
        zombieType = random.randint(0, 32)
    elif PVZ_data.PVZ_version == 2.0:
        zombieType = random.randint(0, 41)
    elif PVZ_data.PVZ_version == 2.1:
        zombieType = random.randint(0, 44)
    elif PVZ_data.PVZ_version == 2.2:
        zombieType = random.randint(0, 50)
    elif PVZ_data.PVZ_version == 2.3:
        zombieType = random.randint(0, 55)
    elif (
        PVZ_data.PVZ_version == 2.35
        or PVZ_data.PVZ_version == 2.36
        or PVZ_data.PVZ_version == 2.37
    ):
        zombieType = random.randint(0, 58)
    elif PVZ_data.PVZ_version == 2.4:
        zombieType = random.randint(0, 63)
    if hasBoss is True:
        return zombieType
    else:
        if zombieType == 25:
            zombieType = getRandomZombie(False)
        return zombieType


def getRandomPlant(isPut=False):
    if PVZ_data.PVZ_version == 0:
        plantType = random.randint(0, 47)
    elif PVZ_data.PVZ_version == 2.0:
        plantType = random.randint(0, 96)
    elif PVZ_data.PVZ_version == 2.1:
        plantType = random.randint(0, 103)
    elif PVZ_data.PVZ_version == 2.2:
        plantType = random.randint(0, 108)
    elif PVZ_data.PVZ_version == 2.3:
        plantType = random.randint(0, 122)
    elif (
        PVZ_data.PVZ_version == 2.35
        or PVZ_data.PVZ_version == 2.36
        or PVZ_data.PVZ_version == 2.37
    ):
        plantType = random.randint(0, 133)
    elif PVZ_data.PVZ_version == 2.4:
        plantType = random.randint(0, 139)
    if plantType >= 48:
        plantType = plantType + 27
    if isPut is False:
        return plantType
    else:
        ExcludedCards = [105, 112, 113, 118, 133, 144, 151, 157]
        while plantType in ExcludedCards:
            plantType = getRandomPlant(True)
        return plantType


def getPlantList():
    plant_list = []
    try:
        plant_num = PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
            )
            + 0xBC
        )
    except:
        return
    i = 0
    j = 0
    while i < plant_num:
        plant_addresss = (
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0xAC
            )
            + 0x204 * j
        )
        plant_exist = PVZ_data.PVZ_memory.read_bytes(plant_addresss + 0x141, 1)
        if plant_exist == b"\x00":
            plant_list.append(PVZ_data.plant(plant_addresss))
            i = i + 1
        j = j + 1
    return plant_list


def getZombieList():
    zombie_list = []
    try:
        zombie_num = PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
            )
            + 0xA0
        )
    except:
        return
    i = 0
    j = 0
    while i < zombie_num:
        zombie_addresss = (
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0x90
            )
            + 0x204 * j
        )
        zombie_exist = PVZ_data.PVZ_memory.read_bytes(zombie_addresss + 0xEC, 1)
        if zombie_exist == b"\x00":
            zombie_list.append(PVZ_data.zombie(zombie_addresss))
            i = i + 1
        j = j + 1
    return zombie_list


def getItemList():
    item_list = []
    try:
        item_num = PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
            )
            + 0x12C
        )
    except:
        return
    i = 0
    j = 0
    while i < item_num:
        item_addresss = (
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0x11C
            )
            + 0x1EC * j
        )
        item_exist = PVZ_data.PVZ_memory.read_bytes(item_addresss + 0x20, 1)
        if item_exist == b"\x00":
            item_list.append(PVZ_data.item(item_addresss))
            i = i + 1
        j = j + 1
    return item_list


def backGround(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x0054EBEF, b"\xc3", 1)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0054EBEF, b"\x57", 1)


def getSun():
    sunAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
        )
        + 0x5560
    )
    sunNow = PVZ_data.PVZ_memory.read_int(sunAddr)
    return sunNow


def addSun(sunIncrement):
    sunAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
        )
        + 0x5560
    )
    sunNow = PVZ_data.PVZ_memory.read_int(sunAddr)
    PVZ_data.PVZ_memory.write_int(sunAddr, sunNow + int(sunIncrement))


def subSun(sunDecrement):
    sunAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
        )
        + 0x5560
    )
    sunNow = PVZ_data.PVZ_memory.read_int(sunAddr)
    sun = sunNow - int(sunDecrement)
    PVZ_data.PVZ_memory.write_int(sunAddr, sun)


def setSun(sun):
    sunAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
        )
        + 0x5560
    )
    PVZ_data.PVZ_memory.write_int(sunAddr, int(sun))


def cancalSunFall(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x00413B7C, b"\x90\x90\x90\x90\x90\x90\x90", 7)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00413B7C, b"\x83\x86\x38\x55\x00\x00\xff", 7)


def getSilver():
    silverAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x208
    )
    silverNow = PVZ_data.PVZ_memory.read_int(silverAddr)
    return silverNow


def addSilver(silverIncrement):
    silverAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x208
    )
    silverNow = PVZ_data.PVZ_memory.read_int(silverAddr)
    PVZ_data.PVZ_memory.write_int(silverAddr, silverNow + int(silverIncrement))


def setSilver(silver):
    silverAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x208
    )
    PVZ_data.PVZ_memory.write_int(silverAddr, int(silver))


def getGold():
    goldAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x20C
    )
    goldNow = PVZ_data.PVZ_memory.read_int(goldAddr)
    return goldNow


def addGold(goldIncrement):
    goldAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x20C
    )
    goldNow = PVZ_data.PVZ_memory.read_int(goldAddr)
    PVZ_data.PVZ_memory.write_int(goldAddr, goldNow + int(goldIncrement))


def setGold(gold):
    goldAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x20C
    )
    PVZ_data.PVZ_memory.write_int(goldAddr, int(gold))


def getDiamond():
    diamondAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x210
    )
    diamondNow = PVZ_data.PVZ_memory.read_int(diamondAddr)
    return diamondNow


def addDiamond(diamondIncrement):
    diamondAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x210
    )
    diamondNow = PVZ_data.PVZ_memory.read_int(diamondAddr)
    PVZ_data.PVZ_memory.write_int(diamondAddr, diamondNow + int(diamondIncrement))


def setDiamond(diamond):
    diamondAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x210
    )
    PVZ_data.PVZ_memory.write_int(diamondAddr, int(diamond))


def upperLimit(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x00430A23, b"\xeb", 1)
        PVZ_data.PVZ_memory.write_bytes(0x00430A78, b"\xeb", 1)
        PVZ_data.PVZ_memory.write_bytes(0x0048CAB0, b"\xeb", 1)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00430A23, b"\x7e", 1)
        PVZ_data.PVZ_memory.write_bytes(0x00430A78, b"\x7e", 1)
        PVZ_data.PVZ_memory.write_bytes(0x0048CAB0, b"\x7e", 1)


def pausePro(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(
            0x415DF0, b"\x0f\x1f\x80\x00\x00\x00\x00\x66\x90", 9
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(
            0x415DF0, b"\x80\xbd\x64\x01\x00\x00\x00\x74\x35", 9
        )


def ignoreSun(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x0041BA70, b"\x90\x90\x90\x90\x90\x90", 6)
        PVZ_data.PVZ_memory.write_bytes(
            0x0048881B, b"\xe9\x97\x01\x00\x00\x0f\x1f\x00", 8
        )
        PVZ_data.PVZ_memory.write_bytes(0x0048847F, b"\xeb", 1)
        PVZ_data.PVZ_memory.write_bytes(0x0040F8A2, b"\xeb", 1)
        PVZ_data.PVZ_memory.write_bytes(0x00488565, b"\xeb\x0e\x90\x90", 4)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0041BA70, b"\x39\xc3\x7f\x0c\x29\xde", 6)
        PVZ_data.PVZ_memory.write_bytes(
            0x0048881B, b"\x84\xc0\x0f\x85\x94\x01\x00\x00", 8
        )
        PVZ_data.PVZ_memory.write_bytes(0x0048847F, b"\x75", 1)
        PVZ_data.PVZ_memory.write_bytes(0x0040F8A2, b"\x75", 1)
        PVZ_data.PVZ_memory.write_bytes(0x00488565, b"\x84\xc0\x75\x0c", 4)


def cancelCd(f):
    # if f:
    #     data.PVZ_memory.write_bytes(0x487293, b'\x3b\x47\x28\x90\x90', 5)
    # else:
    #     data.PVZ_memory.write_bytes(0x487296, b'\x7e\x14', 2)
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x487296, b"\x70", 1)
        PVZ_data.PVZ_memory.write_bytes(0x00488250, b"\xeb", 1)
        PVZ_data.PVZ_memory.write_bytes(0x00488E73, b"\xc6\x45\x48\x01", 4)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x487296, b"\x7e", 1)
        PVZ_data.PVZ_memory.write_bytes(0x00488250, b"\x75", 1)
        PVZ_data.PVZ_memory.write_bytes(0x00488E73, b"\xc6\x45\x48\x00", 4)


def zombieInvisible(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x0052E357, b"\x70", 1)
        PVZ_data.PVZ_memory.write_bytes(0x0053402B, b"\x70", 1)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0052E357, b"\x75", 1)
        PVZ_data.PVZ_memory.write_bytes(0x0053402B, b"\x75", 1)


def killAllZombies():
    zomNum = PVZ_data.PVZ_memory.read_int(
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
        )
        + 0xA0
    )
    i = 0
    j = 0
    while i < zomNum:
        zomAddresss = (
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0x90
            )
            + 0x204 * j
        )
        zomExist = PVZ_data.PVZ_memory.read_bytes(zomAddresss + 0xEC, 1)
        if zomExist == b"\x00":
            PVZ_data.PVZ_memory.write_int(zomAddresss + 0x28, 3)
            i = i + 1
        j = j + 1


def autoCollect(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x43158B, b"\x80\x7b\x50\x00\xeb\x08", 6)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x43158B, b"\x80\x7b\x50\x00\x75\x08", 6)


def changeSlot(n, type):
    slotAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
        )
        + 0x144
    )
    PVZ_data.PVZ_memory.write_int(
        PVZ_data.PVZ_memory.read_int(slotAddr) + 0x5C + 0x50 * (n - 1), type
    )


def win():
    winAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
        )
        + 0x55FC
    )
    PVZ_data.PVZ_memory.write_int(winAddr, 1)


def advacedPause(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(
            0x415DF0, b"\x0f\x1f\x80\x00\x00\x00\x00\x66\x90", 9
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(
            0x415DF0, b"\x80\xbd\x64\x01\x00\x00\x00\x74\x35", 9
        )


newmem_unlock = None


def unlock(f):
    global newmem_unlock
    # [ENABLE]
    # //code from here to '[DISABLE]' will be used to enable the cheat
    # alloc(newmem,2048)
    # label(returnhere)
    # label(originalcode)
    # label(exit)

    # newmem: //this is allocated memory, you have read,write,execute access
    # //place your code here

    # mov al,1
    # ret

    # originalcode:
    # jmp 87AE00

    # exit:
    # jmp returnhere

    # "PlantsVsZombies.exe"+53B20:
    # jmp newmem
    # returnhere:

    # [DISABLE]
    # //code from here till the end of the code will be used to disable the cheat
    # dealloc(newmem)
    # "PlantsVsZombies.exe"+53B20:
    # jmp 87AE00
    # //Alt: db E9 4B CF 3E 00
    if f:
        newmem_unlock = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_unlock)
        shellcode.mov_e(asm.AL, 1)
        shellcode.ret()
        PVZ_data.PVZ_memory.write_bytes(
            newmem_unlock,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x00453B20, b"\xe9" + calculate_call_address(newmem_unlock - 0x00453B25), 5
        )
    else:
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_unlock)
        if 2.37 >= PVZ_data.PVZ_version >= 2.3:
            PVZ_data.PVZ_memory.write_bytes(0x00453B20, b"\xe9\x4b\xcf\x3e\x00", 5)
        elif PVZ_data.PVZ_version >= 2.4:
            PVZ_data.PVZ_memory.write_bytes(0x00453B20, b"\xe9\xdb\xc4\x4d\x00", 5)


def shovelpro(f):
    global newmem_shovelpro
    if PVZ_data.PVZ_version == 2.0:
        addr = (
            int.from_bytes(
                PVZ_data.PVZ_memory.read_bytes(0x411141, 1)
                + PVZ_data.PVZ_memory.read_bytes(0x411140, 1)
                + PVZ_data.PVZ_memory.read_bytes(0x41113F, 1)
                + PVZ_data.PVZ_memory.read_bytes(0x41113E, 1)
            )
            + 0x411142
        )
        if f:
            PVZ_data.PVZ_memory.write_bytes(addr + 0x15, b"\xeb\x6a\x90", 3)
            newmem_shovelpro = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 100
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
            PVZ_data.PVZ_memory.write_bytes(newmem_shovelpro, byte_data, 149)
            PVZ_data.PVZ_memory.write_bytes(
                0x004111D8,
                b"\xe9"
                + calculate_call_address(newmem_shovelpro - 0x004111DD)
                + b"\x90",
                6,
            )
        else:
            PVZ_data.PVZ_memory.write_bytes(addr + 0x15, b"\x83\xf8\x17", 3)
            PVZ_data.PVZ_memory.write_bytes(0x004111D8, b"\x01\x9f\x9c\x57\x00\x00", 6)
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_shovelpro
            )
    elif PVZ_data.PVZ_version == 2.1 or PVZ_data.PVZ_version >= 2.2:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x008E0460, b"\xe9\x7f\x00\x00\x00\x90", 6)
            newmem_shovelpro = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 100
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
            PVZ_data.PVZ_memory.write_bytes(newmem_shovelpro, byte_data, 149)
            PVZ_data.PVZ_memory.write_bytes(
                0x004111D8,
                b"\xe9"
                + calculate_call_address(newmem_shovelpro - 0x004111DD)
                + b"\x90",
                6,
            )
        else:
            PVZ_data.PVZ_memory.write_bytes(0x008E0460, b"\x0f\x84\x88\x00\x00\x00", 6)
            PVZ_data.PVZ_memory.write_bytes(0x004111D8, b"\x01\x9f\x9c\x57\x00\x00", 6)
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_shovelpro
            )


def randomSlots_operstion(randomSlots_event, haszombie):
    while not randomSlots_event.is_set():
        plant1addr = (
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
            )
            + 0x144
        )
        for i in range(0, 14):
            if haszombie is False:
                plant = getRandomPlant(False)
            else:
                plant = getRandomZombie(True) + 256
            PVZ_data.PVZ_memory.write_int(
                PVZ_data.PVZ_memory.read_int(plant1addr) + 0x5C + 0x50 * i, plant
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


def changeGameSpeed(s):
    FrameDurationAddr = PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x454
    if s == 0:
        PVZ_data.PVZ_memory.write_int(FrameDurationAddr, 10)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAA, b"\x01", 1)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAB, b"\x00", 1)
    elif s == 1:
        PVZ_data.PVZ_memory.write_int(FrameDurationAddr, 20)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAA, b"\x00", 1)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAB, b"\x00", 1)
    elif s == 2:
        PVZ_data.PVZ_memory.write_int(FrameDurationAddr, 10)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAA, b"\x00", 1)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAB, b"\x00", 1)
    elif s == 3:
        PVZ_data.PVZ_memory.write_int(FrameDurationAddr, 5)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAA, b"\x00", 1)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAB, b"\x00", 1)
    elif s == 4:
        PVZ_data.PVZ_memory.write_int(FrameDurationAddr, 2)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAA, b"\x00", 1)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAB, b"\x00", 1)
    elif s == 5:
        PVZ_data.PVZ_memory.write_int(FrameDurationAddr, 1)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAA, b"\x00", 1)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAB, b"\x00", 1)
    elif s == 6:
        PVZ_data.PVZ_memory.write_int(FrameDurationAddr, 10)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAA, b"\x00", 1)
        PVZ_data.PVZ_memory.write_bytes(0x6A9EAB, b"\x01", 1)


def completeAdvanture(level):
    advantureAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x42C
    )
    PVZ_data.PVZ_memory.write_int(advantureAddr + level * 4, 1)


def lockAdvanture(level):
    advantureAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x42C
    )
    PVZ_data.PVZ_memory.write_int(advantureAddr + level * 4, 0)


def completeChallenge(level):
    challengeAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x82C
    )
    PVZ_data.PVZ_memory.write_int(challengeAddr + level * 4, 1)


def lockChallenge(level):
    challengeAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x82C
    )
    PVZ_data.PVZ_memory.write_int(challengeAddr + level * 4, 0)


def completeMiniGame(level):
    challengeAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x202C
    )
    PVZ_data.PVZ_memory.write_int(challengeAddr + level * 4, 1)


def completePuzzle(level):
    challengeAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x242C
    )
    PVZ_data.PVZ_memory.write_int(challengeAddr + level * 4, 1)


def lockPuzzle(level):
    challengeAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x242C
    )
    PVZ_data.PVZ_memory.write_int(challengeAddr + level * 4, 0)


def lockMiniGame(level):
    challengeAddr = (
        PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x82C
        )
        + 0x202C
    )
    PVZ_data.PVZ_memory.write_int(challengeAddr + level * 4, 0)


def noHole(d, t, b):
    global newmem_noHole
    if d and not b and not t:
        PVZ_data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 0)
        shellcode.jne_short_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if d and b and not t:
        PVZ_data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 2)
        shellcode.je_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if d and b and t:
        PVZ_data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 0)
        shellcode.add_byte(0x90)
        shellcode.add_byte(0x90)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if not d and b and not t:
        PVZ_data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 1)
        shellcode.jne_short_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if not d and b and t:
        PVZ_data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 0)
        shellcode.je_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if not d and not b and t:
        PVZ_data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 2)
        shellcode.jne_short_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if d and not b and t:
        PVZ_data.PVZ_memory.write_bytes(0x00466668, b"\x90\x90\xeb\x2e", 4)

        newmem_noHole = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_noHole)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0)
        shellcode.jng(0x0041D79E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x50, 1)
        shellcode.je_offset(7)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ESI, 0x20, 1)
        shellcode.add_dword_ptr_exx_add_byte_byte(asm.ESI, 0x18, 0xFF)
        shellcode.jmp(0x0041D79A)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_noHole, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0041D790,
            b"\xe9"
            + calculate_call_address(newmem_noHole - 0x0041D795)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    if not d and not b and not t:
        PVZ_data.PVZ_memory.write_bytes(0x00466668, b"\x84\xc0\x74\x2e", 4)
        PVZ_data.PVZ_memory.write_bytes(
            0x0041D790, b"\x83\x7e\x18\x00\x7e\x08\x83\x46\x18\xff", 10
        )
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_noHole)


def zombiebeanHpynotized(f):
    global newmem_zombiebeanHpynotized1
    global newmem_zombiebeanHpynotized
    if PVZ_data.PVZ_version == 2.0:
        if f:
            newmem_zombiebeanHpynotized1 = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 64
            )
            newmem_zombiebeanHpynotized = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 64
            )
            shellcode = asm.Asm(newmem_zombiebeanHpynotized)
            shellcode.jmp(0x0086E267)
            PVZ_data.PVZ_memory.write_bytes(
                newmem_zombiebeanHpynotized,
                bytes(shellcode.code[: shellcode.index]),
                shellcode.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
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
            PVZ_data.PVZ_memory.write_bytes(
                newmem_zombiebeanHpynotized1,
                bytes(shellcode1.code[: shellcode1.index]),
                shellcode1.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x0084F684,
                b"\xe9"
                + calculate_call_address(newmem_zombiebeanHpynotized1 - 0x0084F689)
                + b"\x90\x90\x90",
                8,
            )

        else:
            PVZ_data.PVZ_memory.write_bytes(
                0x084F684, b"\x8b\x46\x04\xe8\x34\xe7\xbb\xff", 8
            )
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_zombiebeanHpynotized
            )
            PVZ_data.PVZ_memory.write_bytes(0x0086E243, b"\x0f\x84\x1e\x00\x00\x00", 6)
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_zombiebeanHpynotized1
            )
    elif PVZ_data.PVZ_version == 2.1 or PVZ_data.PVZ_version >= 2.2:
        if f:
            newmem_zombiebeanHpynotized1 = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 64
            )
            PVZ_data.PVZ_memory.write_bytes(0x008AF243, b"\xeb\x22\x90\x90\x90\x90", 6)

            shellcode1 = asm.Asm(newmem_zombiebeanHpynotized1)
            shellcode1.mov_exx_dword_ptr_eyy_add_byte(asm.EAX, asm.ESI, 4)
            shellcode1.call(0x0040DDC0)
            shellcode1.mov_byte_ptr_exx_add_dword_byte(asm.EAX, 0xB8, 1)
            shellcode1.jmp(0x008AF43C)
            PVZ_data.PVZ_memory.write_bytes(
                newmem_zombiebeanHpynotized1,
                bytes(shellcode1.code[: shellcode1.index]),
                shellcode1.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x008AF434,
                b"\xe9"
                + calculate_call_address(newmem_zombiebeanHpynotized1 - 0x008AF439)
                + b"\x90\x90\x90",
                8,
            )

        else:
            PVZ_data.PVZ_memory.write_bytes(
                0x008AF434, b"\x8b\x46\x04\xe8\x34\xe7\xbb\xff", 8
            )
            PVZ_data.PVZ_memory.write_bytes(0x008AF243, b"\x0f\x84\x1e\x00\x00\x00", 6)
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_zombiebeanHpynotized1
            )


def scrapHelmetControlled(f):
    if PVZ_data.PVZ_version == 2.0:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x0084AB3F, b"\x90\xe9", 2)
        else:
            PVZ_data.PVZ_memory.write_bytes(0x0084AB3F, b"\x0f\x85", 2)
    elif PVZ_data.PVZ_version == 2.1:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x0089A03F, b"\x90\xe9", 2)
        else:
            PVZ_data.PVZ_memory.write_bytes(0x0089A03F, b"\x0f\x85", 2)
    elif PVZ_data.PVZ_version >= 2.2:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x0089A03F, b"\x90\xe9", 2)
            PVZ_data.PVZ_memory.write_bytes(0x00882211, b"\x90\x90\x90\x90\x90\x90", 6)
        else:
            PVZ_data.PVZ_memory.write_bytes(0x0089A03F, b"\x0f\x85", 2)
            PVZ_data.PVZ_memory.write_bytes(0x00882211, b"\x0f\x84\x87\x00\x00\x00", 6)


def conveyorBeltFull(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x00422D1F, b"\x0f\x80", 2)
        PVZ_data.PVZ_memory.write_bytes(0x00489CA1, b"\x33\xc0", 2)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00422D1F, b"\x0f\x8f", 2)
        PVZ_data.PVZ_memory.write_bytes(0x00489CA1, b"\x85\xc0", 2)


def getEndlessRound():
    try:
        endlessRoundAddr = (
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0x160
            )
            + 0x6C
        )
        return PVZ_data.PVZ_memory.read_int(endlessRoundAddr)
    except:
        return "未知"


def setEndlessRound(endlessRound):
    try:
        endlessRoundAddr = (
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0x160
            )
            + 0x6C
        )
        PVZ_data.PVZ_memory.write_int(endlessRoundAddr, endlessRound)
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
            plantPut_asm.push_dword(self.type)
            plantPut_asm.mov_exx(asm.EAX, self.row)
            plantPut_asm.push_byte(self.col)
            plantPut_asm.mov_exx_dword_ptr(asm.EBP, 0x006A9EC0)
            plantPut_asm.mov_exx_dword_ptr_eyy_add_dword(asm.EBP, asm.EBP, 0x768)
            plantPut_asm.push_exx(asm.EBP)
            plantPut_asm.call(0x0040D120)
            return plantPut_asm

    asm.runThread(plautPut(row, col, type))


def putcard(row, col, type):
    address = pymem.memory.allocate_memory(PVZ_data.PVZ_memory.process_handle, 100)
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
    PVZ_data.PVZ_memory.write_bytes(address, shellcode, 44)
    PVZ_data.PVZ_memory.write_bytes(0x00552014, b"\xfe", 1)
    thread_h = pymem.ressources.kernel32.CreateRemoteThread(
        PVZ_data.PVZ_memory.process_handle,
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
            PVZ_data.PVZ_memory.write_bytes(0x00552014, b"\xdb", 1)
            break
        time.sleep(0.005)
    pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, address)


def creatCaption(str, time, type):
    global newmem_caption
    newmem_caption = pymem.memory.allocate_memory(
        PVZ_data.PVZ_memory.process_handle, 1024
    )
    byte_array = str.encode("gbk")
    PVZ_data.PVZ_memory.write_bytes(
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

    asm.runThread(Defeat())


def noSolt(f):
    # [ENABLE]
    #
    # 485FBA:
    # mov ecx,0 //选卡修改标志位 0可以开局 1不可以开局
    #
    # 4835A5:
    # mov byte ptr [eax+1A],0//开局初始化标志位
    #
    #
    # [DISABLE]
    # 485FBA:
    # mov ecx,1
    #
    #
    # 4835A5:
    # mov byte ptr [eax+1A],1//初始化标志位
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x00485FBA, b"\xb9\x00\x00\x00\x00", 5)
        PVZ_data.PVZ_memory.write_bytes(0x004835A5, b"\xc6\x40\x1a\x00", 4)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00485FBA, b"\xb9\x01\x00\x00\x00", 5)
        PVZ_data.PVZ_memory.write_bytes(0x004835A5, b"\xc6\x40\x1a\x01", 4)


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
        PVZ_data.PVZ_memory.write_bytes(0x00530275, b"\x70", 1)
        newmem_spoils = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 256
        )
        newmem_spoils2 = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 32
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

        PVZ_data.PVZ_memory.write_bytes(
            newmem_spoils2, bytes(tempcode.code[: tempcode.index]), tempcode.index
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x42FFB6,
            b"\xe9" + calculate_call_address(newmem_spoils2 - 0x0042FFBB) + b"\x66\x90",
            7,
        )
        PVZ_data.PVZ_memory.write_bytes(
            newmem_spoils, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x00530277, b"\xe9" + calculate_call_address(newmem_spoils - 0x0053027C), 5
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00530275, b"\x75", 1)
        PVZ_data.PVZ_memory.write_bytes(0x42FFB6, b"\xc7\x45\x68\x00\x00\x00\x00", 7)
        PVZ_data.PVZ_memory.write_bytes(0x00530277, b"\x8b\x03\xbe\x04\x00", 5)
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_spoils)
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_spoils2)


def slotKey(slot_key_list):
    if slot_key_list is not False:
        global newmem_slotKey
        print(slot_key_list)
        newmem_slotKey = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 2048
        )
        print(hex(newmem_slotKey))
        shellcode = asm.Asm(newmem_slotKey)
        shellcode.pushad()
        if slot_key_list["1"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["1"]])
            shellcode.je_offset(0x150)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["2"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["2"]])
            shellcode.je_offset(0x150 + 0x56)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["3"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["3"]])
            shellcode.je_offset(0x150 + 0x56 * 2)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["4"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["4"]])
            shellcode.je_offset(0x150 + 0x56 * 3)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["5"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["5"]])
            shellcode.je_offset(0x150 + 0x56 * 4)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["6"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["6"]])
            shellcode.je_offset(0x150 + 0x56 * 5)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["7"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["7"]])
            shellcode.je_offset(0x150 + 0x56 * 6)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["8"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["8"]])
            shellcode.je_offset(0x150 + 0x56 * 7)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["9"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["9"]])
            shellcode.je_offset(0x150 + 0x56 * 8)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["10"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["10"]])
            shellcode.je_offset(0x150 + 0x56 * 9)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["11"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["11"]])
            shellcode.je_offset(0x150 + 0x56 * 10)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["12"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["12"]])
            shellcode.je_offset(0x150 + 0x56 * 11)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["13"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["13"]])
            shellcode.je_offset(0x150 + 0x56 * 12)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["14"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["14"]])
            shellcode.je_offset(0x150 + 0x56 * 13)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["shovel"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["shovel"]])
            shellcode.je_offset(0x150 + 0x56 * 14)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["zombie_hp"] > 0:
            shellcode.cmp_exx_dword(
                asm.EDI, PVZ_data.keyCode[slot_key_list["zombie_hp"]]
            )
            shellcode.je_offset(0x624)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["top"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["top"]])
            shellcode.je_offset(0x657)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["plant_hp"] > 0:
            shellcode.cmp_exx_dword(
                asm.EDI, PVZ_data.keyCode[slot_key_list["plant_hp"]]
            )
            shellcode.je_offset(0x686)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["speed"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["speed"]])
            shellcode.je_offset(0x6B9)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["bag"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["bag"]])
            shellcode.je_offset(0x6EC)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["15"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["15"]])
            shellcode.je_offset(0x749)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        if slot_key_list["16"] > 0:
            shellcode.cmp_exx_dword(asm.EDI, PVZ_data.keyCode[slot_key_list["16"]])
            shellcode.je_offset(0x79F)
        else:
            shellcode.nop_6()
            shellcode.nop_6()
        # 预留快捷键
        shellcode.nop_6()
        shellcode.nop_6()
        shellcode.nop_6()
        shellcode.nop_6()
        shellcode.nop_6()
        shellcode.nop_6()
        shellcode.nop_6()
        shellcode.nop_6()
        shellcode.nop_6()
        shellcode.nop_6()
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.jmp_dword_offset(0xB)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EDX, 0x1CA0, 0x0)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.mov_exx_dword_ptr(asm.EDX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.EDX, 0x768)
        shellcode.cmp_dword_ptr_exx_add_dword_byte(asm.EDX, 0x57BC, 0x1)
        shellcode.je_offset(0xC)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EDX, 0x57BC, 0x1)
        shellcode.jmp_short_offset(0x0A)
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
        shellcode.jmp_dword_offset(0xB)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EDX, 0x1CA4, 0x0)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        # mov edx,[006A9EC0]
        # mov edx,[edx+0000082C]
        # cmp dword ptr [edx+00001C9C],01
        # je 0089F347
        # mov [edx+00001C9C],00000001
        # popad
        # jmp 0089F352
        # mov [edx+00001C9C],00000000
        # popad
        shellcode.mov_exx_dword_ptr(asm.EDX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.EDX, 0x82C)
        shellcode.cmp_dword_ptr_exx_add_dword_byte(asm.EDX, 0x1C9C, 0x1)
        shellcode.je_offset(0x10)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EDX, 0x1C9C, 0x1)
        shellcode.popad()
        shellcode.jmp_dword_offset(0xB)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EDX, 0x1C9C, 0x0)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        # mov ecx,[006A9EC0]
        # cmp dword ptr [ecx+000007FC],03
        # jne 0089F3B9
        # call 0044F410
        # test al,al
        # je 0089F3B9
        # mov edi,[006A9EC0]
        # mov ebx,FFFFFFFF
        # call 00450180
        # mov ebx,eax
        # mov ecx,eax
        # mov eax,0000000A
        # call 00401BE0
        # mov edx,[ebx]
        # mov ecx,ebx
        # mov eax,[edx+0000012C]
        # push 01
        # call eax
        # mov eax,[006A9EC0]
        # mov eax,[eax+0000083C]
        # call 0045B770
        # popad
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.cmp_dword_ptr_exx_add_dword_byte(asm.ECX, 0x7FC, 0x3)
        shellcode.jne_long_offset(0x4A)
        shellcode.call(0x0044F410)
        shellcode.test_8(asm.AL, asm.AL)
        shellcode.je_offset(0x3D)
        shellcode.mov_exx_dword_ptr(asm.EDI, 0x006A9EC0)
        shellcode.mov_exx(asm.EBX, 0xFFFFFFFF)
        shellcode.call(0x00450180)
        shellcode.mov_exx_eyy(asm.EBX, asm.EAX)
        shellcode.mov_exx_eyy(asm.ECX, asm.EAX)
        shellcode.mov_exx(asm.EAX, 0xA)
        shellcode.call(0x00401BE0)
        shellcode.mov_exx_dword_ptr_eyy(asm.EDX, asm.EBX)
        shellcode.mov_exx_eyy(asm.ECX, asm.EBX)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EDX, 0x12C)
        shellcode.push_byte(0x1)
        shellcode.call_exx(asm.EAX)
        shellcode.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x83C)
        shellcode.call(0x0045B770)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        # 预留快捷键
        shellcode.mov_exx(asm.EDX, 14)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.mov_exx(asm.EDX, 15)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDI, asm.ECX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x144)
        shellcode.cmp_ptr_exx_add_byte_eyy(asm.EBX, 0x24, asm.EDX)
        shellcode.jl_offset(0x3A)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EBX, asm.EDI, 0x138)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x28, 0xFF)
        shellcode.jne_short_offset(0x2E)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x2C, 0xFF)
        shellcode.jne_short_offset(0x28)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x30, 0x00)
        shellcode.jne_short_offset(0x22)
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
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)
        shellcode.popad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.ESI, 0x8C)
        shellcode.jmp(0x0041B278)

        PVZ_data.PVZ_memory.write_bytes(
            newmem_slotKey, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0041B272,
            b"\xe9" + calculate_call_address(newmem_slotKey - 0x0041B277) + b"\x90",
            6,
        )
        if PVZ_data.PVZ_version != 0:
            PVZ_data.PVZ_memory.write_bytes(0x00539660, b"\x90\x90\x90\x90\x90\x90", 6)

    else:
        PVZ_data.PVZ_memory.write_bytes(0x0041B272, b"\x8b\x96\x8c\x00\x00\x00", 6)
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_slotKey)
        if PVZ_data.PVZ_version == 2.0:
            PVZ_data.PVZ_memory.write_bytes(0x00539660, b"\xe9\x9b\x5c\x33\x00\x90", 6)
        elif PVZ_data.PVZ_version == 2.1 or PVZ_data.PVZ_version >= 2.2:
            PVZ_data.PVZ_memory.write_bytes(0x00539660, b"\xe9\x9b\x5b\x36\x00\x90", 6)
        elif PVZ_data.PVZ_version == 0:
            PVZ_data.PVZ_memory.write_bytes(0x00539660, b"\x81\xf9\xfe\x00\x00\x00", 6)


def setAllBullet(f, type):
    global newmem_setAllBullet
    # [ENABLE]
    # //code from here to '[DISABLE]' will be used to enable the cheat
    # alloc(newmem,2048)
    # label(returnhere)
    # label(originalcode)
    # label(exit)

    # newmem: //this is allocated memory, you have read,write,execute access
    # //place your code here
    # mov eax,#39
    # originalcode:
    # mov [ebp+5C],eax
    # mov eax,esi

    # exit:
    # jmp returnhere

    # "PlantsVsZombies.exe"+6C769:
    # jmp newmem
    # returnhere:

    # [DISABLE]
    # //code from here till the end of the code will be used to disable the cheat
    # dealloc(newmem)
    # "PlantsVsZombies.exe"+6C769:
    # db 89 45 5C 8B C6
    # //mov [ebp+5C],eax
    # //mov eax,esi
    if f:
        newmem_setAllBullet = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 2048
        )
        shellcode = asm.Asm(newmem_setAllBullet)
        shellcode.mov_exx(asm.EAX, type)
        shellcode.mov_ptr_exx_add_byte_eyy(asm.EBP, 0x5C, asm.EAX)
        shellcode.mov_exx_eyy(asm.EAX, asm.ESI)
        shellcode.jmp(0x0046C76E)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_setAllBullet,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0046C769,
            b"\xe9" + calculate_call_address(newmem_setAllBullet - 0x0046C76E),
            5,
        )
        PVZ_data.PVZ_memory.write_bytes(0x0088CE91, b"\x90\x90\x90\x90\x90", 5)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0046C769, b"\x89\x45\x5c\x8b\xc6", 5)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_setAllBullet
        )
        PVZ_data.PVZ_memory.write_bytes(0x0088CE91, b"\xe8\x1a\x1e\xbe\xff", 5)


def setOneBullet(f, type1, type2):
    global newmem_setOneBullet
    if f:
        newmem_setOneBullet = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 64
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
        PVZ_data.PVZ_memory.write_bytes(
            newmem_setOneBullet,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0046E8DC,
            b"\xe9" + calculate_call_address(newmem_setOneBullet - 0x0046E8E1),
            5,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0046E8DC, b"\xda\x64\x24\x18\x57", 5)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_setOneBullet
        )


def randomBullet(f, hasDoom, hasMine, hasPepper):
    global newmem_randomBullet
    if f:
        newmem_randomBullet = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 2048
        )
        shellcode = asm.Asm(newmem_randomBullet)
        shellcode.create_label("start")
        shellcode.mov_exx(asm.EAX, 39)
        shellcode.call(0x005AF400)
        if not hasDoom:
            shellcode.cmp_exx_byte(asm.EAX, 11)
            shellcode.je_label("start")
        if not hasMine:
            shellcode.cmp_exx_byte(asm.EAX, 22)
            shellcode.je_label("start")
        if not hasPepper:
            shellcode.cmp_exx_byte(asm.EAX, 24)
            shellcode.je_label("start")
        shellcode.mov_ptr_exx_add_byte_eyy(asm.EBP, 0x5C, asm.EAX)
        shellcode.mov_exx_eyy(asm.EAX, asm.ESI)
        shellcode.jmp(0x0046C76E)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_randomBullet,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0046C769,
            b"\xe9" + calculate_call_address(newmem_randomBullet - 0x0046C76E),
            5,
        )
        PVZ_data.PVZ_memory.write_bytes(0x0088CE91, b"\x90\x90\x90\x90\x90", 5)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0046C769, b"\x89\x45\x5c\x8b\xc6", 5)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_randomBullet
        )
        PVZ_data.PVZ_memory.write_bytes(0x0088CE91, b"\xe8\x1a\x1e\xbe\xff", 5)


def setAttackSpeed(multiple):
    PVZ_data.PVZ_memory.write_uchar(0x045F8AC, 256 - 1 * multiple)


def cancelAttackAnimation(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x00464A96, b"\x90\x90\x90\x90\x90\x90", 6)
        PVZ_data.PVZ_memory.write_bytes(0x00464A62, b"\x90\x90\x90\x90\x90\x90\x90", 7)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00464A96, b"\x0f\x85\x98\xfe\xff\xff", 6)
        PVZ_data.PVZ_memory.write_bytes(0x00464A62, b"\x83\xbf\x90\x00\x00\x00\x13", 7)


def setBulletSize(f, size):
    global newmem_setBulletSize
    global newmem_setBulletPosition
    if f:
        newmem_setBulletSize = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 64
        )
        setBulletSizeCode = asm.Asm(newmem_setBulletSize)
        setBulletSizeCode.imul_exx_eyy_byte(asm.EBX, asm.EBX, size)
        setBulletSizeCode.mov_ptr_exx_add_byte_eyy(asm.ESP, 0x44, asm.EBX)
        setBulletSizeCode.mov_exx(asm.EBX, size)
        setBulletSizeCode.imul_exx_eyy(asm.EBX, asm.EDI)
        setBulletSizeCode.mov_ptr_exx_add_byte_eyy(asm.ESP, 0x40, asm.EBX)
        setBulletSizeCode.jmp(0x0046E77A)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_setBulletSize,
            bytes(setBulletSizeCode.code[: setBulletSizeCode.index]),
            setBulletSizeCode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0046E772,
            b"\xe9"
            + calculate_call_address(newmem_setBulletSize - 0x0046E777)
            + b"\x90\x90\x90",
            8,
        )

        newmem_setBulletPosition = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 64
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
        PVZ_data.PVZ_memory.write_bytes(
            newmem_setBulletPosition,
            bytes(setBulletPositionCode.code[: setBulletPositionCode.index]),
            setBulletPositionCode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0046E765,
            b"\xe9"
            + calculate_call_address(newmem_setBulletPosition - 0x0046E76A)
            + b"\x90\x90\x90",
            8,
        )

    else:
        PVZ_data.PVZ_memory.write_bytes(
            0x0046E772, b"\x89\x7c\x24\x40\x89\x5c\x24\x44", 8
        )
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_setBulletSize
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0046E765, b"\x89\x44\x24\x34\x89\x44\x24\x38", 8
        )
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_setBulletPosition
        )


def setPlantBullet(f, plantType, bulletType, mode):
    global newmem_setPlantBullet
    if f:
        newmem_setPlantBullet = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 64
        )
        shellcode = asm.Asm(newmem_setPlantBullet)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBP, 0x24, plantType)
        shellcode.jne_short_offset(0xE)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EAX, 0x5C, bulletType)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EAX, 0x58, mode)
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EDX, asm.ESP, 0x3C)
        shellcode.mov_exx_eyy(asm.ECX, asm.EAX)
        shellcode.jmp(0x004672BB)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_setPlantBullet,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x004672B5,
            b"\xe9"
            + calculate_call_address(newmem_setPlantBullet - 0x004672BA)
            + b"\x90",
            6,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x004672B5, b"\x8b\x54\x24\x3c\x8b\xc8", 6)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_setPlantBullet
        )


def startAllCars():
    rows = getMap()
    try:
        car_num = PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
            )
            + 0x110
        )
    except:
        return
    i = 0
    j = 0
    start_car_list = [0] * rows
    while i < car_num:
        car_addresss = (
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0x100
            )
            + 0x48 * j
        )
        car_exist = PVZ_data.PVZ_memory.read_bytes(car_addresss + 0x30, 1)
        if car_exist == b"\x00":
            try:
                c = PVZ_data.car(car_addresss)
                if start_car_list[c.row] == 0:
                    startCar(car_addresss)
                    start_car_list[c.row] = 1
            except:
                pass
            i = i + 1
        j = j + 1


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


def endlessCar(f):
    global newmem_endlessCar
    if f:
        newmem_endlessCar = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 64
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
        PVZ_data.PVZ_memory.write_bytes(
            newmem_endlessCar, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x00458AEC,
            b"\xe9" + calculate_call_address(newmem_endlessCar - 0x00458AF1) + b"\x90",
            6,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00458AEC, b"\xd9\x43\x08\x8b\x43\x34", 6)
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_endlessCar)


def initCar(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x0040BCA3, b"\x83\xfa\x14\x7a\x70", 5)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0040BCA3, b"\x83\xfa\x14\x7a\x70", 5)


def autoCar(f):
    global newmem_autoCar  # 声明 newmem 为全局变量
    if f:
        # if enable_LawnMowers==1:
        newmem_autoCar = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 128
        )
        # print(f"无限小车 by 妥妥的 2024-4-9 08:30:45, allocated memory: {hex(newmem)},patch addr: {hex(0x458d99)}")
        PVZ_data.PVZ_memory.write_bytes(
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
        PVZ_data.PVZ_memory.write_bytes(newmem_autoCar, byte_data, 81)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x458D99, b"\xc3\xcc\xcc\xcc\xcc", 5)
        # process_handle = pymem.process.open(pid[1])
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_autoCar)


def setPausePro(f):
    global newmem_pauseFlag
    if f:
        try:
            PVZ_data.PVZ_memory.write_bytes(newmem_pauseFlag, b"\x01", 1)
        except:
            pass
    else:
        try:
            print(PVZ_data.PVZ_memory.read_bool(newmem_pauseFlag))
            PVZ_data.PVZ_memory.write_bytes(newmem_pauseFlag, b"\x00", 1)
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
            PVZ_data.PVZ_memory.process_handle, 64
        )
        print(hex(newmem_pauseProKey))
        newmem_pause = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 128
        )
        print(hex(newmem_pause))
        newmem_draw = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 256
        )
        print(hex(newmem_draw))
        newmem_drawTime = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 4
        )
        print(hex(newmem_drawTime))
        newmem_pauseFlag = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 1
        )
        print(hex(newmem_pauseFlag))
        shell_code_key = asm.Asm(newmem_pauseProKey)
        shell_code_key.push_exx(asm.EDX)
        shell_code_key.call(0x0051C5A0)
        shell_code_key.cmp_exx_byte(asm.EDI, PVZ_data.keyCode[key])
        shell_code_key.jne_short_offset(7)
        shell_code_key.xor_dword_ptr_address_val(newmem_pauseFlag, 1)
        shell_code_key.jmp(0x0041B2A1)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_pauseProKey,
            bytes(shell_code_key.code[: shell_code_key.index]),
            shell_code_key.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0041B29B,
            b"\xe9" + calculate_call_address(newmem_pauseProKey - 0x0041B2A0) + b"\x90",
            6,
        )

        pause_key = asm.Asm(newmem_pause)
        pause_key.cmp_dword_ptr_address_byte(newmem_pauseFlag, 1)
        pause_key.jne_short_offset(0x1F)
        pause_key.add_dword_ptr_address_byte(newmem_drawTime, 24)
        pause_key.cmp_dword_ptr_address_dword(newmem_drawTime, 1000)
        pause_key.jl_offset(0x29)
        pause_key.mov_dword_ptr_dword(newmem_drawTime, 1000)
        pause_key.jmp_short_offset(0x1D)
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
        PVZ_data.PVZ_memory.write_bytes(
            newmem_pause, bytes(pause_key.code[: pause_key.index]), pause_key.index
        )
        PVZ_data.PVZ_memory.write_bytes(
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
        shellcode_draw.jmp_dword_offset(0x78)
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
        PVZ_data.PVZ_memory.write_bytes(
            newmem_draw,
            bytes(shellcode_draw.code[: shellcode_draw.index]),
            shellcode_draw.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0041AABE,
            b"\xe9" + calculate_call_address(newmem_draw - 0x0041AAC3) + b"\x90\x90",
            7,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0041B29B, b"\x52\xe8\xff\x12\x10\x00", 6)
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_pauseProKey)

        PVZ_data.PVZ_memory.write_bytes(0x00415DF0, b"\x80\x8d\x64\x01\x00\x00\x00", 7)
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_pause)

        PVZ_data.PVZ_memory.write_bytes(0x0041AABE, b"\x83\xbd\x48\x57\x00\x00\x00", 7)
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_draw)


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
        plant_num = PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
            )
            + 0xBC
        )
    except:
        return
    i = 0
    j = 0
    while i < plant_num:
        plant_addresss = (
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0xAC
            )
            + 0x204 * j
        )
        plant_exist = PVZ_data.PVZ_memory.read_bytes(plant_addresss + 0x141, 1)
        if plant_exist == b"\x00":
            plant_list.append(PVZ_data.plant(plant_addresss))
            i = i + 1
        j = j + 1
    for p in plant_list:
        plantType = getRandomPlant(True)
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
        PVZ_data.PVZ_memory.write_bytes(0x0041CC2F, b"\xeb", 1)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0041CC2F, b"\x74", 1)


def PlantConnotBurnedDeath(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x005276EA, b"\xeb", 1)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x005276EA, b"\x75", 1)


def PlantConnotBitedDeath(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x0052FCF3, b"\x00", 1)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0052FCF3, b"\xfc", 1)


def PlantConnotCrushedDeath(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x0052E93B, b"\xeb", 1)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0052E93B, b"\x74", 1)


def PlantConnotHitedDeath(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x0046CFEB, b"\x90\x90\x90", 3)
        PVZ_data.PVZ_memory.write_bytes(0x0046D7A6, b"\x90\x90\x90", 3)
        if PVZ_data.PVZ_version == 2.1 or PVZ_data.PVZ_version >= 2.2:
            PVZ_data.PVZ_memory.write_bytes(0x008AD752, b"\x90\x90\x90", 3)
        elif PVZ_data.PVZ_version == 2.0:
            PVZ_data.PVZ_memory.write_bytes(0x0084F15D, b"\x90\x90\x90", 3)
        PVZ_data.PVZ_memory.write_bytes(0x0046CFEB, b"\x90\x90\x90", 3)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0046CFEB, b"\x29\x50\x40", 3)
        PVZ_data.PVZ_memory.write_bytes(0x0046D7A6, b"\x29\x50\x40", 3)
        if PVZ_data.PVZ_version == 2.1 or PVZ_data.PVZ_version >= 2.2:
            PVZ_data.PVZ_memory.write_bytes(0x008AD752, b"\x29\x50\x40", 3)
        elif PVZ_data.PVZ_version == 2.0:
            PVZ_data.PVZ_memory.write_bytes(0x0084F15D, b"\x29\x50\x40", 3)
        PVZ_data.PVZ_memory.write_bytes(0x0046CFEB, b"\x29\x50\x40", 3)


def PlantConnotStolen(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x00524D33, b"\xeb", 1)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00524D33, b"\x74", 1)


def fogDraw(f):
    if PVZ_data.PVZ_version == 2.0:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x0086E521, b"\x0f\x80", 2)
        else:
            PVZ_data.PVZ_memory.write_bytes(0x0086E521, b"\x0f\x84", 2)
    elif PVZ_data.PVZ_version == 2.1 or PVZ_data.PVZ_version >= 2.2:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x008A7821, b"\x0f\x80", 2)
        else:
            PVZ_data.PVZ_memory.write_bytes(0x008A7821, b"\x0f\x84", 2)


def invisibleDraw(f):
    if PVZ_data.PVZ_version == 2.0:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x0086E56C, b"\x70", 1)
        else:
            PVZ_data.PVZ_memory.write_bytes(0x0086E56C, b"\x74", 1)
    elif PVZ_data.PVZ_version == 2.1 or PVZ_data.PVZ_version >= 2.2:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x008A786C, b"\x70", 1)
        else:
            PVZ_data.PVZ_memory.write_bytes(0x008A786C, b"\x74", 1)


newmem_bossHPDraw = None


def bossHPDraw(f):
    global newmem_bossHPDraw
    # [ENABLE]
    # //code from here to '[DISABLE]' will be used to enable the cheat
    # alloc(newmem,2048)
    # label(returnhere)
    # label(originalcode)
    # label(exit)

    # newmem: //this is allocated memory, you have read,write,execute access
    # //place your code here
    # mov [00736690],0
    # mov eax,[6a9ec0]
    # mov eax,[eax+7fc]
    # cmp eax,3
    # jne originalcode
    # pushad
    # sub esp,4
    # lea esi,[esp]
    # mov [esi],0
    # mov edx,[6a9ec0]
    # mov edx,[edx+768]

    # xunhuan:
    # mov ecx,41c8f0
    # call ecx
    # test al,al
    # je end
    # mov ebx,[esi]//[esi]=*zombie
    # cmp [ebx+24],#25
    # jne xunhuan

    # push eax
    # mov eax,0
    # add eax,[700104]
    # sub eax,[700100]
    # mov [700b40],eax
    # pop eax

    # pushad
    # mov eax, [ebx+C8]
    # mov ecx,eax
    # // itoa的第二个参数是目标字符串的地址，这里是jiangwang+A
    # lea edx, [jiangwang+5]
    # call 5B0280
    # popad
    # pushad
    # push jiangwang
    # mov ecx,700b00
    # call 404300
    # popad
    # pushad
    # mov eax,[00736690]
    # inc eax
    # mov [00736690],eax
    # mov ebx,eax
    # // 将 ebx 的值乘以 20 存储在 edx 中
    # mov edx, ebx
    # imul edx, edx, #20 // edx = ebx * 20
    # add edx, #250 // edx = 600 + ebx * 20
    # // 现在 edx 包含了正确的 Y 坐标
    # push edx
    # push #640
    # push 700b00
    # mov eax,edi
    # mov ebx,[6A7314]
    # mov [edi+40],ebx
    # mov [edi+30],ff
    # mov [edi+34],cc
    # mov [edi+38],cc
    # mov [edi+3c],ff
    # call 587120
    # popad
    # jmp xunhuan

    # end:
    # mov [esp],0
    # add esp,4
    # popad

    # originalcode:
    # mov eax,fs:[00000000]

    # exit:
    # jmp returnhere

    # jiangwang:

    # db BD A9 CD F5 D1 AA C1 BF 3A
    # db 00 00 00 00 00 00 00

    # "PlantsVsZombies.exe"+11AA50:
    # jmp newmem
    # nop
    # returnhere:

    # [DISABLE]
    # //code from here till the end of the code will be used to disable the cheat
    # dealloc(newmem)
    # "PlantsVsZombies.exe"+11AA50:
    # db 64 A1 00 00 00 00
    # //mov eax,fs:[00000000]
    if f:
        newmem_bossHPDraw = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 1024
        )
        shellcode = asm.Asm(newmem_bossHPDraw)
        shellcode.mov_dword_ptr_dword(0x00736690, 0)
        shellcode.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x7FC)
        shellcode.cmp_exx_byte(asm.EAX, 3)
        shellcode.jne_label("originalcode")
        shellcode.pushad()
        shellcode.sub_exx_byte(asm.ESP, 4)
        shellcode.lea_exx_ptr_eyy(asm.ESI, asm.ESP)
        shellcode.mov_ptr_exx_dword(asm.ESI, 0)
        shellcode.mov_exx_dword_ptr(asm.EDX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.EDX, 0x768)
        shellcode.create_label("xunhuan")
        shellcode.call(0x0041C8F0)
        shellcode.test_8(asm.AL, asm.AL)
        shellcode.je_label("end")
        shellcode.mov_exx_dword_ptr_eyy(asm.EBX, asm.ESI)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x24, 25)
        shellcode.jne_label("xunhuan")
        shellcode.push_exx(asm.EAX)
        shellcode.mov_exx(asm.EAX, 0)
        shellcode.add_exx_ptr_dword(asm.EAX, 0x00700104)
        shellcode.sub_exx_ptr_dword(asm.EAX, 0x00700100)
        shellcode.mov_dword_ptr_exx(0x00700B40, asm.EAX)
        shellcode.pop_exx(asm.EAX)
        shellcode.pushad()
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EBX, 0xC8)
        shellcode.mov_exx_eyy(asm.ECX, asm.EAX)
        shellcode.lea_exx_label_add_byte(asm.EDX, "jiangwang", 5)
        shellcode.call(0x005B0280)
        shellcode.popad()
        shellcode.pushad()
        shellcode.push_label("jiangwang")
        shellcode.mov_exx(asm.ECX, 0x00700B00)
        shellcode.call(0x00404300)
        shellcode.popad()
        shellcode.pushad()
        shellcode.mov_exx_dword_ptr(asm.EAX, 0x00736690)
        shellcode.inc_exx(asm.EAX)
        shellcode.mov_dword_ptr_exx(0x00736690, asm.EAX)
        shellcode.mov_exx_eyy(asm.EBX, asm.EAX)
        shellcode.mov_exx_eyy(asm.EDX, asm.EBX)
        shellcode.imul_exx_eyy_byte(asm.EDX, asm.EDX, 20)
        shellcode.add_exx_dword(asm.EDX, 250)
        shellcode.push_exx(asm.EDX)
        shellcode.push_dword(640)
        shellcode.push_dword(0x00700B00)
        shellcode.mov_exx_eyy(asm.EAX, asm.EDI)
        shellcode.mov_exx_dword_ptr(asm.EBX, 0x006A7314)
        shellcode.mov_ptr_exx_add_byte_eyy(asm.EDI, 0x40, asm.EBX)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EDI, 0x30, 0xFF)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EDI, 0x34, 0x66)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EDI, 0x38, 0x66)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EDI, 0x3C, 0xFF)
        shellcode.call(0x00587120)
        shellcode.popad()
        shellcode.jmp_label("xunhuan")
        shellcode.create_label("end")
        shellcode.mov_ptr_exx_dword(asm.ESP, 0)
        shellcode.add_exx_byte(asm.ESP, 4)
        shellcode.popad()
        shellcode.create_label("originalcode")
        shellcode.mov_exx_fs_offset(asm.EAX, 0)
        shellcode.create_label("exit")
        shellcode.jmp(0x0051AA56)
        shellcode.create_label("jiangwang")
        shellcode.add_bytes(
            b"\xbd\xa9\xcd\xf5\xd1\xaa\xc1\xbf\x3a\x00\x00\x00\x00\x00\x00\x00"
        )
        PVZ_data.PVZ_memory.write_bytes(
            newmem_bossHPDraw,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0051AA50,
            b"\xe9" + calculate_call_address(newmem_bossHPDraw - 0x0051AA55) + b"\x90",
            6,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0051AA50, b"\x64\xa1\x00\x00\x00\x00", 6)
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_bossHPDraw)


zb = False


def spawisModified():
    global zb
    if zb is True:
        pass
    else:
        global newmem_spawisModified
        if (
            newmem_modifySpawNum is not None
            or newmem_globalSpawModify is not None
            or newmem_modifySpawMultiplier is not None
        ):
            newmem_spawisModified = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 256
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
            shellcode.jmp_dword_offset(0)
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
            PVZ_data.PVZ_memory.write_bytes(
                newmem_spawisModified,
                bytes(shellcode.code[: shellcode.index]),
                shellcode.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x00417DC0,
                b"\xe9"
                + calculate_call_address(newmem_spawisModified - 0x00417DC5)
                + b"\x90\x90\x90\x90",
                9,
            )
        else:
            PVZ_data.PVZ_memory.write_bytes(
                0x00417DC0, b"\x57\xc7\x44\x24\x7c\x0f\x00\x00\x00", 9
            )
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_spawisModified
            )


def clearPlants():
    try:
        plant_num = PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
            )
            + 0xBC
        )
    except:
        return
    i = 0
    j = 0
    while i < plant_num:
        plant_addresss = (
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0xAC
            )
            + 0x204 * j
        )
        plant_exist = PVZ_data.PVZ_memory.read_bytes(plant_addresss + 0x141, 1)
        if plant_exist == b"\x00":
            PVZ_data.PVZ_memory.write_bytes(plant_addresss + 0x141, b"\x01", 1)
            i = i + 1
        j = j + 1


def modifySpawNum(f, num):
    global newmem_modifySpawNum
    if f:
        newmem_modifySpawNum = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_modifySpawNum)
        shellcode.mov_ptr_exx_add_dword_dword(asm.EAX, 0x5564, num * 10)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.EAX, 0x5564)
        shellcode.jmp(0x0043A25A)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_modifySpawNum,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0043A254,
            b"\xe9"
            + calculate_call_address(newmem_modifySpawNum - 0x0043A259)
            + b"\x90",
            6,
        )
        spawisModified()
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0043A254, b"\x8b\x88\x64\x55\x00\x00", 6)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_modifySpawNum
        )
        # newmem_modifySpawNum = None


def modifySpawMultiplier(f, mult):
    divzero(1)
    unlimitedMonsterSpawning(1)
    global newmem_modifySpawMultiplier
    if PVZ_data.PVZ_version == 2.0:
        if f:
            newmem_modifySpawMultiplier = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 256
            )
            shellcode = asm.Asm(newmem_modifySpawMultiplier)
            shellcode.mov_ptr_exx_add_byte_dword(asm.ESP, 0x24, mult)
            shellcode.jmp(0x00409968)
            PVZ_data.PVZ_memory.write_bytes(
                newmem_modifySpawMultiplier,
                bytes(shellcode.code[: shellcode.index]),
                shellcode.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x00409893,
                b"\xe9"
                + calculate_call_address(newmem_modifySpawMultiplier - 0x00409898)
                + b"\x90",
                6,
            )
            spawisModified()
        else:
            PVZ_data.PVZ_memory.write_bytes(0x00409893, b"\xe9\x68\x37\x46\x00\x90", 6)
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_modifySpawMultiplier
            )
    elif PVZ_data.PVZ_version == 2.1 or PVZ_data.PVZ_version >= 2.2:
        if f:
            newmem_modifySpawMultiplier = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 256
            )
            shellcode = asm.Asm(newmem_modifySpawMultiplier)
            shellcode.mov_ptr_exx_add_byte_dword(asm.ESP, 0x24, mult)
            shellcode.jmp(0x00409968)
            PVZ_data.PVZ_memory.write_bytes(
                newmem_modifySpawMultiplier,
                bytes(shellcode.code[: shellcode.index]),
                shellcode.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x00409893,
                b"\xe9"
                + calculate_call_address(newmem_modifySpawMultiplier - 0x00409898)
                + b"\x90",
                6,
            )
            spawisModified()
        else:
            PVZ_data.PVZ_memory.write_bytes(0x00409893, b"\xe9\x68\x6b\x42\x00\x90", 6)
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_modifySpawMultiplier
            )


def globalSpawModify(f, zombieTypes):
    divzero(1)
    unlimitedMonsterSpawning(1)
    global newmem_globalSpawModify
    if PVZ_data.PVZ_version == 2.0:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x00425855, b"\xeb", 1)
            PVZ_data.PVZ_memory.write_bytes(0x0042584E, b"\x90\x90\x90\x90\x90", 5)
            newmem_globalSpawModify = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 256
            )
            shellcode = asm.Asm(newmem_globalSpawModify)
            for i in range(0, 42):
                if str(i) in zombieTypes:
                    shellcode.mov_byte_ptr_exx_add_dword_byte(asm.EDX, 0x57D4 + i, 1)
                else:
                    shellcode.mov_byte_ptr_exx_add_dword_byte(asm.EDX, 0x57D4 + i, 0)

            shellcode.jmp(0x00425D1D)
            PVZ_data.PVZ_memory.write_bytes(
                newmem_globalSpawModify,
                bytes(shellcode.code[: shellcode.index]),
                shellcode.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x00820CFF,
                b"\xe9"
                + calculate_call_address(newmem_globalSpawModify - 0x00820D04)
                + b"\x90",
                6,
            )
            spawisModified()
        else:
            PVZ_data.PVZ_memory.write_bytes(0x00425855, b"\x7f", 1)
            PVZ_data.PVZ_memory.write_bytes(0x0042584E, b"\xe9\xed\x9f\x42\x00", 5)
            PVZ_data.PVZ_memory.write_bytes(0x00820CFF, b"\x0f\x85\x21\x00\x00\x00", 6)
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_globalSpawModify
            )
    elif PVZ_data.PVZ_version == 2.1 or PVZ_data.PVZ_version == 2.2:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x00425855, b"\xeb", 1)
            PVZ_data.PVZ_memory.write_bytes(0x0042584E, b"\x90\x90\x90\x90\x90", 5)
            newmem_globalSpawModify = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 256
            )
            shellcode = asm.Asm(newmem_globalSpawModify)
            for i in range(0, 51):
                if str(i) in zombieTypes:
                    shellcode.mov_byte_ptr_exx_add_dword_byte(asm.EDX, 0x57D4 + i, 1)
                else:
                    shellcode.mov_byte_ptr_exx_add_dword_byte(asm.EDX, 0x57D4 + i, 0)

            shellcode.jmp(0x00425D1D)
            PVZ_data.PVZ_memory.write_bytes(
                newmem_globalSpawModify,
                bytes(shellcode.code[: shellcode.index]),
                shellcode.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x0082401F,
                b"\xe9"
                + calculate_call_address(newmem_globalSpawModify - 0x00824024)
                + b"\x90",
                6,
            )
            spawisModified()
        else:
            PVZ_data.PVZ_memory.write_bytes(0x00425855, b"\x7f", 1)
            PVZ_data.PVZ_memory.write_bytes(0x0042584E, b"\xe9\xad\xaa\x48\x00", 5)
            PVZ_data.PVZ_memory.write_bytes(0x0082401F, b"\x0f\x85\x21\x00\x00\x00", 6)
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_globalSpawModify
            )
    elif PVZ_data.PVZ_version == 2.3:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x00425855, b"\xeb", 1)
            PVZ_data.PVZ_memory.write_bytes(0x0042584E, b"\x90\x90\x90\x90\x90", 5)
            newmem_globalSpawModify = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 256
            )
            shellcode = asm.Asm(newmem_globalSpawModify)
            for i in range(0, 56):
                if str(i) in zombieTypes:
                    print(i)
                    shellcode.mov_byte_ptr_exx_add_dword_byte(asm.EDX, 0x57D4 + i, 1)
                else:
                    shellcode.mov_byte_ptr_exx_add_dword_byte(asm.EDX, 0x57D4 + i, 0)

            shellcode.jmp(0x00425D1D)
            PVZ_data.PVZ_memory.write_bytes(
                newmem_globalSpawModify,
                bytes(shellcode.code[: shellcode.index]),
                shellcode.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x0082401F,
                b"\xe9"
                + calculate_call_address(newmem_globalSpawModify - 0x00824024)
                + b"\x90",
                6,
            )
            spawisModified()
        else:
            PVZ_data.PVZ_memory.write_bytes(0x00425855, b"\x7f", 1)
            PVZ_data.PVZ_memory.write_bytes(0x0042584E, b"\xe9\xad\xaa\x48\x00", 5)
            PVZ_data.PVZ_memory.write_bytes(0x0082401F, b"\x0f\x85\x21\x00\x00\x00", 6)
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_globalSpawModify
            )
    elif (
        PVZ_data.PVZ_version == 2.35
        or PVZ_data.PVZ_version == 2.36
        or PVZ_data.PVZ_version == 2.37
    ):
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x00425855, b"\xeb", 1)
            PVZ_data.PVZ_memory.write_bytes(0x0042584E, b"\x90\x90\x90\x90\x90", 5)
            newmem_globalSpawModify = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 256
            )
            shellcode = asm.Asm(newmem_globalSpawModify)
            for i in range(0, 59):
                if str(i) in zombieTypes:
                    print(i)
                    shellcode.mov_byte_ptr_exx_add_dword_byte(asm.EDX, 0x57D4 + i, 1)
                else:
                    shellcode.mov_byte_ptr_exx_add_dword_byte(asm.EDX, 0x57D4 + i, 0)

            shellcode.jmp(0x00425D1D)
            PVZ_data.PVZ_memory.write_bytes(
                newmem_globalSpawModify,
                bytes(shellcode.code[: shellcode.index]),
                shellcode.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x0082401F,
                b"\xe9"
                + calculate_call_address(newmem_globalSpawModify - 0x00824024)
                + b"\x90",
                6,
            )
            spawisModified()
        else:
            PVZ_data.PVZ_memory.write_bytes(0x00425855, b"\x7f", 1)
            PVZ_data.PVZ_memory.write_bytes(0x0042584E, b"\xe9\xad\xaa\x48\x00", 5)
            PVZ_data.PVZ_memory.write_bytes(0x0082401F, b"\x0f\x85\x21\x00\x00\x00", 6)
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_globalSpawModify
            )
    elif PVZ_data.PVZ_version == 2.4:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x00425855, b"\xeb", 1)
            PVZ_data.PVZ_memory.write_bytes(0x0042584E, b"\x90\x90\x90\x90\x90", 5)
            newmem_globalSpawModify = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 256
            )
            shellcode = asm.Asm(newmem_globalSpawModify)
            for i in range(0, 63):
                if str(i) in zombieTypes:
                    print(i)
                    shellcode.mov_byte_ptr_exx_add_dword_byte(asm.EDX, 0x57D4 + i, 1)
                else:
                    shellcode.mov_byte_ptr_exx_add_dword_byte(asm.EDX, 0x57D4 + i, 0)

            shellcode.jmp(0x00425D1D)
            PVZ_data.PVZ_memory.write_bytes(
                newmem_globalSpawModify,
                bytes(shellcode.code[: shellcode.index]),
                shellcode.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x0082401F,
                b"\xe9"
                + calculate_call_address(newmem_globalSpawModify - 0x00824024)
                + b"\x90",
                6,
            )
            spawisModified()
        else:
            PVZ_data.PVZ_memory.write_bytes(0x00425855, b"\x7f", 1)
            PVZ_data.PVZ_memory.write_bytes(0x0042584E, b"\xe9\xad\xaa\x48\x00", 5)
            PVZ_data.PVZ_memory.write_bytes(0x0082401F, b"\x0f\x85\x21\x00\x00\x00", 6)
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_globalSpawModify
            )


def changeZombieHead(f, zombieType):
    print("changehead" + str(f))
    global newmem_changeZombieHead
    global newmem_changeZombieDeadHead
    if PVZ_data.PVZ_version == 2.0:
        if f:
            newmem_changeZombieHead = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 256
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
            PVZ_data.PVZ_memory.write_bytes(
                newmem_changeZombieHead,
                bytes(shellcode.code[: shellcode.index]),
                shellcode.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x0052AF8B,
                b"\xe9"
                + calculate_call_address(newmem_changeZombieHead - 0x0052AF90)
                + b"\x90\x90",
                7,
            )
            newmem_changeZombieDeadHead = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 256
            )
            shellcode2 = asm.Asm(newmem_changeZombieDeadHead)
            shellcode2.cmp_exx_byte(asm.EAX, zombieType)
            shellcode2.jne_long_offset(0xB)
            shellcode2.mov_exx_dword_ptr(asm.ESI, 0x006A7A08)
            shellcode2.jmp(0x00529D07)
            shellcode2.cmp_exx_byte(asm.EAX, 0x23)
            shellcode2.jne(0x0084E4E4)
            shellcode2.jmp(0x0084E4D9)
            PVZ_data.PVZ_memory.write_bytes(
                newmem_changeZombieDeadHead,
                bytes(shellcode2.code[: shellcode2.index]),
                shellcode2.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x0084E4D0,
                b"\xe9"
                + calculate_call_address(newmem_changeZombieDeadHead - 0x0084E4D5)
                + b"\x90\x90\x90\x90",
                9,
            )
        else:
            PVZ_data.PVZ_memory.write_bytes(
                0x0052AF8B, b"\x8b\x46\x58\x83\x46\x54\xff", 7
            )
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_changeZombieHead
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x0084E4D0, b"\x83\xf8\x23\x0f\x85\x0b\x00\x00\x00", 9
            )
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_changeZombieDeadHead
            )
    elif PVZ_data.PVZ_version == 2.1 or PVZ_data.PVZ_version >= 2.2:
        if f:
            newmem_changeZombieHead = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 256
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
            PVZ_data.PVZ_memory.write_bytes(
                newmem_changeZombieHead,
                bytes(shellcode.code[: shellcode.index]),
                shellcode.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x0052AF8B,
                b"\xe9"
                + calculate_call_address(newmem_changeZombieHead - 0x0052AF90)
                + b"\x90\x90",
                7,
            )
            newmem_changeZombieDeadHead = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 256
            )
            shellcode2 = asm.Asm(newmem_changeZombieDeadHead)
            shellcode2.cmp_exx_byte(asm.EAX, zombieType)
            shellcode2.jne_long_offset(0xB)
            shellcode2.mov_exx_dword_ptr(asm.ESI, 0x006A7A08)
            shellcode2.jmp(0x00529D07)
            shellcode2.cmp_exx_byte(asm.EAX, 0x23)
            shellcode2.jne(0x008A9214)
            shellcode2.jmp(0x008A9209)
            PVZ_data.PVZ_memory.write_bytes(
                newmem_changeZombieDeadHead,
                bytes(shellcode2.code[: shellcode2.index]),
                shellcode2.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x008A9200,
                b"\xe9"
                + calculate_call_address(newmem_changeZombieDeadHead - 0x008A9205)
                + b"\x90\x90\x90\x90",
                9,
            )
        else:
            PVZ_data.PVZ_memory.write_bytes(
                0x0052AF8B, b"\x8b\x46\x58\x83\x46\x54\xff", 7
            )
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_changeZombieHead
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x008A9200, b"\x83\xf8\x23\x0f\x85\x0b\x00\x00\x00", 9
            )
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_changeZombieDeadHead
            )


def deathrattleCallZombie(f, deadZombieType):
    global newmem_deathrattleCallZombie
    if f:
        newmem_deathrattleCallZombie = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 256
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
        if PVZ_data.PVZ_version == 2.0:
            shellcode.mov_exx(asm.EAX, 42)
        else:
            shellcode.mov_exx(asm.EAX, 45)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_byte(asm.EAX, 25)
        shellcode.nop_6()
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
        PVZ_data.PVZ_memory.write_bytes(
            newmem_deathrattleCallZombie,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x00529A30,
            b"\xe9"
            + calculate_call_address(newmem_deathrattleCallZombie - 0x00529A35)
            + b"\x90",
            6,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00529A30, b"\x55\x8b\xec\x83\xe4\xf8", 6)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_deathrattleCallZombie
        )


newmem_zombieDeadZombie = None


def zombieDeadZombie(f, deadZombieType, bossWeight, bosshp):
    global newmem_zombieDeadZombie
    # [ENABLE]
    # //code from here to '[DISABLE]' will be used to enable the cheat
    # alloc(newmem,2048)
    # label(returnhere)
    # label(originalcode)
    #
    # newmem:
    # cmp [ebp+24],#24
    # jne originalcode
    # pushad
    # push 47//特效ID
    # push 00061A80
    # sub esp,10
    # mov [esp],#40//y偏移
    # mov [esp+4],#40//x偏移
    # fild dword ptr [ebp+c]//y
    # fiadd dword ptr [esp]
    # fstp dword ptr [esp+c]
    # fild dword ptr [ebp+8]//x
    # fiadd dword ptr [esp+4]
    # fstp dword ptr [esp+8]
    # mov esi,[6A9EC0]
    # mov esi,[esi+00000820]
    # mov esi,[esi]
    # add esp,8
    # call PlantsVsZombies.exe+118A70
    # popad
    # pushad
    # mov edi,ebp
    # mov eax,[6a9ec0]
    # cmp [eax+7fc],3
    # jne end
    # mov eax,[eax+768]
    # cmp byte ptr [eax+164],1
    # je end
    # cmp [edi+24],#24
    # jne end
    #
    # RZ:
    # mov eax,#999
    # call 5af400
    # cmp eax,60
    # mov eax,#25
    # jl CZ
    #
    # mov eax,#41
    # call 5af400
    # cmp eax,#19
    # je RZ
    # CZ:
    # push [edi+1c]//row
    # push eax//id
    # mov eax,[edi+4]//*Board
    # call 40ddc0
    # fld [edi+2c]
    # fstp [eax+2c]
    # mov [eax+1b0],1
    #
    # end:
    # popad
    # mov [ebp+28],3
    #
    # originalcode:
    # push ebp
    # mov ebp,esp
    # and esp,-08
    # jmp returnhere
    #
    #
    #
    # "PlantsVsZombies.exe"+129A30:
    # jmp newmem
    # nop
    # returnhere:
    #
    #
    #
    #
    # [DISABLE]
    # //code from here till the end of the code will be used to disable the cheat
    # dealloc(newmem)
    # "PlantsVsZombies.exe"+129A30:
    # push ebp
    # mov ebp,esp
    # and esp,-08
    # //Alt: db 55 8B EC 83 E4 F8
    if f:
        newmem_zombieDeadZombie = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_zombieDeadZombie)
        shellcode.cmp_byte_ptr_exx_add_byte_byte(asm.EBP, 0x24, deadZombieType)
        shellcode.jne_label("originalcode")
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
        shellcode.jne_label("end")
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x768)
        shellcode.cmp_byte_ptr_exx_add_dword_byte(asm.EAX, 0x164, 1)
        shellcode.je_label("end")
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EDI, 0x24, deadZombieType)
        shellcode.jne_label("end")
        shellcode.create_label("RZ")
        shellcode.mov_exx(asm.EAX, 999)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_dword(asm.EAX, bossWeight)
        shellcode.mov_exx(asm.EAX, 25)
        shellcode.jl_label("CZ")
        if PVZ_data.PVZ_version == 2.0:
            shellcode.mov_exx(asm.EAX, 41)
        elif PVZ_data.PVZ_version == 2.1:
            shellcode.mov_exx(asm.EAX, 44)
        elif PVZ_data.PVZ_version == 2.2:
            shellcode.mov_exx(asm.EAX, 51)
        else:
            shellcode.mov_exx(asm.EAX, 56)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_byte(asm.EAX, 25)
        shellcode.je_label("RZ")
        shellcode.create_label("CZ")
        shellcode.push_ptr_exx_add_byte(asm.EDI, 0x1C)
        shellcode.push_exx(asm.EAX)
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EAX, asm.EDI, 4)
        shellcode.call(0x0040DDC0)
        shellcode.cmp_byte_ptr_exx_add_dword_byte(asm.EDI, 0xB8, 1)
        shellcode.jne_label("bumeihuo")
        shellcode.mov_byte_ptr_exx_add_dword_byte(asm.EAX, 0xB8, 1)
        shellcode.create_label("bumeihuo")
        shellcode.fld_dword_ptr_exx_add_byte(asm.EDI, 0x2C)
        shellcode.fstp_dword_ptr_exx_add_byte(asm.EAX, 0x2C)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EAX, 0x24, 25)
        shellcode.jne_label("end")
        if bosshp != 0:
            shellcode.mov_ptr_exx_add_dword_dword(asm.EAX, 0xC8, bosshp)
            shellcode.mov_ptr_exx_add_dword_dword(asm.EAX, 0xCC, bosshp)
        shellcode.create_label("end")
        shellcode.popad()
        shellcode.mov_ptr_exx_add_byte_dword(asm.EBP, 0x28, 3)
        shellcode.create_label("originalcode")
        shellcode.push_exx(asm.EBP)
        shellcode.mov_exx_eyy(asm.EBP, asm.ESP)
        shellcode.add_bytes(b"\x83\xe4\xf8")
        shellcode.jmp(0x00529A36)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_zombieDeadZombie,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x00529A30,
            b"\xe9"
            + calculate_call_address(newmem_zombieDeadZombie - 0x00529A35)
            + b"\x90",
            6,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00529A30, b"\x55\x8b\xec\x83\xe4\xf8", 6)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_zombieDeadZombie
        )


def reserveMaterialDropAllCard(f, zombieWeight, lmpWeight):
    global newmem_reserveMaterialDropAllCard
    if f:
        newmem_reserveMaterialDropAllCard = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 256
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
        shellcode.jmp_dword_offset(0x3B)
        shellcode.mov_exx(asm.EAX, 48)
        shellcode.call(0x005AF400)
        shellcode.jmp_dword_offset(0x2C)
        shellcode.mov_exx(asm.EAX, 99)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_byte(asm.EAX, lmpWeight)
        shellcode.jl_long_offset(0x14)
        if PVZ_data.PVZ_version == 2.0:
            shellcode.mov_exx(asm.EAX, 42)
        else:
            shellcode.mov_exx(asm.EAX, 45)
        shellcode.call(0x005AF400)
        shellcode.add_exx_dword(asm.EAX, 0x100)
        shellcode.jmp_dword_offset(0x5)
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
        PVZ_data.PVZ_memory.write_bytes(
            newmem_reserveMaterialDropAllCard,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x008689F2,
            b"\xe9"
            + calculate_call_address(newmem_reserveMaterialDropAllCard - 0x008689F7),
            5,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x008689F2, b"\x89\x43\x68\x61\x60", 5)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_reserveMaterialDropAllCard
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
        card_num = PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
            )
            + 0xF4
        )
        print(card_num)
    except:
        return
    i = 0
    j = 0
    while i < card_num:
        card_addresss = (
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0xE4
            )
            + 0x104 * j
        )
        card_exist = PVZ_data.PVZ_memory.read_bytes(card_addresss + 0x38, 1)
        if card_exist == b"\x00":
            card_plant_type = PVZ_data.PVZ_memory.read_int(card_addresss + 0x68)
            if type == 0:
                if card_plant_type < 255:
                    PVZ_data.PVZ_memory.write_bytes(card_addresss + 0x38, b"\x01", 1)
                    PVZ_data.PVZ_memory.write_bytes(card_addresss + 0x3C, b"\x01", 1)
            elif type == 1:
                if card_plant_type > 255:
                    PVZ_data.PVZ_memory.write_bytes(card_addresss + 0x38, b"\x01", 1)
                    PVZ_data.PVZ_memory.write_bytes(card_addresss + 0x3C, b"\x01", 1)
            i = i + 1
        j = j + 1


def cardsNotDisappear(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x00430DD1, b"\x00", 1)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00430DD1, b"\x01", 1)


def lockLevel(f, level):
    divzero(1)
    unlimitedMonsterSpawning(1)
    global newmem_lockLevel
    if f:
        newmem_lockLevel = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_lockLevel)
        shellcode.mov_exx(asm.EAX, level)
        shellcode.mov_ptr_exx_add_dword_eyy(asm.ESI, 0x7F8, asm.EAX)
        shellcode.jmp(0x0044F587)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_lockLevel,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0044F581,
            b"\xe9" + calculate_call_address(newmem_lockLevel - 0x0044F586) + b"\x90",
            6,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0044F581, b"\x89\x86\xf8\x07\x00\x00", 6)
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_lockLevel)


def divzero(f):
    global newmem_divzero
    if f:
        print("divzero")
        newmem_divzero = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 256
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
        PVZ_data.PVZ_memory.write_bytes(
            newmem_divzero,
            bytes(shellcode2.code[: shellcode2.index]),
            shellcode2.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x005A9A47,
            b"\xe9" + calculate_call_address(newmem_divzero - 0x005A9A4C) + b"\x90",
            6,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x005A9A47, b"\xf7\x74\x24\x04\x8b\xc2", 6)
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_divzero)


def unlimitedMonsterSpawning(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x0041C078, b"\xeb", 1)
        PVZ_data.PVZ_memory.write_bytes(0x0040D91F, b"\xeb", 1)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0041C078, b"\x74", 1)
        PVZ_data.PVZ_memory.write_bytes(0x0040D91F, b"\x74", 1)


def bungeeFix(f):
    global newmem_bungeeTipFix
    global newmem_bungeePutFix
    if f:
        newmem_bungeeTipFix = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_bungeeTipFix)
        shellcode.cmp_dword_ptr_exx_add_byte_dword(asm.ECX, 0x28, 276)
        shellcode.jne(0x0042A35A)
        shellcode.jmp(0x0042A2F5)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_bungeeTipFix,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0042A2EF,
            b"\xe9"
            + calculate_call_address(newmem_bungeeTipFix - 0x0042A2F4)
            + b"\x90",
            6,
        )
        newmem_bungeePutFix = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 256
        )
        shellcode2 = asm.Asm(newmem_bungeePutFix)
        shellcode2.cmp_exx_dword(asm.EBP, 276)
        shellcode2.jne(0x004255F2)
        shellcode2.jmp(0x004255E6)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_bungeePutFix,
            bytes(shellcode2.code[: shellcode2.index]),
            shellcode2.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x004255E1,
            b"\xe9" + calculate_call_address(newmem_bungeePutFix - 0x004255E6),
            5,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0042A2EF, b"\x83\x79\x28\x42\x75\x65", 6)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_bungeeTipFix
        )
        PVZ_data.PVZ_memory.write_bytes(0x004255E1, b"\x83\xfd\x42\x75\x0c", 5)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_bungeePutFix
        )


def setZombieRedLine(row):
    print(row)
    PVZ_data.PVZ_memory.write_int(0x004255DD, row)
    PVZ_data.PVZ_memory.write_int(0x004253F7, 20 + row * 80)


def findBoss():
    bossList = []
    try:
        zombie_num = PVZ_data.PVZ_memory.read_int(
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
            )
            + 0xA0
        )
    except:
        return
    i = 0
    j = 0
    while i < zombie_num:
        zombie_addresss = (
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0x90
            )
            + 0x204 * j
        )
        zombie_exist = PVZ_data.PVZ_memory.read_bytes(zombie_addresss + 0xEC, 1)
        if zombie_exist == b"\x00":
            z = PVZ_data.zombie(zombie_addresss)
            if z.type == 25:
                bossList.append(z)
            i = i + 1
        j = j + 1
    return bossList


def nightSun(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x0040B196, b"\xeb\x14", 2)
        PVZ_data.PVZ_memory.write_bytes(
            0x00413A76, b"\x90\x90\x90\x53\x57\xeb\x28\x90\x90\x90\x90", 11
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0040B196, b"\x74\x29", 2)
        PVZ_data.PVZ_memory.write_bytes(
            0x00413A76, b"\x83\xf8\x01\x53\x57\x0f\x84\x70\x01\x00\x00", 11
        )


newmem_bossCorrect_Outerleg = None


def bossCorrect_Outerleg(f):
    global newmem_bossCorrect_Outerleg
    if f:
        newmem_bossCorrect_Outerleg = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_bossCorrect_Outerleg)
        shellcode.mov_ptr_exx_add_eyy_times_add_byte_doword(asm.EBX, asm.ECX, 4, 8, 0)
        shellcode.add_ptr_exx_add_eyy_times_add_byte_ezz(
            asm.EBX, asm.ECX, 4, 8, asm.EBP
        )
        shellcode.lea_exx_ptr_eyy_add_ezz_times(asm.ECX, asm.EBX, asm.ECX, 4)
        shellcode.push_dword(0x004167B1)
        shellcode.ret()

        PVZ_data.PVZ_memory.write_bytes(
            newmem_bossCorrect_Outerleg,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x004167A8,
            b"\xe9"
            + calculate_call_address(newmem_bossCorrect_Outerleg - 0x004167AD)
            + b"\x90\x90\x90\x90\x90\x90",
            11,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(
            0x004167A8, b"\xc7\x44\x8b\x08\x00\x00\x00\x00\x8d\x0c\x8b", 11
        )
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_bossCorrect_Outerleg
        )


newmem_bossCorrect_body = None


def bossCorrect_body(f):
    global newmem_bossCorrect_body
    if f:
        newmem_bossCorrect_body = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 128
        )
        shellcode = asm.Asm(newmem_bossCorrect_body)
        shellcode.mov_ptr_exx_add_eyy_times_add_byte_doword(asm.EBX, asm.ECX, 4, 8, 1)
        shellcode.add_ptr_exx_add_eyy_times_add_byte_ezz(
            asm.EBX, asm.ECX, 4, 8, asm.EBP
        )
        shellcode.lea_exx_ptr_eyy_add_ezz_times(asm.ECX, asm.EBX, asm.ECX, 4)
        shellcode.push_dword(0x004167DC)
        shellcode.ret()

        PVZ_data.PVZ_memory.write_bytes(
            newmem_bossCorrect_body,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x004167D1,
            b"\xe9"
            + calculate_call_address(newmem_bossCorrect_body - 0x004167D6)
            + b"\x90\x90\x90\x90\x90\x90",
            11,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(
            0x004167D1, b"\xc7\x44\x8b\x08\x01\x00\x00\x00\x8d\x0c\x8b", 11
        )
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_bossCorrect_body
        )


newmem_bossCorrect_Innerleg = None


def bossCorrect_Innerleg(f):
    global newmem_bossCorrect_Innerleg
    if f:
        newmem_bossCorrect_Innerleg = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 128
        )
        shellcode = asm.Asm(newmem_bossCorrect_Innerleg)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ECX, 0x08, 0x02)
        shellcode.add_ptr_exx_add_byte_eyy(asm.ECX, 0x08, asm.EBP)
        shellcode.lea_exx_ptr_eyy_add_ezz_times_add_byte(
            asm.ECX, asm.EAX, asm.EAX, 2, 9
        )
        shellcode.push_dword(0x004167FE)
        shellcode.ret()

        PVZ_data.PVZ_memory.write_bytes(
            newmem_bossCorrect_Innerleg,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x004167F4,
            b"\xe9"
            + calculate_call_address(newmem_bossCorrect_Innerleg - 0x004167F9)
            + b"\x90\x90\x90\x90\x90\x90",
            11,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(
            0x004167F4, b"\xc7\x41\x08\x02\x00\x00\x00\x8d\x4c\x40\x09", 11
        )
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_bossCorrect_Innerleg
        )


newmem_bossCorrect_Innerarm = None


def bossCorrect_Innerarm(f):
    global newmem_bossCorrect_Innerarm
    # mov [ecx+08],00000003
    # add [ecx+08],ebp
    # mov edx,[edx+0000008C]
    # push 00416821
    # ret
    if f:
        newmem_bossCorrect_Innerarm = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 128
        )
        shellcode = asm.Asm(newmem_bossCorrect_Innerarm)
        shellcode.mov_ptr_exx_add_byte_dword(asm.ECX, 0x08, 0x03)
        shellcode.add_ptr_exx_add_byte_eyy(asm.ECX, 0x08, asm.EBP)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EDX, asm.EDX, 0x8C)
        shellcode.push_dword(0x00416821)
        shellcode.ret()

        PVZ_data.PVZ_memory.write_bytes(
            newmem_bossCorrect_Innerarm,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x00416815,
            b"\xe9"
            + calculate_call_address(newmem_bossCorrect_Innerarm - 0x0041681A)
            + b"\x90\x90\x90\x90\x90\x90\x90\x90",
            13,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(
            0x00416815, b"\xc7\x41\x08\x03\x00\x00\x00\x8b\x92\x8c\x00\x00\x00", 13
        )
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_bossCorrect_Innerarm
        )


newmem_bossCorrect_Ball = None


def bossCorrect_Ball(f):
    global newmem_bossCorrect_Ball
    # mov [ebx+08],00000004
    # add [ebx+08],ebp
    # mov [edi],eax
    # push 00416870
    # ret
    if f:
        newmem_bossCorrect_Ball = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_bossCorrect_Ball)
        shellcode.mov_ptr_exx_add_byte_dword(asm.EBX, 0x08, 0x04)
        shellcode.add_ptr_exx_add_byte_eyy(asm.EBX, 0x08, asm.EBP)
        shellcode.mov_ptr_exx_eyy(asm.EDI, asm.EAX)
        shellcode.push_dword(0x00416870)
        shellcode.ret()

        PVZ_data.PVZ_memory.write_bytes(
            newmem_bossCorrect_Ball,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x00416867,
            b"\xe9"
            + calculate_call_address(newmem_bossCorrect_Ball - 0x0041686C)
            + b"\x90\x90\x90\x90",
            9,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(
            0x00416867, b"\xc7\x43\x08\x04\x00\x00\x00\x89\x07", 9
        )
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_bossCorrect_Ball
        )


newmem_bossCorrect_iterate = None


def bossCorrect_iterate(f):
    global newmem_bossCorrect_iterate
    # mov edx,[ebx]
    # mov edi,edx
    # mov eax,[ebp+08]
    # mov eax,[eax+00000090]
    # cmp edx,eax
    # db 7D 06
    # push 0041732E
    # ret
    # sub edx,eax
    # mov cx,[0041C911]
    # xchg eax,edx
    # cdq
    # sub eax,edx
    # idiv cx
    # sub edi,edx
    # mov [ebx],edx
    # mov eax,edi
    # push 00417124
    # ret

    if f:
        newmem_bossCorrect_iterate = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 256
        )
        shellcode = asm.Asm(newmem_bossCorrect_iterate)
        shellcode.mov_exx_dword_ptr_eyy(asm.EDX, asm.EBX)
        shellcode.mov_exx_eyy(asm.EDI, asm.EDX)
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EAX, asm.EBP, 0x8)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x90)
        shellcode.cmp_exx_eyy(asm.EDX, asm.EAX)
        shellcode.jnl_offset(0x06)
        shellcode.push_dword(0x0041732E)
        shellcode.ret()
        shellcode.sub_exx_eyy(asm.EDX, asm.EAX)
        shellcode.mov_ex_ptr_dword(asm.CX, 0x0041C911)
        shellcode.xchg_exx_eyy(asm.EAX, asm.EDX)
        shellcode.cdq()
        shellcode.sub_exx_eyy(asm.EAX, asm.EDX)
        shellcode.idiv_ex(asm.CX)
        shellcode.sub_exx_eyy(asm.EDI, asm.EDX)
        shellcode.mov_ptr_exx_eyy(asm.EBX, asm.EDX)
        shellcode.mov_exx_eyy(asm.EAX, asm.EDI)
        shellcode.push_dword(0x00417124)
        shellcode.ret()

        PVZ_data.PVZ_memory.write_bytes(
            newmem_bossCorrect_iterate,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0041711A,
            b"\xe9"
            + calculate_call_address(newmem_bossCorrect_iterate - 0x0041711F)
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(
            0x0041711A, b"\x8b\x55\x08\xe8\x6e\x62\x00\x00\x8b\xf8", 10
        )
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_bossCorrect_iterate
        )


newmem_bossCorrect_Coordinate = None


def bossCorrect_Coordinate(f):
    global newmem_bossCorrect_Coordinate
    # fldz
    # fstp dword ptr [edi+30]
    # mov ecx,edi
    # db E8 26 00 00 00
    # test al,al
    # db 74 0E
    # fld dword ptr [00679FE4]
    # fadd dword ptr [00679498]
    # db EB 02
    # fldz
    # fstp dword ptr [edi+2C]
    # fild dword ptr [edi+08]
    # mov esi,[ebp+0C]
    # mov edx,[ebx]
    # push edx
    # push 0041713F
    # ret
    # push 0052BEE0
    # ret

    if f:
        newmem_bossCorrect_Coordinate = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 128
        )
        shellcode = asm.Asm(newmem_bossCorrect_Coordinate)
        shellcode.fldz()
        shellcode.fstp_dword_ptr_exx_add_byte(asm.EDI, 0x30)
        shellcode.mov_exx_eyy(asm.ECX, asm.EDI)
        shellcode.call(newmem_bossCorrect_Coordinate + 0x32)
        shellcode.test_8(asm.AL, asm.AL)
        shellcode.je_short_offset(0x0E)
        shellcode.fld_dword_ptr_address(0x00679FE4)
        shellcode.fadd_dword_ptr_address(0x00679498)
        shellcode.jmp_short_offset(2)
        shellcode.fldz()
        shellcode.fstp_dword_ptr_exx_add_byte(asm.EDI, 0x2C)
        shellcode.fild_dword_ptr_exx_add_byte(asm.EDI, 0x08)
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ESI, asm.EBP, 0x0C)
        shellcode.mov_exx_dword_ptr_eyy(asm.EDX, asm.EBX)
        shellcode.push_exx(asm.EDX)
        shellcode.push_dword(0x0041713F)
        shellcode.ret()
        shellcode.push_dword(0x0052BEE0)
        shellcode.ret()

        PVZ_data.PVZ_memory.write_bytes(
            newmem_bossCorrect_Coordinate,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x00417136,
            b"\xe9"
            + calculate_call_address(newmem_bossCorrect_Coordinate - 0x0041713B)
            + b"\x90\x90\x90\x90",
            9,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(
            0x00417136, b"\xdb\x47\x08\x8b\x75\x0c\x8b\x13\x52", 9
        )
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_bossCorrect_Coordinate
        )


newmem_bossCorrect_fire_melting_iceBall = None


def bossCorrect_fire_melting_iceBall(f):
    global newmem_bossCorrect_fire_melting_iceBall
    # pushad
    # push 00
    # mov esi,esp
    # mov edx,[edi+04]
    # db E8 27 00 00 00
    # test al,al
    # db 74 19
    # mov esi,[esi]
    # cmp dword ptr [esi+24],19
    # db 75 EA
    # cmp byte ptr [esi+000000B8],01
    # db 74 E1
    # push esi
    # db E8 12 00 00 00
    # db EB D9
    # add esp,04
    # popad
    # push 004664A5
    # ret
    # push 0041C8F0
    # ret
    # push 005356D0
    # ret

    if f:
        newmem_bossCorrect_fire_melting_iceBall = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 2048
        )
        shellcode = asm.Asm(newmem_bossCorrect_fire_melting_iceBall)
        shellcode.pushad()
        shellcode.push_byte(0)
        shellcode.mov_exx_eyy(asm.ESI, asm.ESP)
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EDX, asm.EDI, 0x04)
        shellcode.call(newmem_bossCorrect_fire_melting_iceBall + 0x34)
        shellcode.test_8(asm.AL, asm.AL)
        shellcode.je_short_offset(0x19)
        shellcode.mov_exx_dword_ptr_eyy(asm.ESI, asm.ESI)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x24, 0x19)
        shellcode.jne_short_offset(0xEA)
        shellcode.cmp_byte_ptr_exx_add_dword_byte(asm.ESI, 0xB8, 0x01)
        shellcode.je_short_offset(0xE1)
        shellcode.push_exx(asm.ESI)
        shellcode.call(newmem_bossCorrect_fire_melting_iceBall + 0x3A)
        shellcode.jmp_short_offset(0xD9)
        shellcode.add_exx_byte(asm.ESP, 0x04)
        shellcode.popad()
        shellcode.push_dword(0x004664A5)
        shellcode.ret()
        shellcode.push_dword(0x0041C8F0)
        shellcode.ret()
        shellcode.push_dword(0x005356D0)
        shellcode.ret()

        PVZ_data.PVZ_memory.write_bytes(
            newmem_bossCorrect_fire_melting_iceBall,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x00466493,
            b"\xe9"
            + calculate_call_address(
                newmem_bossCorrect_fire_melting_iceBall - 0x00466498
            )
            + b"\x90\x90\x90\x90\x90",
            10,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(
            0x00466493, b"\x8b\x57\x04\xe8\xf5\x6e\xfb\xff\x85\xc0", 10
        )
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_bossCorrect_fire_melting_iceBall
        )


newmem_bossCorrect_ice_melting_fireBall = None


def bossCorrect_ice_melting_fireBall(f):
    global newmem_bossCorrect_ice_melting_fireBall
    # [ENABLE]
    # //code from here to '[DISABLE]' will be used to enable the cheat
    # alloc(newmem,2048)
    # label(returnhere)
    #
    # newmem: //this is allocated memory, you have read,write,execute access
    # //place your code here
    # mov ebx,[esp+14]
    # pushad
    # push 00
    # mov esi,esp
    # mov edx,[edi+04]
    # db E8 30 00 00 00
    # test al,al
    # db 74 22
    # mov esi,[esi]
    # cmp dword ptr [esi+24],19
    # db 75 EA
    # cmp byte ptr [esi+000000B8],01
    # db 74 E1
    # cmp ebx,[esi+00000148]
    # db 75 D9
    # mov eax,esi
    # db E8 12 00 00 00
    # db EB D0
    # add esp,04
    # popad
    # push 004665A4
    # ret
    # push 0041C8F0
    # ret
    # push 00535630
    # ret
    #
    #
    # "PlantsVsZombies.exe"+66587:
    # jmp newmem
    # nop
    # nop
    # nop
    # returnhere:
    #
    #
    #
    #
    # [DISABLE]
    # //code from here till the end of the code will be used to disable the cheat
    # dealloc(newmem)
    # "PlantsVsZombies.exe"+66587:
    # db 8B 57 04 E8 01 6E FB FF
    # //mov edx,[edi+04]
    # //call 0041D390
    if f:
        newmem_bossCorrect_ice_melting_fireBall = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 2048
        )
        shellcode = asm.Asm(newmem_bossCorrect_ice_melting_fireBall)
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EBX, asm.ESP, 0x14)
        shellcode.pushad()
        shellcode.push_byte(0)
        shellcode.mov_exx_eyy(asm.ESI, asm.ESP)
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EDX, asm.EDI, 0x04)
        shellcode.call(newmem_bossCorrect_ice_melting_fireBall + 0x41)
        shellcode.test_8(asm.AL, asm.AL)
        shellcode.je_short_offset(0x22)
        shellcode.mov_exx_dword_ptr_eyy(asm.ESI, asm.ESI)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESI, 0x24, 0x19)
        shellcode.jne_short_offset(0xEA)
        shellcode.cmp_byte_ptr_exx_add_dword_byte(asm.ESI, 0xB8, 0x01)
        shellcode.je_short_offset(0xE1)
        shellcode.cmp_exx_ptr_eyy_add_dword(asm.EBX, asm.ESI, 0x148)
        shellcode.jne_short_offset(0xD9)
        shellcode.mov_exx_eyy(asm.EAX, asm.ESI)
        shellcode.call(newmem_bossCorrect_ice_melting_fireBall + 0x47)
        shellcode.jmp_short_offset(0xD0)
        shellcode.add_exx_byte(asm.ESP, 0x04)
        shellcode.popad()
        shellcode.push_dword(0x004665A4)
        shellcode.ret()
        shellcode.push_dword(0x0041C8F0)
        shellcode.ret()
        shellcode.push_dword(0x00535630)
        shellcode.ret()

        PVZ_data.PVZ_memory.write_bytes(
            newmem_bossCorrect_ice_melting_fireBall,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x00466587,
            b"\xe9"
            + calculate_call_address(
                newmem_bossCorrect_ice_melting_fireBall - 0x0046658C
            )
            + b"\x90\x90\x90\x90",
            9,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(
            0x00466587, b"\x8b\x57\x04\xe8\x01\x6e\xfb\xff", 9
        )
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_bossCorrect_ice_melting_fireBall
        )


newmem_bossCorrect_dead = None


def bossCorrect_dead(f):
    global newmem_bossCorrect_dead
    # [ENABLE]
    # //code from here to '[DISABLE]' will be used to enable the cheat
    # alloc(newmem,2048)
    # label(returnhere)
    # label(originalcode)
    # label(exit)
    #
    # newmem: //this is allocated memory, you have read,write,execute access
    # //place your code here
    # push ecx
    # mov ecx,edi
    # call 530510
    # pop ecx
    #
    # originalcode:
    # cmp dword ptr [ebx+5C],00
    # jle 00533D7A
    #
    # exit:
    # jmp returnhere
    #
    # "PlantsVsZombies.exe"+133D6D:
    # jmp newmem
    # nop
    # returnhere:
    #
    #
    #
    #
    # [DISABLE]
    # //code from here till the end of the code will be used to disable the cheat
    # dealloc(newmem)
    # "PlantsVsZombies.exe"+133D6D:
    # db 83 7B 5C 00 7E 07
    # //cmp dword ptr [ebx+5C],00
    # //jle 00533D7A
    if f:
        newmem_bossCorrect_dead = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 2048
        )
        shellcode = asm.Asm(newmem_bossCorrect_dead)
        shellcode.push_exx(asm.ECX)
        shellcode.mov_exx_eyy(asm.ECX, asm.EDI)
        shellcode.call(0x00530510)
        shellcode.pop_exx(asm.ECX)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x5C, 0)
        shellcode.jng(0x00533D7A)
        shellcode.jmp(0x00533D73)

        PVZ_data.PVZ_memory.write_bytes(
            newmem_bossCorrect_dead,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x00533D6D,
            b"\xe9"
            + calculate_call_address(newmem_bossCorrect_dead - 0x00533D72)
            + b"\x90",
            6,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00533D6D, b"\x83\x7b\x5c\x00\x7e\x07", 6)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_bossCorrect_dead
        )


def bossCorrect(f):
    bossCorrect_Outerleg(f)
    bossCorrect_body(f)
    bossCorrect_Innerleg(f)
    bossCorrect_Innerarm(f)
    bossCorrect_Ball(f)
    bossCorrect_iterate(f)
    bossCorrect_Coordinate(f)
    bossCorrect_fire_melting_iceBall(f)
    bossCorrect_ice_melting_fireBall(f)
    bossCorrect_dead(f)


def unpack(src_file, dst_dir):
    try:
        with open(src_file, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        return "UNPACK_SRC_NOT_EXIST"

    # 整个文件与 0xF7 异或
    data = bytes([b ^ 0xF7 for b in data])

    # 文件偏移量
    offset = 0

    # 检查文件头
    file_header_magic, file_header_version = struct.unpack_from("<II", data, offset)
    offset += 8

    if file_header_magic != 0xBAC04AC0 or file_header_version > 0x00000000:
        return "UNPACK_SRC_HEADER_ERROR"

    # 索引区域数据结构
    files_count = 0
    files_name = []
    files_size = []

    while True:
        (eof_flag,) = struct.unpack_from("<B", data, offset)
        offset += 1

        if eof_flag != 0x00 or eof_flag == 0x80:
            break

        (name_width,) = struct.unpack_from("<B", data, offset)
        offset += 1

        file_name = data[offset : offset + name_width].decode("utf-8", errors="ignore")
        offset += name_width

        (file_size,) = struct.unpack_from("<I", data, offset)
        offset += 4

        offset += 8  # skip file_time

        files_name.append(file_name)
        files_size.append(file_size)
        files_count += 1

    # 提取数据区所有文件
    for i in range(files_count):
        output_path = os.path.join(dst_dir, files_name[i])
        output_size = files_size[i]

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(data[offset : offset + output_size])

        offset += output_size

    return "UNPACK_SUCCESS"


def pack(src_dir, dst_file):
    # 获取源目录下的所有文件
    files = [
        os.path.join(root, file)
        for root, dirs, files in os.walk(src_dir)
        for file in files
    ]

    # 创建一个临时的二进制数据列表
    data = bytearray()

    # 写入文件头
    data.extend(struct.pack("<II", 0xBAC04AC0, 0x00000000))

    # 写入索引区域
    for file in files:
        # 获取文件名和大小
        name = os.path.relpath(file, src_dir)
        size = os.path.getsize(file)

        # 写入文件名长度和文件名
        name_utf8 = name.encode("utf-8")
        data.extend(struct.pack("<B", len(name_utf8)))
        data.extend(name_utf8)

        # 写入文件大小
        data.extend(struct.pack("<I", size))

        # 写入文件时间（这里简化为0）
        data.extend(struct.pack("<Q", 0))

    # 写入结束标志
    data.extend(struct.pack("<B", 0x80))

    # 写入数据区域
    for file in files:
        # 读取并写入文件内容
        with open(file, "rb") as src_f:
            data.extend(src_f.read())

    # 对整个文件进行异或操作
    data = bytearray([b ^ 0xF7 for b in data])

    # 写入目标文件
    with open(dst_file, "wb") as f:
        f.write(data)


newmem_zombieHitDeadSun = None


def zombieHitDeadSun(f, large_sun_weight, middle_sun_weight, small_sun_weight):
    global newmem_zombieHitDeadSun
    # [ENABLE]
    # //code from here to '[DISABLE]' will be used to enable the cheat
    # alloc(newmem,2048)
    # label(returnhere)
    # label(originalcode)
    # label(exit)
    #
    # newmem: //this is allocated memory, you have read,write,execute access
    # //place your code here
    # pushad
    # mov ebx,eax
    # mov eax,99
    # call 5AF400
    # cmp eax,1//大阳光概率
    # jg nolargesun
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 06
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    # jmp nosun
    #
    # nolargesun:
    # mov eax,99
    # call 5AF400
    # cmp eax,1//中阳光概率
    # jg nomiddlesun
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 04
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    # jmp nosun
    #
    # nomiddlesun:
    # mov eax,99
    # call 5AF400
    # cmp eax,80//小阳光概率
    # jg nosun
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 05
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    #
    #
    #
    # nosun:
    # popad
    #
    #
    # originalcode:
    # call 00530170
    #
    # exit:
    # jmp returnhere
    #
    # "PlantsVsZombies.exe"+1317A4:
    # jmp newmem
    # returnhere:
    #
    #
    #
    #
    # [DISABLE]
    # //code from here till the end of the code will be used to disable the cheat
    # dealloc(newmem)
    # "PlantsVsZombies.exe"+1317A4:
    # db E8 C7 E9 FF FF
    if f:
        newmem_zombieHitDeadSun = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 2048
        )
        shellcode = asm.Asm(newmem_zombieHitDeadSun)
        shellcode.pushad()
        shellcode.mov_exx_eyy(asm.EBX, asm.EAX)
        shellcode.mov_exx(asm.EAX, 99)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_byte(asm.EAX, large_sun_weight)
        shellcode.jg_long_offset(0x36)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x06)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.jmp_dword_offset(0x8D)
        shellcode.mov_exx(asm.EAX, 99)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_byte(asm.EAX, middle_sun_weight)
        shellcode.jg_long_offset(0x36)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x04)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.jmp_dword_offset(0x44)
        shellcode.mov_exx(asm.EAX, 99)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_byte(asm.EAX, small_sun_weight)
        shellcode.jg_long_offset(0x31)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x05)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.popad()
        shellcode.call(0x00530170)
        shellcode.jmp(0x005317A9)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_zombieHitDeadSun,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x005317A4,
            b"\xe9" + calculate_call_address(newmem_zombieHitDeadSun - 0x005317A9),
            5,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x005317A4, b"\xe8\xc7\xe9\xff\xff", 5)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_zombieHitDeadSun
        )


newmem_zombieBombDeadSun = None


def zombieBombDeadSun(f, large_sun_weight, middle_sun_weight, small_sun_weight):
    global newmem_zombieBombDeadSun
    # [ENABLE]
    # //code from here to '[DISABLE]' will be used to enable the cheat
    # alloc(newmem,2048)
    # label(returnhere)
    # label(originalcode)
    # label(exit)
    #
    # newmem: //this is allocated memory, you have read,write,execute access
    # //place your code here
    # pushad
    # mov ebx,eax
    # mov eax,99
    # call 5AF400
    # cmp eax,1//大阳光概率
    # jg nolargesun
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 06
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    # jmp nosun
    #
    # nolargesun:
    # mov eax,99
    # call 5AF400
    # cmp eax,10//中阳光概率
    # jg nomiddlesun
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 04
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    # jmp nosun
    #
    # nomiddlesun:
    # mov eax,99
    # call 5AF400
    # cmp eax,99//小阳光概率
    # jg nosun
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 05
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    #
    # nosun:
    # popad
    #
    #
    # originalcode:
    # call 00530170
    #
    # exit:
    # jmp returnhere
    #
    # "PlantsVsZombies.exe"+130301:
    # jmp newmem
    # returnhere:
    #
    #
    #
    #
    # [DISABLE]
    # //code from here till the end of the code will be used to disable the cheat
    # dealloc(newmem)
    # "PlantsVsZombies.exe"+130301:
    # db E8 6A FE FF FF
    # //call 00530170
    if f:
        newmem_zombieBombDeadSun = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 2048
        )
        shellcode = asm.Asm(newmem_zombieBombDeadSun)
        shellcode.pushad()
        shellcode.mov_exx_eyy(asm.EBX, asm.EAX)
        shellcode.mov_exx(asm.EAX, 99)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_byte(asm.EAX, large_sun_weight)
        shellcode.jg_long_offset(0x36)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x06)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.jmp_dword_offset(0x8D)
        shellcode.mov_exx(asm.EAX, 99)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_byte(asm.EAX, middle_sun_weight)
        shellcode.jg_long_offset(0x36)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x04)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.jmp_dword_offset(0x44)
        shellcode.mov_exx(asm.EAX, 99)
        shellcode.call(0x005AF400)
        shellcode.cmp_exx_byte(asm.EAX, small_sun_weight)
        shellcode.jg_long_offset(0x31)
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x05)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.popad()
        shellcode.call(0x00530170)
        shellcode.jmp(0x00530306)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_zombieBombDeadSun,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x00530301,
            b"\xe9" + calculate_call_address(newmem_zombieBombDeadSun - 0x00530306),
            5,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00530301, b"\xe8\x6a\xfe\xff\xff", 5)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_zombieBombDeadSun
        )


def zombieTypeDeadDropSun(f, large_sun_weight, middle_sun_weight, small_sun_weight):
    zombieTypeBomeDeadDropSun(f, large_sun_weight, middle_sun_weight, small_sun_weight)
    zombieTypeHitDeadDropSun(f, large_sun_weight, middle_sun_weight, small_sun_weight)


def zombieTypeHitDeadDropSun(f, type):
    global newmem_zombieTypeHitDeadDropSun
    # [ENABLE]
    # //code from here to '[DISABLE]' will be used to enable the cheat
    # alloc(newmem,2048)
    # label(returnhere)
    # label(originalcode)
    # label(exit)
    #
    # newmem: //this is allocated memory, you have read,write,execute access
    # //place your code here
    # pushad
    # mov ebx,eax
    # cmp [eax+24],2
    # jne nosun
    # pushad
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 06
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    # popad
    # pushad
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 06
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    # popad
    # pushad
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 06
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    # popad
    # pushad
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 06
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    # popad
    #
    #
    #
    # nosun:
    # popad
    #
    #
    # originalcode:
    # call 00530170
    #
    # exit:
    # jmp returnhere
    #
    # "PlantsVsZombies.exe"+1317A4:
    # jmp newmem
    # returnhere:
    #
    #
    #
    #
    # [DISABLE]
    # //code from here till the end of the code will be used to disable the cheat
    # dealloc(newmem)
    # "PlantsVsZombies.exe"+1317A4:
    # db E8 C7 E9 FF FF
    if f:
        newmem_zombieTypeHitDeadDropSun = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 2048
        )
        shellcode = asm.Asm(newmem_zombieTypeHitDeadDropSun)
        shellcode.pushad()
        shellcode.mov_exx_eyy(asm.EBX, asm.EAX)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x24, type)
        shellcode.jne_long_offset(0xCC)
        shellcode.pushad()
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x06)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.popad()
        shellcode.pushad()
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x06)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.popad()
        shellcode.pushad()
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x06)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.popad()
        shellcode.pushad()
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x06)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.popad()
        shellcode.popad()
        shellcode.call(0x00530170)
        shellcode.jmp(0x005317A9)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_zombieTypeHitDeadDropSun,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x005317A4,
            b"\xe9"
            + calculate_call_address(newmem_zombieTypeHitDeadDropSun - 0x005317A9),
            5,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x005317A4, b"\xe8\xc7\xe9\xff\xff", 5)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_zombieTypeHitDeadDropSun
        )


newmem_zombieTypeBomeDeadDropSun = None


def zombieTypeBomeDeadDropSun(f, type):
    global newmem_zombieTypeBomeDeadDropSun
    # [ENABLE]
    # //code from here to '[DISABLE]' will be used to enable the cheat
    # alloc(newmem,2048)
    # label(returnhere)
    # label(originalcode)
    # label(exit)
    #
    # newmem: //this is allocated memory, you have read,write,execute access
    # //place your code here
    # pushad
    # mov ebx,eax
    # cmp [eax+24],2
    # jne nosun
    # pushad
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 06
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    # popad
    # pushad
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 06
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    # popad
    # pushad
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 06
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    # popad
    # pushad
    # mov ecx,[6a9ec0]
    # mov ecx,[ecx+768]
    # push 02
    # push 06
    # fld [ebx+30]
    # sub esp,4
    # fistp [esp]
    # fld [ebx+2c]
    # sub esp,4
    # fistp [esp]
    # mov [00743F62],1
    # call 0040CB10
    # popad
    #
    # nosun:
    # popad
    #
    #
    # originalcode:
    # call 00530170
    #
    # exit:
    # jmp returnhere
    #
    # "PlantsVsZombies.exe"+130301:
    # jmp newmem
    # returnhere:
    #
    #
    #
    #
    # [DISABLE]
    # //code from here till the end of the code will be used to disable the cheat
    # dealloc(newmem)
    # "PlantsVsZombies.exe"+130301:
    # db E8 6A FE FF FF
    if f:
        newmem_zombieTypeBomeDeadDropSun = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 2048
        )
        shellcode = asm.Asm(newmem_zombieTypeBomeDeadDropSun)
        shellcode.pushad()
        shellcode.mov_exx_eyy(asm.EBX, asm.EAX)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBX, 0x24, type)
        shellcode.jne_long_offset(0xCC)
        shellcode.pushad()
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x06)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.popad()
        shellcode.pushad()
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x06)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.popad()
        shellcode.pushad()
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x06)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.popad()
        shellcode.pushad()
        shellcode.mov_exx_dword_ptr(asm.ECX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
        shellcode.push_byte(0x02)
        shellcode.push_byte(0x06)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x30)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.fld_dword_ptr_exx_add_byte(asm.EBX, 0x2C)
        shellcode.sub_exx_byte(asm.ESP, 0x04)
        shellcode.fistp_dword_ptr_exx(asm.ESP)
        shellcode.mov_ptr_dword_dword(0x00743F62, 1)
        shellcode.call(0x0040CB10)
        shellcode.popad()
        shellcode.popad()
        shellcode.call(0x00530170)
        shellcode.jmp(0x00530306)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_zombieTypeBomeDeadDropSun,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x00530301,
            b"\xe9"
            + calculate_call_address(newmem_zombieTypeBomeDeadDropSun - 0x00530306),
            5,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00530301, b"\xe8\x6a\xfe\xff\xff", 5)
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_zombieTypeBomeDeadDropSun
        )


newmem_infiniteItems = None


def infiniteItems(f):
    global newmem_infiniteItems
    if PVZ_data.PVZ_version == 2.0:
        pass
    elif PVZ_data.PVZ_version == 2.1 or PVZ_data.PVZ_version >= 2.2:
        if f:
            newmem_infiniteItems = pymem.memory.allocate_memory(
                PVZ_data.PVZ_memory.process_handle, 2048
            )
            shellcode = asm.Asm(newmem_infiniteItems)
            shellcode.pushad()
            shellcode.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
            shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x82C)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x208, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x20C, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x210, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x220, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1CB4, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1CB8, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1CBC, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1CC0, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1CC4, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1CEC, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1CF0, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1CF4, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1CF8, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1CFC, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1D00, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1D04, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1D08, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1D0C, 9999)
            shellcode.mov_dword_ptr_exx_add_dword_dowrd(asm.EAX, 0x1D10, 9999)
            shellcode.popad()
            shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.ECX, 0x28)
            shellcode.cmp_ptr_exx_add_byte_eyy(asm.ESI, 0x24, asm.EAX)
            shellcode.jmp(0x00538020)
            PVZ_data.PVZ_memory.write_bytes(
                newmem_infiniteItems,
                bytes(shellcode.code[: shellcode.index]),
                shellcode.index,
            )
            PVZ_data.PVZ_memory.write_bytes(
                0x0053801A,
                b"\xe9"
                + calculate_call_address(newmem_infiniteItems - 0x0053801F)
                + b"\x90",
                6,
            )
        else:
            PVZ_data.PVZ_memory.write_bytes(0x0053801A, b"\x8b\x41\x28\x39\x46\x24", 6)
            pymem.memory.free_memory(
                PVZ_data.PVZ_memory.process_handle, newmem_infiniteItems
            )


def PlatoonCannonBullet():
    # [ENABLE]
    # //code from here to '[DISABLE]' will be used to enable the cheat
    # alloc(newmem,2048)
    #
    # newmem: //this is allocated memory, you have read,write,execute access
    # //place your code here
    # mov edx,[esp+3C]
    # mov ecx,eax
    # cmp [ebp+24],0
    # jne long EX
    # push eax
    # mov eax,0000002E
    # XH:
    # mov [ecx+50],00000001
    # pushad
    # push 0000000B
    # push eax
    # mov edx,[ebp+04]
    # mov ecx,eax
    # mov eax,[ebp+08]
    # call 0041C550
    # mov edx,eax
    # inc edx
    # pop eax
    # push edx
    # mov ebx,000000FF
    # add ebx,eax
    # mov ecx,[ebp+08]
    # add ecx,50
    # push ebx
    # push eax
    # push ecx
    # mov eax,[ebp+04]
    # call 0040D620
    # mov [eax+58],0
    # mov [eax+68],270
    # mov [eax+88],1
    # mov byte ptr [eax+74],01
    # popad
    # add eax,30
    # cmp eax,00000200
    # jl XH
    # pop eax
    #
    # EX:
    # jmp 004672BB
    #
    #
    #
    #
    # 004672B5:
    # jmp newmem
    # nop
    #
    newmem = pymem.memory.allocate_memory(PVZ_data.PVZ_memory.process_handle, 256)
    shellcode = asm.Asm(newmem)
    shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EDX, asm.ESP, 0x3C)
    shellcode.mov_exx_eyy(asm.ECX, asm.EAX)
    shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.EBP, 0x24, 0)
    shellcode.jne_long_offset(0x66)
    shellcode.push_exx(asm.EAX)
    shellcode.mov_exx(asm.EAX, 0x2E)
    shellcode.mov_ptr_exx_add_byte_dword(asm.ECX, 0x50, 1)
    shellcode.pushad()
    shellcode.push_dword(0x0B)
    shellcode.push_exx(asm.EAX)
    shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EDX, asm.EBP, 0x04)
    shellcode.mov_exx_eyy(asm.ECX, asm.EAX)
    shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EAX, asm.EBP, 0x08)
    shellcode.call(0x0041C550)
    shellcode.mov_exx_eyy(asm.EDX, asm.EAX)
    shellcode.inc_exx(asm.EDX)
    shellcode.pop_exx(asm.EAX)
    shellcode.push_exx(asm.EDX)
    shellcode.mov_exx(asm.EBX, 0xFF)
    shellcode.add_exx_eyy(asm.EBX, asm.EAX)
    shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ECX, asm.EBP, 0x08)
    shellcode.add_exx_byte(asm.ECX, 0x50)
    shellcode.push_exx(asm.EBX)
    shellcode.push_exx(asm.EAX)
    shellcode.push_exx(asm.ECX)
    shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EAX, asm.EBP, 0x04)
    shellcode.call(0x0040D620)
    shellcode.mov_ptr_exx_add_byte_dword(asm.EAX, 0x58, 0)
    shellcode.mov_ptr_exx_add_byte_dword(asm.EAX, 0x68, 270)
    shellcode.mov_ptr_exx_add_dword_dword(asm.EAX, 0x88, 1)
    shellcode.mov_byte_ptr_exx_add_byte_byte(asm.EAX, 0x74, 1)
    shellcode.popad()
    shellcode.add_exx_byte(asm.EAX, 0x30)
    shellcode.cmp_exx_dword(asm.EAX, 0x200)
    shellcode.jl_offset(0xA1)
    shellcode.pop_exx(asm.EAX)
    shellcode.jmp(0x004672BB)
    PVZ_data.PVZ_memory.write_bytes(
        newmem, bytes(shellcode.code[: shellcode.index]), shellcode.index
    )
    PVZ_data.PVZ_memory.write_bytes(
        0x004672B5,
        b"\xe9" + calculate_call_address(newmem - 0x004672BA) + b"\x90",
        6,
    )


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

    PVZ_data.PVZ_memory.write_bytes(0x0040BC98, b"\xeb\x60", 2)
    PVZ_data.PVZ_memory.write_bytes(0x00458002, b"\xfc\x99", 2)
    PVZ_data.PVZ_memory.write_bytes(0x0040BD17, b"\x01", 1)
    asm.runThread(carsRecovery())
    PVZ_data.PVZ_memory.write_bytes(0x0040BC98, b"\x75\x09", 2)
    PVZ_data.PVZ_memory.write_bytes(0x00458002, b"\xf8\x9b", 2)
    PVZ_data.PVZ_memory.write_bytes(0x0040BD17, b"\x00", 1)


def pauseSpawn(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x004265DC, b"\xeb", 1)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x004265DC, b"\x74", 1)


def ignoreZombies(f):
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x413431, b"\xe9\x7f\x04\x00\x00\x90", 6)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x413431, b"\x0f\x84\x7f\x04\x00\x00", 6)


def overPlant(f):
    # addr = (
    #     int.from_bytes(
    #         data.PVZ_memory.read_bytes(0x40E2C2, 1)
    #         + data.PVZ_memory.read_bytes(0x40E2C1, 1)
    #         + data.PVZ_memory.read_bytes(0x40E2C0, 1)
    #         + data.PVZ_memory.read_bytes(0x40E2BF, 1)
    #     )
    #     + 0x40E2C3
    # )
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x00425634, b"\xeb\x1b\x0f\x1f\x00", 5)
        PVZ_data.PVZ_memory.write_bytes(
            0x0040E3C6, b"\xe9\x94\x00\x00\x00\x0f\x1f\x00", 8
        )
        PVZ_data.PVZ_memory.write_bytes(0x0040FE2D, b"\xe9\x22\x09\x00\x00\x0f\x1f", 7)
        PVZ_data.PVZ_memory.write_bytes(
            0x0042A2D6, b"\xe9\xe2\x00\x00\x00\x0f\x1f\x00", 8
        )
        PVZ_data.PVZ_memory.write_bytes(0x00438E3E, b"\xeb\x34\x66\x90", 4)
        PVZ_data.PVZ_memory.write_bytes(
            0x0040E263, b"\x8b\x5c\x24\x24\xeb\x2a\x0f\x1f\x00", 9
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0087FA00, b"\x0f\x1f\x00\x8b\x4c\x24\x2c\x66\x0f\x1f\x44\x00\x00", 13
        )
        # data.PVZ_memory.write_bytes(
        #     0x00843D50, b"\xeb\x6a\x90\x90\x90\x90\x90\x90\x90", 9
        # )
        PVZ_data.PVZ_memory.write_bytes(0x00410908, b"\xeb\x12\x90\x90\x90", 5)
        # data.PVZ_memory.write_bytes(0x00843DEE, b"\xe9\xe1\xcb\xbc\xff\x0f\x1f\x00", 8)
        # data.PVZ_memory.write_bytes(0x00843E23, b"\xe9\xac\xcb\xbc\xff\x0f\x1f\x00", 8)
        # data.PVZ_memory.write_bytes(0x00843E58, b"\xe9\x77\xcb\xbc\xff\x0f\x1f\x00", 8)
        PVZ_data.PVZ_memory.write_bytes(0x00410958, b"\xeb\x7a\x90\x90", 4)
        PVZ_data.PVZ_memory.write_bytes(0x00410960, b"\xeb\x72", 2)
        PVZ_data.PVZ_memory.write_bytes(0x00410B11, b"\x90\x90", 2)
        PVZ_data.PVZ_memory.write_bytes(0x00410B16, b"\xeb\x47", 2)
        # data.PVZ_memory.write_bytes(0x0084A3EB, b"\xe9\x6a\x3f\xbc\xff\x90", 6)
        PVZ_data.PVZ_memory.write_bytes(0x00410BA2, b"\xeb\x06", 2)
        PVZ_data.PVZ_memory.write_bytes(0x00410967, b"\xeb\x39", 2)
        PVZ_data.PVZ_memory.write_bytes(0x004109A5, b"\xeb\x2d", 2)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x00425634, b"\x83\xf8\xff\x74\x18", 5)
        PVZ_data.PVZ_memory.write_bytes(0x0040FE2D, b"\x85\xc0\x0f\x84\x1f\x09\x00", 7)
        PVZ_data.PVZ_memory.write_bytes(
            0x0040E3C6, b"\x85\xdb\x0f\x84\x91\x00\x00\x00", 8
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0042A2D6, b"\x85\xc0\x0f\x84\xdf\x00\x00\x00", 8
        )
        PVZ_data.PVZ_memory.write_bytes(0x00438E3E, b"\x85\xc0\x74\x32", 4)
        PVZ_data.PVZ_memory.write_bytes(
            0x0040E263, b"\x83\xf9\x03\x8b\x5c\x24\x24\x75\x27", 9
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0087FA00,
            b"\x83\xf9\x02\x8b\x4c\x24\x2c\x0f\x84"
            + calculate_call_address(0x0040E2CD - 0x0087FA00 - 0xD),
            13,
        )
        # data.PVZ_memory.write_bytes(
        #     0x00843D50, b"\x83\xfb\x4c\x0f\x84\xb4\xcb\xbc\xff", 9
        # )
        PVZ_data.PVZ_memory.write_bytes(0x00410908, b"\x83\xfb\x17\x75\x0f", 5)
        # data.PVZ_memory.write_bytes(0x00843DEE, b"\x85\xc0\x0f\x84\xde\xcb\xbc\xff", 8)
        # data.PVZ_memory.write_bytes(0x00843E23, b"\x85\xc0\x0f\x84\xa9\xcb\xbc\xff", 8)
        # data.PVZ_memory.write_bytes(0x00843E58, b"\x85\xc0\x0f\x84\x74\xcb\xbc\xff", 8)
        PVZ_data.PVZ_memory.write_bytes(0x00410958, b"\x85\xc0\x73\x78", 4)
        PVZ_data.PVZ_memory.write_bytes(0x00410960, b"\x75\x72", 2)
        PVZ_data.PVZ_memory.write_bytes(0x00410B11, b"\x74\x05", 2)
        PVZ_data.PVZ_memory.write_bytes(0x00410B16, b"\x75\x47", 2)
        # data.PVZ_memory.write_bytes(0x0084A3EB, b"\x0f\x85\x69\x3f\xbc\xff", 6)
        PVZ_data.PVZ_memory.write_bytes(0x00410BA2, b"\x75\x06", 2)
        PVZ_data.PVZ_memory.write_bytes(0x00410967, b"\x75\x39", 2)
        PVZ_data.PVZ_memory.write_bytes(0x004109A5, b"\x75\x2d", 2)


def column(f):
    if PVZ_data.PVZ_version == 2.1 or PVZ_data.PVZ_version >= 2.2:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x00410ADF, b"\xeb\x0b\x90\x90\x90", 5)
            PVZ_data.PVZ_memory.write_bytes(0x00439035, b"\xeb\x0b\x90\x90\x90", 5)
        else:
            PVZ_data.PVZ_memory.write_bytes(0x00410ADF, b"\xe9\x1c\xbf\x42\x00", 5)
            PVZ_data.PVZ_memory.write_bytes(0x00439035, b"\xe9\xc6\x3b\x40\x00", 5)
    else:
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x00410ADF, b"\xeb\x0b\x90\x90\x90", 5)
            PVZ_data.PVZ_memory.write_bytes(0x00439035, b"\xeb\x0b\x90\x90\x90", 5)
        else:
            PVZ_data.PVZ_memory.write_bytes(0x00410ADF, b"\xeb\x0b\x90\x90\x90", 5)
            PVZ_data.PVZ_memory.write_bytes(0x00439035, b"\xeb\x0b\x90\x90\x90", 5)


newmem_half_court_plant = None


def half_court_plant(f):
    global newmem_half_court_plant
    # [ENABLE]
    # //code from here to '[DISABLE]' will be used to enable the cheat

    # alloc(newmem,2048)
    # label(returnhere)

    # newmem:
    # mov ebx,eax

    # push -1
    # push ebx
    # mov eax,[esp+20]
    # mov esi,eax
    # push edi
    # push ebp
    # call 0040D120

    # pushad
    # mov EAX,[006A9EC0]
    # mov EAX,[EAX+768]
    # mov EAX,[EAX+554c]
    # cmp EAX,#0
    # je row_5
    # cmp EAX,#1
    # je row_5
    # cmp EAX,#10
    # je row_5
    # cmp EAX,#13
    # je row_5
    # cmp EAX,#15
    # je row_5
    # cmp EAX,#16
    # je row_5
    # cmp EAX,#18
    # je row_5
    # cmp EAX,#19
    # je row_5
    # cmp EAX,#21
    # je row_5
    # cmp EAX,#24
    # je row_5
    # cmp EAX,#2
    # je row_6
    # cmp EAX,#11
    # je row_6
    # cmp EAX,#3
    # je row_6
    # cmp EAX,#12
    # je row_6
    # cmp EAX,#14
    # je row_6
    # cmp EAX,#17
    # je row_6
    # cmp EAX,#20
    # je row_6
    # cmp EAX,#22
    # je row_6
    # cmp EAX,#23
    # je row_6
    # cmp EAX,#25
    # je row_6
    # cmp EAX,#26
    # je row_6
    # row_5:
    # cmp esi,0
    # je row_5_0
    # cmp esi,1
    # je row_5_1
    # cmp esi,2
    # je end
    # cmp esi,3
    # je row_5_3
    # cmp esi,4
    # je row_5_4
    # jmp end
    # row_6:
    # cmp esi,0
    # je row_6_0
    # cmp esi,1
    # je row_6_1
    # cmp esi,2
    # je row_6_2
    # cmp esi,3
    # je row_6_3
    # cmp esi,4
    # je row_6_4
    # cmp esi,5
    # je row_6_5
    # jmp end

    # row_5_0:
    # push -1
    # push ebx
    # mov eax,1
    # push edi
    # push ebp
    # call 0040D120
    # jmp end

    # row_5_1:
    # push -1
    # push ebx
    # mov eax,0
    # push edi
    # push ebp
    # call 0040D120
    # jmp end

    # row_5_3:
    # push -1
    # push ebx
    # mov eax,4
    # push edi
    # push ebp
    # call 0040D120
    # jmp end

    # row_5_4:
    # push -1
    # push ebx
    # mov eax,3
    # push edi
    # push ebp
    # call 0040D120
    # jmp end

    # row_6_0:
    # push -1
    # push ebx
    # mov eax,1
    # push edi
    # push ebp
    # call 0040D120
    # push -1
    # push ebx
    # mov eax,2
    # push edi
    # push ebp
    # call 0040D120
    # jmp end

    # row_6_1:
    # push -1
    # push ebx
    # mov eax,0
    # push edi
    # push ebp
    # call 0040D120
    # push -1
    # push ebx
    # mov eax,2
    # push edi
    # push ebp
    # call 0040D120
    # jmp end

    # row_6_2:
    # push -1
    # push ebx
    # mov eax,0
    # push edi
    # push ebp
    # call 0040D120
    # push -1
    # push ebx
    # mov eax,1
    # push edi
    # push ebp
    # call 0040D120
    # jmp end

    # row_6_3:
    # push -1
    # push ebx
    # mov eax,4
    # push edi
    # push ebp
    # call 0040D120
    # push -1
    # push ebx
    # mov eax,5
    # push edi
    # push ebp
    # call 0040D120
    # jmp end

    # row_6_4:
    # push -1
    # push ebx
    # mov eax,3
    # push edi
    # push ebp
    # call 0040D120
    # push -1
    # push ebx
    # mov eax,5
    # push edi
    # push ebp
    # call 0040D120
    # jmp end

    # row_6_5:
    # push -1
    # push ebx
    # mov eax,3
    # push edi
    # push ebp
    # call 0040D120
    # push -1
    # push ebx
    # mov eax,4
    # push edi
    # push ebp
    # call 0040D120
    # jmp end

    # end:
    # popad
    # jmp returnhere

    # 410A94:
    # jmp newmem
    # nop 8
    # returnhere:

    # [DISABLE]
    # 410A94:
    # push edx
    # push eax
    # mov eax,[esp+20]
    # push edi
    # push ebp
    # call 0040D120
    if f:
        newmem_half_court_plant = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 2048
        )
        shellcode = asm.Asm(newmem_half_court_plant)
        shellcode.mov_exx_eyy(asm.EBX, asm.EAX)
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.EAX, asm.ESP, 0x20)
        shellcode.mov_exx_eyy(asm.ESI, asm.EAX)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.pushad()
        shellcode.mov_exx_dword_ptr(asm.EAX, 0x006A9EC0)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x768)
        shellcode.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x554C)
        shellcode.cmp_exx_dword(asm.EAX, 0)
        shellcode.je_label("row_5")
        shellcode.cmp_exx_dword(asm.EAX, 1)
        shellcode.je_label("row_5")
        shellcode.cmp_exx_dword(asm.EAX, 10)
        shellcode.je_label("row_5")
        shellcode.cmp_exx_dword(asm.EAX, 13)
        shellcode.je_label("row_5")
        shellcode.cmp_exx_dword(asm.EAX, 15)
        shellcode.je_label("row_5")
        shellcode.cmp_exx_dword(asm.EAX, 16)
        shellcode.je_label("row_5")
        shellcode.cmp_exx_dword(asm.EAX, 18)
        shellcode.je_label("row_5")
        shellcode.cmp_exx_dword(asm.EAX, 19)
        shellcode.je_label("row_5")
        shellcode.cmp_exx_dword(asm.EAX, 21)
        shellcode.je_label("row_5")
        shellcode.cmp_exx_dword(asm.EAX, 24)
        shellcode.je_label("row_5")
        shellcode.cmp_exx_dword(asm.EAX, 2)
        shellcode.je_label("row_6")
        shellcode.cmp_exx_dword(asm.EAX, 11)
        shellcode.je_label("row_6")
        shellcode.cmp_exx_dword(asm.EAX, 3)
        shellcode.je_label("row_6")
        shellcode.cmp_exx_dword(asm.EAX, 12)
        shellcode.je_label("row_6")
        shellcode.cmp_exx_dword(asm.EAX, 14)
        shellcode.je_label("row_6")
        shellcode.cmp_exx_dword(asm.EAX, 17)
        shellcode.je_label("row_6")
        shellcode.cmp_exx_dword(asm.EAX, 20)
        shellcode.je_label("row_6")
        shellcode.cmp_exx_dword(asm.EAX, 22)
        shellcode.je_label("row_6")
        shellcode.cmp_exx_dword(asm.EAX, 23)
        shellcode.je_label("row_6")
        shellcode.cmp_exx_dword(asm.EAX, 25)
        shellcode.je_label("row_6")
        shellcode.cmp_exx_dword(asm.EAX, 26)
        shellcode.je_label("row_6")
        shellcode.create_label("row_5")
        shellcode.cmp_exx_dword(asm.ESI, 0)
        shellcode.je_label("row_5_0")
        shellcode.cmp_exx_dword(asm.ESI, 1)
        shellcode.je_label("row_5_1")
        shellcode.cmp_exx_dword(asm.ESI, 2)
        shellcode.je_label("end")
        shellcode.cmp_exx_dword(asm.ESI, 3)
        shellcode.je_label("row_5_3")
        shellcode.cmp_exx_dword(asm.ESI, 4)
        shellcode.je_label("row_5_4")
        shellcode.jmp_label("end")
        shellcode.create_label("row_6")
        shellcode.cmp_exx_dword(asm.ESI, 0)
        shellcode.je_label("row_6_0")
        shellcode.cmp_exx_dword(asm.ESI, 1)
        shellcode.je_label("row_6_1")
        shellcode.cmp_exx_dword(asm.ESI, 2)
        shellcode.je_label("row_6_2")
        shellcode.cmp_exx_dword(asm.ESI, 3)
        shellcode.je_label("row_6_3")
        shellcode.cmp_exx_dword(asm.ESI, 4)
        shellcode.je_label("row_6_4")
        shellcode.cmp_exx_dword(asm.ESI, 5)
        shellcode.je_label("row_6_5")
        shellcode.jmp_label("end")
        shellcode.create_label("row_5_0")
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 1)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.jmp_label("end")
        shellcode.create_label("row_5_1")
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 0)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.jmp_label("end")
        shellcode.create_label("row_5_3")
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 4)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.jmp_label("end")
        shellcode.create_label("row_5_4")
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 3)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.jmp_label("end")
        shellcode.create_label("row_6_0")
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 1)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 2)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.jmp_label("end")
        shellcode.create_label("row_6_1")
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 0)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 2)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.jmp_label("end")
        shellcode.create_label("row_6_2")
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 0)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 1)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.jmp_label("end")
        shellcode.create_label("row_6_3")
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 4)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 5)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.jmp_label("end")
        shellcode.create_label("row_6_4")
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 3)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 5)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.jmp_label("end")
        shellcode.create_label("row_6_5")
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 3)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.push_dword(-1)
        shellcode.push_exx(asm.EBX)
        shellcode.mov_exx(asm.EAX, 4)
        shellcode.push_exx(asm.EDI)
        shellcode.push_exx(asm.EBP)
        shellcode.call(0x0040D120)
        shellcode.jmp_label("end")
        shellcode.create_label("end")
        shellcode.popad()
        shellcode.jmp(0x00410AA1)
        PVZ_data.PVZ_memory.write_bytes(
            newmem_half_court_plant,
            bytes(shellcode.code[: shellcode.index]),
            shellcode.index,
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x410A94,
            b"\xe9"
            + calculate_call_address(newmem_half_court_plant - 0x410A99)
            + b"\x90\x90\x90\x90\x90\x90\x90\x90",
            13,
        )
    else:
        PVZ_data.PVZ_memory.write_bytes(
            0x410A94, b"\x52\x50\x8b\x44\x24\x20\x57\x55\xe8\x7f\xc6\xff\xff", 13
        )
        pymem.memory.free_memory(
            PVZ_data.PVZ_memory.process_handle, newmem_half_court_plant
        )


newmem_noSun = None


def noSun(f):
    global newmem_noSun
    # [ENABLE]
    # //code from here to '[DISABLE]' will be used to enable the cheat
    # alloc(newmem,2048)
    # label(returnhere)
    # label(originalcode)
    # label(exit)
    #
    # newmem: //this is allocated memory, you have read,write,execute access
    # //place your code here
    # cmp [esp+c],4
    # je ns
    # cmp [esp+c],5
    # je ns
    # cmp [esp+c],6
    # je ns
    # originalcode:
    # push ebp
    # mov ebp,esp
    # and esp,-08
    #
    # exit:
    # jmp returnhere
    #
    # ns:
    # cmp byte [00743F62],0
    # mov byte [00743F62],0
    # jne originalcode
    # ret 10
    #
    #
    # "PlantsVsZombies.exe"+CB10:
    # jmp newmem
    # nop
    # returnhere:
    #
    #
    #
    #
    # [DISABLE]
    # //code from here till the end of the code will be used to disable the cheat
    # dealloc(newmem)
    # "PlantsVsZombies.exe"+CB10:
    # db 55 8B EC 83 E4 F8
    # //push ebp
    # //mov ebp,esp
    # //and esp,-08
    if f:
        newmem_noSun = pymem.memory.allocate_memory(
            PVZ_data.PVZ_memory.process_handle, 128
        )
        shellcode = asm.Asm(newmem_noSun)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESP, 0xC, 4)
        shellcode.je_offset(0x21)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESP, 0xC, 5)
        shellcode.je_offset(0x16)
        shellcode.cmp_dword_ptr_exx_add_byte_byte(asm.ESP, 0xC, 6)
        shellcode.je_offset(0x0B)
        shellcode.push_exx(asm.EBP)
        shellcode.mov_exx_eyy(asm.EBP, asm.ESP)
        shellcode.and_exx_byte(asm.ESP, 0xF8)
        shellcode.jmp(0x0040CB16)
        shellcode.cmp_byte_ptr_address_byte(0x00743F62, 0)
        shellcode.mov_byte_ptr_address_byte(0x00743F62, 0)
        shellcode.jne_short_offset(0xE5)
        shellcode.ret_word(0x10)

        PVZ_data.PVZ_memory.write_bytes(
            newmem_noSun, bytes(shellcode.code[: shellcode.index]), shellcode.index
        )
        PVZ_data.PVZ_memory.write_bytes(
            0x0040CB10,
            b"\xe9" + calculate_call_address(newmem_noSun - 0x0040CB15) + b"\x90",
            6,
        )
        PVZ_data.PVZ_memory.write_bytes(0x008A2E4B, b"\x90\x90\x90", 3)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x0040CB10, b"\x55\x8b\xec\x83\xe4\xf8", 6)
        pymem.memory.free_memory(PVZ_data.PVZ_memory.process_handle, newmem_noSun)


def num_slot(f):
    if f:
        slotKey(
            {
                "1": 2,
                "2": 3,
                "3": 4,
                "4": 5,
                "5": 6,
                "6": 7,
                "7": 8,
                "8": 9,
                "9": 10,
                "10": 1,
                "11": 27,
                "12": 33,
                "13": 15,
                "14": 28,
                "shovel": 36,
                "hp": 13,
                "top": 13,
                "pause": 36,
                "zombie_hp": 34,
                "plant_hp": 32,
                "speed": 12,
                "bag": 24,
            }
        )
    else:
        slotKey(False)


def vase_gargantuar_fix(f):
    if PVZ_data.PVZ_version == 2.1 or PVZ_data.PVZ_version >= 2.2:
        # [ENABLE]
        # 0052F41F:
        # db D9 EE 51 D9 1C 24
        # 005272BB:
        # db D9 05 98 97 67 00
        # [DISABLE]
        # 0052F41F:
        # db E9 8C 51 31 00 90
        # 005272BB:
        # db E9 10 D5 31 00 90
        if f:
            PVZ_data.PVZ_memory.write_bytes(0x0052F41F, b"\xd9\xee\x51\xd9\x1c\x24", 6)
            PVZ_data.PVZ_memory.write_bytes(0x005272BB, b"\xd9\x05\x98\x97\x67\x00", 6)
        else:
            PVZ_data.PVZ_memory.write_bytes(0x0052F41F, b"\xe9\x8c\x51\x31\x00\x90", 6)
            PVZ_data.PVZ_memory.write_bytes(0x005272BB, b"\xe9\x10\xd5\x31\x00\x90", 6)


def fix_nut_gargantuar(f):
    # [ENABLE]
    # 008A60E0:
    # nop
    # nop
    # nop
    # nop
    # nop
    # nop
    # nop

    # [DISABLE]
    # 008A60E0:
    # push 01
    # call 00530E30
    if f:
        PVZ_data.PVZ_memory.write_bytes(0x008A60E0, b"\x90\x90\x90\x90\x90\x90\x90", 7)
    else:
        PVZ_data.PVZ_memory.write_bytes(0x008A60E0, b"\x6a\x01\xe8\x49\xad\xc8\xff", 7)
