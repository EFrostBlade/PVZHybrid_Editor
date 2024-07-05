import wmi
import psutil
import pymem
import pymem.ressources.kernel32
import pymem.ressources.structure
import pymem.thread
import pymem.memory
import time
import shutil
import sys
import os
import PVZ_data as data
import PVZ_asm as asm
import ctypes


def calculate_call_address(ctypes_obj):
    """S
    计算函数调用地址
    """
    c_uint_obj = ctypes.c_uint(ctypes_obj)
    return ctypes.string_at(ctypes.addressof(c_uint_obj), ctypes.sizeof(c_uint_obj))


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
    newmem = pymem.memory.allocate_memory(process.process_handle, 256)
    print("newmem", hex(newmem))
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
    process.write_bytes(
        newmem, bytes(shellcode.code[: shellcode.index]), shellcode.index
    )
    process.write_bytes(
        0x004672B5,
        b"\xe9" + calculate_call_address(newmem - 0x004672BA) + b"\x90",
        6,
    )


def CrossLineEnemySearch():
    newmem = pymem.memory.allocate_memory(process.process_handle, 64)
    shellcode = asm.Asm(newmem)
    shellcode.cmp_exx_byte(asm.EAX, 0)
    shellcode.je(0x004676C8)
    shellcode.cmp_exx_byte(asm.EAX, 0x2A)
    shellcode.jne(0x0046769D)
    shellcode.jmp(0x0046768A)
    process.write_bytes(
        newmem, bytes(shellcode.code[: shellcode.index]), shellcode.index
    )
    process.write_bytes(
        0x00467685,
        b"\xe9" + calculate_call_address(newmem - 0x0046768A),
        5,
    )


def searchEnemy():
    newmem = pymem.memory.allocate_memory(process.process_handle, 256)
    shellcode = asm.Asm(newmem)
    shellcode.cmp_exx_byte(asm.EDX, 0)
    shellcode.je(0x00468152)
    shellcode.cmp_exx_byte(asm.EDX, 16)
    shellcode.jne(0x004680CC)
    shellcode.jmp(0x004680AB)
    process.write_bytes(
        newmem, bytes(shellcode.code[: shellcode.index]), shellcode.index
    )
    process.write_bytes(
        0x004680A6,
        b"\xe9" + calculate_call_address(newmem - 0x004680AB),
        5,
    )


def resource_path(relative_path):
    """获取资源的绝对路径，适用于开发环境和PyInstaller环境"""
    try:
        # PyInstaller创建的临时文件夹的路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def copy_and_merge(src, dst):
    if os.path.isdir(src):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            copy_and_merge(s, d)
    else:
        shutil.copy2(src, dst)


def on_process_created(event):
    global process
    if event.Caption == "PlantsVsZombies.exe":
        print("PlantsVsZombies.exe started", "PID:", event.ProcessID)

        # 获取目标进程
        proc = psutil.Process(event.ProcessID)  # 请将12345替换为你的目标进程的PID

        # 暂停进程
        proc.suspend()
        print(f"Process {proc.pid} is suspended.")
        process = pymem.Pymem(event.ProcessID)
        print(process.process_base)
        now_reanim_num = process.read_int(0x47377E)
        process.write_int(0x47377E, now_reanim_num + 1)
        process.write_int(0x007A0060 + (now_reanim_num - 1 - 142) * 12, now_reanim_num)
        newmem_reanim_path_address = process.allocate(0x128)
        process.write_int(
            0x007A0060 + (now_reanim_num - 1 - 142) * 12 + 4, newmem_reanim_path_address
        )
        game_path = proc.exe()
        print(game_path)
        source_dir = resource_path(r"./res/gameres")
        # 获取game_path的目录部分
        dir_path = os.path.dirname(game_path)
        # 复制并合并文件和文件夹
        copy_and_merge(source_dir, dir_path)

        file_path = r"new\PlatoonCannon.reanim"
        file_bytes = bytes(file_path, "utf-8")
        file_bytes += b"\x00\x00"
        process.write_bytes(newmem_reanim_path_address, file_bytes, len(file_bytes))
        process.write_int(0x007A2008, 220)
        # process.write_bytes(0x004814E4, b"\x90\x90\x90\x90\x90\x90", 6)
        reanim_adderess = process.read_int(0x006A9EE8)
        if reanim_adderess != 0:
            print(hex(reanim_adderess))
            print(hex(reanim_adderess + (now_reanim_num) * 16))
            process.write_int(reanim_adderess + (now_reanim_num) * 16, 0)
            process.write_int(reanim_adderess + (now_reanim_num) * 16 + 4, 0)
            process.write_int(reanim_adderess + (now_reanim_num) * 16 + 8, 0x4140000)
            process.write_int(reanim_adderess + (now_reanim_num) * 16 + 12, 0)
        PlatoonCannonBullet()
        CrossLineEnemySearch()
        searchEnemy()
        process.write_bytes(0x4814E4, b"\x90\x90\x90\x90\x90\x90", 6)
        # 恢复进程
        proc.resume()
        print(f"Process {proc.pid} is resumed.")


print("请先打开本软件，再运行游戏")
c = wmi.WMI()
process_watcher = c.Win32_Process.watch_for("creation")
while True:
    try:
        process_created = process_watcher()
        on_process_created(process_created)
    except wmi.x_wmi_timed_out:
        pass  # Timeout occurred, just continue the loop
