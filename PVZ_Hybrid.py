import ctypes
import PVZ_data as data
import pymem.ressources.kernel32
import pymem.ressources.structure
import pymem.thread
import pymem.memory
from threading import Thread, Event
import time
import PVZ_asm as asm

column1addr=None
column2addr=None
newmem_shovelpro=None
newmem_spoils=None
newmem_spoils2=None

def calculate_call_address(ctypes_obj):
    """S
    计算函数调用地址
    """
    c_uint_obj = ctypes.c_uint(ctypes_obj)
    return ctypes.string_at(ctypes.addressof(c_uint_obj), ctypes.sizeof(c_uint_obj))

def getMap():
    try:
        map=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x554c)
        if(map==0 or map==1 or map==10 or map==13 or map==15 or map==16 or map==18 or map==19):
            return 5
        elif(map==2 or map==11 or map==3 or map==12 or map==14 or map==17):
            return 6
        else:
            return False
    except:
        return False

def getState():
    try:
        game_state=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x7fc)
        return game_state  #1主菜单 2选局内  5帮助  7关卡选择  
    except:
        return False
def backGround(f):
    if f:
        data.PVZ_memory.write_bytes(0x0054EBEF,b'\xc3',1)
    else:
        data.PVZ_memory.write_bytes(0x0054EBEF,b'\x57',1)

def overPlant(f): 
    addr=int.from_bytes(data.PVZ_memory.read_bytes(0x40e2c2,1)+data.PVZ_memory.read_bytes(0x40e2c1,1)+data.PVZ_memory.read_bytes(0x40e2c0,1)+data.PVZ_memory.read_bytes(0x40e2bf,1))+0x40e2c3
    if f:
        data.PVZ_memory.write_bytes(0x00425634,b'\xeb\x1b\x0f\x1f\x00',5)
        data.PVZ_memory.write_bytes(0x0040FE2D,b'\xe9\x22\x09\x00\x00\x0f\x1f',7)
        data.PVZ_memory.write_bytes(0x0040e3c6,b'\xe9\x94\x00\x00\x00\x0f\x1f\x00',8)
        data.PVZ_memory.write_bytes(0x0042a2d6,b'\xe9\xe2\x00\x00\x00\x0f\x1f\x00',8)
        data.PVZ_memory.write_bytes(0x00438e3e,b'\xeb\x34\x66\x90',4)
        data.PVZ_memory.write_bytes(0x0040e263,b'\x8b\x5c\x24\x24\xeb\x2a\x0f\x1f\x00',9)
        data.PVZ_memory.write_bytes(addr,b'\x0f\x1f\x00\x8b\x4c\x24\x2c\x66\x0f\x1f\x44\x00\x00',13)
    else:
        data.PVZ_memory.write_bytes(0x00425634,b'\x83\xf8\xff\x74\x18',5)
        data.PVZ_memory.write_bytes(0x0040FE2D,b'\x85\xc0\x0f\x84\x1f\x09\x00',7)
        data.PVZ_memory.write_bytes(0x0040e3c6,b'\x85\xdb\x0f\x84\x91\x00\x00\x00',8)
        data.PVZ_memory.write_bytes(0x0042a2d6,b'\x85\xc0\x0f\x84\xdf\x00\x00\x00',8)
        data.PVZ_memory.write_bytes(0x00438e3e,b'\x85\xc0\x74\x32',4)
        data.PVZ_memory.write_bytes(0x0040e263,b'\x83\xf9\x03\x8b\x5c\x24\x24\x75\x27',9)
        data.PVZ_memory.write_bytes(addr,b'\x83\xf9\x02\x8b\x4c\x24\x2c\x0f\x84'+calculate_call_address(0x0040e2cd-addr-0xd),13)

def getSun():
    sunAddr=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x5560
    sunNow = data.PVZ_memory.read_int(sunAddr) 
    return sunNow

def addSun(sunIncrement):
    sunAddr=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x5560
    sunNow = data.PVZ_memory.read_int(sunAddr) 
    data.PVZ_memory.write_int(sunAddr,sunNow+int(sunIncrement))

def setSun(sun):
    sunAddr=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x5560
    data.PVZ_memory.write_int(sunAddr,int(sun))

def upperLimit(f):
    if f:
        data.PVZ_memory.write_bytes(0x00430A23,b'\xeb',1)
        data.PVZ_memory.write_bytes(0x00430A78,b'\xeb',1)
        data.PVZ_memory.write_bytes(0x0048CAB0,b'\xeb',1)
    else:
        data.PVZ_memory.write_bytes(0x00430A23,b'\x7e',1)
        data.PVZ_memory.write_bytes(0x00430A78,b'\x7e',1)
        data.PVZ_memory.write_bytes(0x0048CAB0,b'\x7e',1)

def pausePro(f):
    if f:
        data.PVZ_memory.write_bytes(0x415df0,b'\x0f\x1f\x80\x00\x00\x00\x00\x66\x90',9)
    else:
        data.PVZ_memory.write_bytes(0x415df0,b'\x80\xbd\x64\x01\x00\x00\x00\x74\x35',9)

def ignoreSun(f):
    if f:
        data.PVZ_memory.write_bytes(0x0041ba70,b'\x90\x90\x90\x90\x90\x90',6)
        data.PVZ_memory.write_bytes(0x0048881B,b'\xe9\x97\x01\x00\x00\x0f\x1f\x00',8)
        data.PVZ_memory.write_bytes(0x0048847f,b'\xeb',1)
        data.PVZ_memory.write_bytes(0x0040f8a2,b'\xeb',1)
        data.PVZ_memory.write_bytes(0x00488565,b'\xeb\x0e\x90\x90',4)
    else:
        data.PVZ_memory.write_bytes(0x0041ba70,b'\x39\xc3\x7f\x0c\x29\xde',6)
        data.PVZ_memory.write_bytes(0x0048881B,b'\x84\xc0\x0f\x85\x94\x01\x00\x00',8)
        data.PVZ_memory.write_bytes(0x0048847f,b'\x75',1)
        data.PVZ_memory.write_bytes(0x0040f8a2,b'\x75',1)
        data.PVZ_memory.write_bytes(0x00488565,b'\x84\xc0\x75\x0c',4)

def cancelCd(f):
    if f:
        data.PVZ_memory.write_bytes(0x487293,b'\x3b\x47\x28\x90\x90',5)
    else:
        data.PVZ_memory.write_bytes(0x487296,b'\x7e\x14',2)

def killAllZombies():
    zomNum=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xa0)
    i=0
    j=0
    while i<zomNum:
        zomAddresss=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x90)+0x15c*j
        zomExist=data.PVZ_memory.read_bytes(zomAddresss+0xec,1)
        if(zomExist==b'\x00'):
            data.PVZ_memory.write_int(zomAddresss+0x28,3)
            i=i+1
        j=j+1

def autoCollect(f):
    if f:
        data.PVZ_memory.write_bytes(0x43158B,b'\x80\x7B\x50\x00\xEB\x08',6)
    else:
        data.PVZ_memory.write_bytes(0x43158B,b'\x80\x7B\x50\x00\x75\x08',6)

def changeSlot(n,type):        
    slotAddr=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x144
    data.PVZ_memory.write_int(data.PVZ_memory.read_int(slotAddr)+0x5c+0x50*(n-1),type)

def win():
    winAddr=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x55fc
    data.PVZ_memory.write_int(winAddr,1)

def advacedPause(f):
    if f:
        data.PVZ_memory.write_bytes(0x415df0,b'\x0f\x1f\x80\x00\x00\x00\x00\x66\x90',9)
    else:
        data.PVZ_memory.write_bytes(0x415df0,b'\x80\xbd\x64\x01\x00\x00\x00\x74\x35',9) 

def column(f):
    global column1addr
    global column2addr
    if f:
        column1addr=data.PVZ_memory.read_bytes(0x00410adf,5)
        column2addr=data.PVZ_memory.read_bytes(0x00439035,5)
        data.PVZ_memory.write_bytes(0x00410adf,b'\xeb\x0b\x90\x90\x90',5)
        data.PVZ_memory.write_bytes(0x00439035,b'\xeb\x0b\x90\x90\x90',5)
    else:
        data.PVZ_memory.write_bytes(0x00410adf,column1addr,5)
        data.PVZ_memory.write_bytes(0x00439035,column2addr,5)

def unlock():
    data.PVZ_memory.write_bytes(0x00453b20,b'\x56\x8b\xb7\x2c\x08\x00\x00',7)

def shovelpro(f):
    global newmem_shovelpro
    addr=int.from_bytes(data.PVZ_memory.read_bytes(0x411141,1)+data.PVZ_memory.read_bytes(0x411140,1)+data.PVZ_memory.read_bytes(0x41113f,1)+data.PVZ_memory.read_bytes(0x41113e,1))+0x411142+0x3
    print(hex(addr))
    if f:
        data.PVZ_memory.write_bytes(addr,b'\x90\x90\x90\xeb\x77\x90\x90\x90\x90',9)
        newmem_shovelpro=pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 100) 
        print(newmem_shovelpro)
        byte_data=(
                b'\x60\x8b\x45\x24\x8b\x7d\x04\xba\xff\xff\xff\xff\xe8'
                +calculate_call_address(0x0041dae0-newmem_shovelpro-0x11)+
                b'\x01\x85\x2c\x01\x00\x00\x61\x83\xbd\x2c\x01\x00\x00\x32\x7c\x1d\x83\xad\x2c\x01\x00\x00\x32'
                b'\x60\x8b\x4d\x04\x6a\x02\x6a\x06\xff\x75\x0c\xff\x75\x08\xe8'
                +calculate_call_address(0x0040cb10-newmem_shovelpro-0x3b)+
                b'\x61\xeb\xda\x83\xbd\x2c\x01\x00\x00\x19\x7c\x1d\x83\xad\x2c\x01\x00\x00\x19\x60\x8b\x4d\x04'
                b'\x6a\x02\x6a\x04\xff\x75\x0c\xff\x75\x08\xe8'
                +calculate_call_address(0x0040cb10-newmem_shovelpro-0x61)+
                b'\x61\xeb\xb4\x83\xbd\x2c\x01\x00\x00\x0f\x7c\x1d\x83\xad\x2c\x01\x00\x00\x0f\x60\x8b\x4d\x04'
                b'\x6a\x02\x6a\x05\xff\x75\x0c\xff\x75\x08\xe8'
                +calculate_call_address(0x0040cb10-newmem_shovelpro-0x87)+
                b'\x61\xeb\x8e\x01\x9f\x9c\x57\x00\x00\xe9'
                +calculate_call_address(0x004111de-newmem_shovelpro-0x95)
        )
        data.PVZ_memory.write_bytes(newmem_shovelpro,byte_data,149)
        data.PVZ_memory.write_bytes(0x004111d8,b'\xe9'+calculate_call_address(newmem_shovelpro-0x004111dd)+b'\x90',6)
    else:
        data.PVZ_memory.write_bytes(addr,b'\x83\xf8\x36\x0f\x84\x64\x00\x00\x00',9)
        data.PVZ_memory.write_bytes(0x004111d8,b'\x01\x9f\x9c\x57\x00\x00',6)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_shovelpro)

def ignoreZombies(f):
    if f:
        data.PVZ_memory.write_bytes(0x413431,b'\xe9\x7f\x04\x00\x00\x90',6)
    else:        
        data.PVZ_memory.write_bytes(0x413431,b'\x0f\x84\x7f\x04\x00\x00',6)

def pauseSpawn(f):
    if f:
        data.PVZ_memory.write_bytes(0x004265DC,b'\xeb',1)
    else:
        data.PVZ_memory.write_bytes(0x004265DC,b'\x74',1)


def changeGameSpeed(s):
    FrameDurationAddr=data.PVZ_memory.read_int(data.baseAddress)+0x454
    if(s==0):
        data.PVZ_memory.write_int(FrameDurationAddr,10)
        data.PVZ_memory.write_bytes(0x6A9EAA,b'\x01',1)
        data.PVZ_memory.write_bytes(0x6A9EAB,b'\x00',1)
    elif(s==1):
        data.PVZ_memory.write_int(FrameDurationAddr,20)
        data.PVZ_memory.write_bytes(0x6A9EAA,b'\x00',1)
        data.PVZ_memory.write_bytes(0x6A9EAB,b'\x00',1)
    elif(s==2):
        data.PVZ_memory.write_int(FrameDurationAddr,10)
        data.PVZ_memory.write_bytes(0x6A9EAA,b'\x00',1)
        data.PVZ_memory.write_bytes(0x6A9EAB,b'\x00',1)
    elif(s==3):
        data.PVZ_memory.write_int(FrameDurationAddr,5)
        data.PVZ_memory.write_bytes(0x6A9EAA,b'\x00',1)
        data.PVZ_memory.write_bytes(0x6A9EAB,b'\x00',1)
    elif(s==4):
        data.PVZ_memory.write_int(FrameDurationAddr,2)
        data.PVZ_memory.write_bytes(0x6A9EAA,b'\x00',1)
        data.PVZ_memory.write_bytes(0x6A9EAB,b'\x00',1)
    elif(s==5):
        data.PVZ_memory.write_int(FrameDurationAddr,1)
        data.PVZ_memory.write_bytes(0x6A9EAA,b'\x00',1)
        data.PVZ_memory.write_bytes(0x6A9EAB,b'\x00',1)
    elif(s==6):
        data.PVZ_memory.write_int(FrameDurationAddr,10)
        data.PVZ_memory.write_bytes(0x6A9EAA,b'\x00',1)
        data.PVZ_memory.write_bytes(0x6A9EAB,b'\x01',1)

def putLadder(row,col):
    class ladder:
        def __init__(self,row,col):
            self.row=row
            self.col=col   

        def creat_asm(self,startAddress):
            ladder_asm=asm.Asm(startAddress)
            ladder_asm.mov_exx_dword_ptr(asm.EAX, 0x006a9ec0)
            ladder_asm.mov_exx_dword_ptr_eyy_add_dword(asm.EAX,asm.EAX, 0x768)
            ladder_asm.mov_exx(asm.EDI, self.row)
            ladder_asm.push_byte(self.col)
            ladder_asm.call(0x00408f40)
            return ladder_asm

    asm.runThread(ladder(row,col))
    
def putZombie(row,col,type):
    class zombiePut:
        def __init__(self,row,col,type):
            self.row=row
            self.col=col  
            self.type=type

        def creat_asm(self,startAddress):
            zombiePut_asm=asm.Asm(startAddress)
            zombiePut_asm.push_byte(self.col)
            zombiePut_asm.push_byte(self.type)
            zombiePut_asm.mov_exx(asm.EAX, self.row)
            zombiePut_asm.mov_exx_dword_ptr(asm.ECX, 0x006a9ec0)
            zombiePut_asm.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
            zombiePut_asm.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x160)
            zombiePut_asm.call(0x0042a0f0)
            return zombiePut_asm
        
    asm.runThread(zombiePut(row,col,type))
            
def putBoss(row,col,type):
    class bossPut:
        def __init__(self,row,col,type):
            self.row=row
            self.col=col  
            self.type=type

        def creat_asm(self,startAddress):
            bossPut_asm=asm.Asm(startAddress)
            bossPut_asm.mov_exx_dword_ptr(asm.EAX, 0x006a9ec0)
            bossPut_asm.mov_exx_dword_ptr_eyy_add_dword(asm.EAX,asm.EAX,  0x768)
            bossPut_asm.push_byte(0)
            bossPut_asm.push_byte(25)
            bossPut_asm.call(0x0040ddc0)
            return bossPut_asm
        
    asm.runThread(bossPut(row,col,type))
            
def putPlant(row,col,type):
    class plautPut:
        def __init__(self,row,col,type):
            self.row=row
            self.col=col  
            self.type=type

        def creat_asm(self,startAddress):
            plantPut_asm=asm.Asm(startAddress)
            plantPut_asm.push_byte(255)
            plantPut_asm.push_byte(self.type)
            plantPut_asm.mov_exx(asm.EAX, self.row)
            plantPut_asm.push_byte(self.col)
            plantPut_asm.mov_exx_dword_ptr(asm.EBP, 0x006a9ec0)
            plantPut_asm.mov_exx_dword_ptr_eyy_add_dword(asm.EBP,asm.EBP, 0x768)
            plantPut_asm.push_exx(asm.EBP)
            plantPut_asm.call(0x0040d120)
            return plantPut_asm
        
    asm.runThread(plautPut(row,col,type))

def selectCard(type):
    class cardSelect:
        def __init__(self,type):
            self.type=type
        
        def creat_asm(self,startAddress):
            cardSelect_asm=asm.Asm(startAddress)
            cardSelect_asm.mov_exx_dword_ptr(asm.EAX,0x006A9EC0)
            cardSelect_asm.mov_exx_dword_ptr_eyy_add_dword(asm.ESI,asm.EAX,0x00000774)
            cardSelect_asm.mov_exx(asm.EBX,self.type)
            cardSelect_asm.imul_exx_eyy_byte(asm.EDX,asm.EBX,0xf)
            cardSelect_asm.lea_exx_byte_dword(asm.EAX,0x96,0xa4)
            cardSelect_asm.push_exx(asm.EAX)
            cardSelect_asm.mov_exx_eyy(asm.EAX,asm.ESI)
            cardSelect_asm.call(0x00486030)
            return cardSelect_asm
    
    asm.runThread(cardSelect(type))

def deselectCard(type):
    class cardDeselect:
        def __init__(self,type):
            self.type=type
        
        def creat_asm(self,startAddress):
            cardDeselect_asm=asm.Asm(startAddress)
            cardDeselect_asm.mov_exx_dword_ptr(asm.EAX,0x006A9EC0)
            cardDeselect_asm.mov_exx_dword_ptr_eyy_add_dword(asm.ESI,asm.EAX,0x00000774)
            cardDeselect_asm.mov_exx(asm.EBX,self.type)
            cardDeselect_asm.imul_exx_eyy_byte(asm.EDX,asm.EBX,0xf)
            cardDeselect_asm.lea_exx_byte_dword(asm.EAX,0x96,0xa4)
            cardDeselect_asm.push_exx(asm.EAX)
            cardDeselect_asm.mov_exx_eyy(asm.EAX,asm.ESI)
            cardDeselect_asm.call(0x00485E90)
            return cardDeselect_asm
    
    asm.runThread(cardDeselect(type))

def defeat():
    class Defeat:
        def __init__(self) -> None:
            pass
        
        def creat_asm(self,startAddress):
            Defeat_asm=asm.Asm(startAddress)
            Defeat_asm.mov_exx_dword_ptr(asm.EAX,0x006A9EC0)
            Defeat_asm.mov_exx_dword_ptr_eyy_add_dword(asm.EAX, asm.EAX, 0x768)
            Defeat_asm.mov_exx_dword_ptr_eyy_add_dword(asm.ESI, asm.EAX, 0x90)
            Defeat_asm.mov_exx_dword_ptr_eyy(asm.EBX,asm.ESI)
            Defeat_asm.mov_exx(asm.EDX,0x2d)
            Defeat_asm.mov_exx_eyy(asm.ECX,asm.ESI)
            Defeat_asm.mov_exx(asm.EDI,0xFFFFFF9C)
            Defeat_asm.mov_exx_dword_ptr_eyy_add_byte(asm.EAX,asm.ESI,0x04)
            Defeat_asm.push_exx(asm.ESI)
            Defeat_asm.push_exx(asm.EAX)
            Defeat_asm.call(0x413400)
            return Defeat_asm
            
    asm.justRunThread(Defeat())
        

def noSlot_operstion(noSlot_event):
    while not noSlot_event.is_set():
        try:
            start=data.PVZ_memory.read_bool(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x774)+0x88)+0x1a)
            if  start==True:
                data.PVZ_memory.write_bool(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x774)+0x88)+0x1a,False)
        except:
            pass
        time.sleep(1)
noSlot_event=Event()
noSlot_thread=None
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
        
        def creat_asm(self,startAddress):
            Save_asm=asm.Asm(startAddress)
            Save_asm.mov_exx_dword_ptr(asm.ECX,0x006A9EC0)
            Save_asm.mov_exx_dword_ptr_eyy_add_dword(asm.ECX, asm.ECX, 0x768)
            Save_asm.push_exx(asm.ECX)
            Save_asm.call(0x408c30)
            return Save_asm
            
    asm.runThread(Save())
    
def load():
    class Load:
        def __init__(self) -> None:
            pass
        
        def creat_asm(self,startAddress):
            Load_asm=asm.Asm(startAddress)
            Load_asm.mov_exx_dword_ptr(asm.ESI,0x006A9EC0)
            Load_asm.push_exx(asm.ESI)
            Load_asm.call(0x44f7a0)
            return Load_asm
            
    asm.runThread(Load())


def spoils(spoils_config):
    global newmem_spoils
    global newmem_spoils2
    print(spoils_config)
    if(spoils_config!=False):
        data.PVZ_memory.write_bytes(0x00530275,b'\x70',1)
        newmem_spoils=pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 256) 
        newmem_spoils2=pymem.memory.allocate_memory(data.PVZ_memory.process_handle, 32) 
        print(hex(newmem_spoils))
        print(hex(newmem_spoils2))
        shellcode=asm.Asm(newmem_spoils)
        shellcode.mov_exx_dword_ptr_eyy(asm.EAX,asm.EBX)
        shellcode.mov_exx(asm.ESI,4)
        shellcode.call(0x00453630)
        if(len(spoils_config)>0):
            shellcode.random(100)
            shellcode.cmp_exx_byte(asm.EDX,spoils_config[0]["percent"])
            shellcode.add_byte(0x72)#jb
            shellcode.add_byte(0x05)#小于则后移5位
            shellcode.add_byte(0xe9)#大于则jmp
            shellcode.add_dword(0x1f)
            shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ESI,asm.ESP,0x24)
            shellcode.add_byte(0x0c)#mov esi,[esp+0c]
            shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ECX,asm.EBX,0x04)
            shellcode.push_byte(0x03)            
            if(spoils_config[0]["type"]<=6):
                shellcode.push_byte(spoils_config[0]["type"])
            elif(spoils_config[0]["type"]==7):
                shellcode.push_byte(0x8)
            elif(spoils_config[0]["type"]==8):
                shellcode.push_byte(0xf)
            elif(spoils_config[0]["type"]==9):
                shellcode.push_byte(0x10)
            elif(spoils_config[0]["type"]==10):
                shellcode.push_byte(0x12)      
            if(spoils_config[0]["card"]==-1):
                shellcode.mov_dword_ptr_dword(0x00751EC0,0)    
            else:   
                shellcode.mov_dword_ptr_dword(0x00751EC0,spoils_config[0]["card"])
            shellcode.push_exx(asm.ESI)
            shellcode.lea_exy_byte(0x47,0xec)
            shellcode.push_exx(asm.EAX)
            shellcode.call(0x0040CB10)
            if(len(spoils_config)>1):
                shellcode.random(100)
                shellcode.cmp_exx_byte(asm.EDX,spoils_config[1]["percent"])
                shellcode.add_byte(0x72)#jb
                shellcode.add_byte(0x05)#小于则后移5位
                shellcode.add_byte(0xe9)#大于则jmp
                shellcode.add_dword(0x1b)
                shellcode.push_byte(0x03)            
                if(spoils_config[1]["type"]<=6):
                    shellcode.push_byte(spoils_config[1]["type"])
                elif(spoils_config[1]["type"]==7):
                    shellcode.push_byte(0x8)
                elif(spoils_config[1]["type"]==8):
                    shellcode.push_byte(0xf)
                elif(spoils_config[1]["type"]==9):
                    shellcode.push_byte(0x10)
                elif(spoils_config[1]["type"]==10):
                    shellcode.push_byte(0x12)      
                if(spoils_config[1]["card"]==-1):
                    shellcode.mov_dword_ptr_dword(0x00751EC0,0)    
                else:   
                    shellcode.mov_dword_ptr_dword(0x00751EC0,spoils_config[1]["card"])
                shellcode.push_exx(asm.ESI)
                shellcode.lea_exy_byte(0x4f,0xe2)
                shellcode.push_exx(asm.ECX)
                shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ECX,asm.EBX,0x04)
                shellcode.call(0x0040CB10)
                if(len(spoils_config)>2):
                    shellcode.random(100)
                    shellcode.cmp_exx_byte(asm.EDX,spoils_config[2]["percent"])
                    shellcode.add_byte(0x72)#jb
                    shellcode.add_byte(0x05)#小于则后移5位
                    shellcode.add_byte(0xe9)#大于则jmp
                    shellcode.add_dword(0x1b)
                    shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ECX,asm.EBX,0x04)
                    shellcode.push_byte(0x03)            
                    if(spoils_config[2]["type"]<=6):
                        shellcode.push_byte(spoils_config[2]["type"])
                    elif(spoils_config[2]["type"]==7):
                        shellcode.push_byte(0x8)
                    elif(spoils_config[2]["type"]==8):
                        shellcode.push_byte(0xf)
                    elif(spoils_config[2]["type"]==9):
                        shellcode.push_byte(0x10)
                    elif(spoils_config[2]["type"]==10):
                        shellcode.push_byte(0x12)      
                    if(spoils_config[2]["card"]==-1):
                        shellcode.mov_dword_ptr_dword(0x00751EC0,0)    
                    else:   
                        shellcode.mov_dword_ptr_dword(0x00751EC0,spoils_config[2]["card"])
                    shellcode.push_exx(asm.ESI)
                    shellcode.lea_exy_byte(0x57,0xd8)
                    shellcode.push_exx(asm.EDX)
                    shellcode.call(0x0040CB10)
                    if(len(spoils_config)>3):
                        shellcode.random(100)
                        shellcode.cmp_exx_byte(asm.EDX,spoils_config[3]["percent"])
                        shellcode.add_byte(0x72)#jb
                        shellcode.add_byte(0x05)#小于则后移5位
                        shellcode.add_byte(0xe9)#大于则jmp
                        shellcode.add_dword(0x1b)
                        shellcode.mov_exx_dword_ptr_eyy_add_byte(asm.ECX,asm.EBX,0x04)
                        shellcode.push_byte(0x03)            
                        if(spoils_config[3]["type"]<=6):
                            shellcode.push_byte(spoils_config[2]["type"])
                        elif(spoils_config[3]["type"]==7):
                            shellcode.push_byte(0x8)
                        elif(spoils_config[3]["type"]==8):
                            shellcode.push_byte(0xf)
                        elif(spoils_config[3]["type"]==9):
                            shellcode.push_byte(0x10)
                        elif(spoils_config[3]["type"]==10):
                            shellcode.push_byte(0x12)      
                        if(spoils_config[3]["card"]==-1):
                            shellcode.mov_dword_ptr_dword(0x00751EC0,0)    
                        else:   
                            shellcode.mov_dword_ptr_dword(0x00751EC0,spoils_config[3]["card"])
                        shellcode.push_exx(asm.ESI)
                        shellcode.add_exx_byte(asm.EDI,0xce)
                        shellcode.push_exx(asm.EDI)
                        shellcode.call(0x0040CB10)
            shellcode.pop_exx(asm.EDI)
            shellcode.pop_exx(asm.ESI)
            shellcode.pop_exx(asm.EBX)
            shellcode.mov_exx_eyy(asm.ESP,asm.EBP)
            shellcode.pop_exx(asm.EBP)
            shellcode.ret()
            shellcode.jmp(0x005302D2)            
            
        tempcode=asm.Asm(newmem_spoils2)
        tempcode.mov_exx_dword_ptr(asm.EAX,0x00751EC0)
        tempcode.add_byte(0x89)
        tempcode.add_byte(0x45)
        tempcode.add_byte(0x68)
        tempcode.jmp(0x0042FFBD)
        
        
        data.PVZ_memory.write_bytes(newmem_spoils2,bytes(tempcode.code[:tempcode.index]),tempcode.index)
        data.PVZ_memory.write_bytes(0x42ffb6,b'\xe9'+calculate_call_address(newmem_spoils2-0x0042ffbb)+b'\x66\x90',7)
        data.PVZ_memory.write_bytes(newmem_spoils,bytes(shellcode.code[:shellcode.index]),shellcode.index)
        data.PVZ_memory.write_bytes(0x00530277,b'\xe9'+calculate_call_address(newmem_spoils-0x0053027c),5)
    else:
        data.PVZ_memory.write_bytes(0x00530275,b'\x75',1)
        data.PVZ_memory.write_bytes(0x42ffb6,b'\xc7\x45\x68\x00\x00\x00\x00',7)
        data.PVZ_memory.write_bytes(0x00530277,b'\x8b\x03\xbe\x04\x00',5)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_spoils)
        pymem.memory.free_memory(data.PVZ_memory.process_handle, newmem_spoils2)

        