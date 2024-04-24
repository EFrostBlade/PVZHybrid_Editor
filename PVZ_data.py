from pymem import Pymem

PVZ_memory=Pymem()
def update_PVZ_memory(memory):
    global PVZ_memory
    PVZ_memory=memory
    
baseAddress=0x006A9EC0

zombiesType=["普僵","旗帜","路障","撑杆","铁桶","冰车二爷","铁门","黑橄榄","武装舞王",
                 "舞伴","泳圈普僵","潜水","冰车巨人","雪橇","海豚机枪","小丑","气球舞王","矿工",
                 "跳跳","冰车雪人","飞贼","扶梯","篮球","巨人","小鬼","僵王","豌豆僵尸",
                 "坚果僵尸","辣椒僵尸","机枪僵尸","冰窝瓜僵尸","高冰果僵尸","红眼","迪斯科",
                 "舞者","骷髅"]

class plant:
    def __init__(self,addr):
        self.addr=addr
        self.no=int((addr-(PVZ_memory.read_int(PVZ_memory.read_int(PVZ_memory.read_int(baseAddress)+0x768)+0xac)))/0x14c)
        self.exist=PVZ_memory.read_bytes(self.addr+0x141,1)
        self.row=PVZ_memory.read_int(self.addr+0x1c)
        self.col=PVZ_memory.read_int(self.addr+0x28)
        self.type=PVZ_memory.read_int(self.addr+0x24)
        self.x=PVZ_memory.read_int(self.addr+0x8)
        self.y=PVZ_memory.read_int(self.addr+0xc)
        self.state=PVZ_memory.read_int(self.addr+0x3c)
        self.hp=PVZ_memory.read_int(self.addr+0x40)
        self.maxhp=PVZ_memory.read_int(self.addr+0x44)
        self.producttime=PVZ_memory.read_int(self.addr+0x58)
    def modify(self,row,col,x,y,state,hp):
        PVZ_memory.write_int(self.addr+0x1c,row-1)
        PVZ_memory.write_int(self.addr+0x28,col-1)
        PVZ_memory.write_int(self.addr+0x8,x)
        PVZ_memory.write_int(self.addr+0xc,y)
        PVZ_memory.write_int(self.addr+0x3c,state)
        PVZ_memory.write_int(self.addr+0x40,hp)
        PVZ_memory.write_int(self.addr+0x44,hp)
class zombie:
    def __init__(self,addr):
        self.addr=addr
        self.no=int((addr-(PVZ_memory.read_int(PVZ_memory.read_int(PVZ_memory.read_int(baseAddress)+0x768)+0x90)))/0x15c)
        self.exist=PVZ_memory.read_int(self.addr+0xec)
        self.row=PVZ_memory.read_int(self.addr+0x1c)
        self.type=PVZ_memory.read_int(self.addr+0x24)
        self.x=PVZ_memory.read_float(self.addr+0x2c)
        self.y=PVZ_memory.read_float(self.addr+0x30)
        self.size=PVZ_memory.read_float(self.addr+0x11c)
        self.state=PVZ_memory.read_int(self.addr+0x28)
        self.hp=PVZ_memory.read_int(self.addr+0xc8)
        self.maxHP=PVZ_memory.read_int(self.addr+0xcc)
        self.hatType=PVZ_memory.read_int(self.addr+0xc4)
        self.hatHP=PVZ_memory.read_int(self.addr+0xd0)
        self.maxHatHP=PVZ_memory.read_int(self.addr+0xd4)
        self.doorHP=PVZ_memory.read_int(self.addr+0xdc)
        self.maxDoorHP=PVZ_memory.read_int(self.addr+0xe0)
        self.slow=PVZ_memory.read_int(self.addr+0xac)
        self.butter=PVZ_memory.read_int(self.addr+0xb0)
        self.frozen=PVZ_memory.read_int(self.addr+0xb4)
        self.isVisible=PVZ_memory.read_bool(self.addr+0x18)
        self.isEating=PVZ_memory.read_bool(self.addr+0x51)
        self.isHpynotized=PVZ_memory.read_bool(self.addr+0xb8)
        self.isBlow=PVZ_memory.read_bool(self.addr+0xb9)
        self.isDying=PVZ_memory.read_bool(self.addr+0xba)

    def setRow(self,row):
        PVZ_memory.write_int(self.addr+0x1c,row)
    def setX(self,x):
        PVZ_memory.write_float(self.addr+0x2c,x)
    def setY(self,y):
        PVZ_memory.write_float(self.addr+0x30,y)
    def setSize(self,size):
        PVZ_memory.write_float(self.addr+0x11c,size)
    def setState(self,state):
        PVZ_memory.write_int(self.addr+0x28,state)
    def setHP(self,hp):
        PVZ_memory.write_int(self.addr+0xc8,hp)
        PVZ_memory.write_int(self.addr+0xcc,hp)
    def setHatHP(self,hatHP):
        PVZ_memory.write_int(self.addr+0xd0,hatHP)
        PVZ_memory.write_int(self.addr+0xd4,hatHP)
    def setDoorHP(self,doorHP):
        PVZ_memory.write_int(self.addr+0xdc,doorHP)
        PVZ_memory.write_int(self.addr+0xe0,doorHP)
    def setSlow(self,slow):
        PVZ_memory.write_int(self.addr+0xac,slow)
    def setButter(self,butter):
        PVZ_memory.write_int(self.addr+0xb0,butter)
    def setFrozen(self,frozen):
        PVZ_memory.write_int(self.addr+0xb4,frozen)
    def setExist(self,exist):
        PVZ_memory.write_int(self.addr+0xec,exist)
    def setIsVisible(self,isVisible):
        PVZ_memory.write_bool(self.addr+0x18,isVisible)
    def setIsEating(self,isEating):
        PVZ_memory.write_bool(self.addr+0x51,isEating)
    def setIsHPynotized(self,isHPynotized):
        PVZ_memory.write_bool(self.addr+0xb8,isHPynotized)
    def setIsBlow(self,isBlow):
        PVZ_memory.write_bool(self.addr+0xb9,isBlow)
    def setIsDying(self,isDying):
        PVZ_memory.write_bool(self.addr+0xba,isDying)


class item:
    def __init__(self,addr):
        self.addr=addr
        self.no=int((addr-(PVZ_memory.read_int(PVZ_memory.read_int(PVZ_memory.read_int(baseAddress)+0x768)+0x11c)))/0xec)
        self.exist=PVZ_memory.read_bytes(self.addr+0x20,1)
        self.Row = PVZ_memory.read_int(self.addr + 0x14)
        self.Col = PVZ_memory.read_int(self.addr + 0x10)
        self.Type = PVZ_memory.read_int(self.addr + 8)