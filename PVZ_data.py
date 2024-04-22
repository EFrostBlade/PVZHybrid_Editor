from editor import PVZ_memory

base=0x006A9EC0
class plant:
    def __init__(self,addr):
        self.addr=addr
        self.no=int((addr-(PVZ_memory.read_int(PVZ_memory.read_int(PVZ_memory.read_int(base)+0x768)+0xac)))/0x14c)
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
        self.no=int((addr-(PVZ_memory.read_int(PVZ_memory.read_int(PVZ_memory.read_int(base)+0x768)+0x90)))/0x15c)
        self.exist=PVZ_memory.read_bytes(self.addr+0xec,1)
        self.row=PVZ_memory.read_int(self.addr+0x1c)
        self.type=PVZ_memory.read_int(self.addr+0x24)
        self.x=PVZ_memory.read_float(self.addr+0x2c)
        self.y=PVZ_memory.read_float(self.addr+0x30)
        self.size=PVZ_memory.read_float(self.addr+0x11c)
        self.state=PVZ_memory.read_int(self.addr+0x28)
        self.hp=PVZ_memory.read_int(self.addr+0xc8)
        self.maxhp=PVZ_memory.read_int(self.addr+0xcc)
        self.hathp=PVZ_memory.read_int(self.addr+0xd0)
        self.maxhathp=PVZ_memory.read_int(self.addr+0xd4)
        self.doorhp=PVZ_memory.read_int(self.addr+0xdc)
        self.maxdoorhp=PVZ_memory.read_int(self.addr+0xe0)
        self.slow=PVZ_memory.read_int(self.addr+0xac)
        self.butter=PVZ_memory.read_int(self.addr+0xb0)
        self.frozen=PVZ_memory.read_int(self.addr+0xb4)
    def modify(self,row,x,y,state,hp,hathp,doorhp,slow,butter,frozen):
        PVZ_memory.write_int(self.addr+0x1c,row-1)
        PVZ_memory.write_float(self.addr+0x2c,x)
        PVZ_memory.write_float(self.addr+0x30,y)
        PVZ_memory.write_int(self.addr+0x28,state)
        PVZ_memory.write_int(self.addr+0xc8,hp)
        PVZ_memory.write_int(self.addr+0xcc,hp)
        PVZ_memory.write_int(self.addr+0xd0,hathp)
        PVZ_memory.write_int(self.addr+0xd4,hathp)
        PVZ_memory.write_int(self.addr+0xdc,doorhp)
        PVZ_memory.write_int(self.addr+0xe0,doorhp)
        PVZ_memory.write_int(self.addr+0xac,slow)
        PVZ_memory.write_int(self.addr+0xb0,butter)
        PVZ_memory.write_int(self.addr+0xb4,frozen)
class item:
    def __init__(self,addr):
        self.addr=addr
        self.no=int((addr-(PVZ_memory.read_int(PVZ_memory.read_int(PVZ_memory.read_int(base)+0x768)+0x11c)))/0xec)
        self.exist=PVZ_memory.read_bytes(self.addr+0x20,1)
        self.Row = PVZ_memory.read_int(self.addr + 0x14)
        self.Col = PVZ_memory.read_int(self.addr + 0x10)
        self.Type = PVZ_memory.read_int(self.addr + 8)