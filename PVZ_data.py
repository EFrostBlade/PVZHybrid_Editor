from pymem import Pymem

PVZ_memory = Pymem()
PVZ_pid = 0


def update_PVZ_memory(memory):
    global PVZ_memory
    PVZ_memory = memory


def update_PVZ_pid(pid):
    global PVZ_pid
    PVZ_pid = pid


baseAddress = 0x006A9EC0

zombiesType = ["普僵", "旗帜", "路障", "撑杆", "铁桶", "冰车二爷", "铁门", "黑橄榄", "武装舞王",
               "舞伴", "泳圈普僵", "潜水", "冰车巨人", "雪橇", "海豚机枪", "小丑", "气球舞王", "矿工",
               "跳跳", "冰车雪人", "飞贼", "扶梯", "篮球", "巨人", "小鬼", "僵王", "豌豆僵尸",
               "坚果僵尸", "辣椒僵尸", "机枪僵尸", "冰窝瓜僵尸", "高冰果僵尸", "红眼", "迪斯科",
               "舞者", "骷髅","死灵法师","火焰迪斯科","火焰舞者","小黄鸭僵尸","床车僵尸","小摔哥僵尸"]

itemType = ["未知0", "墓碑", "坑洞", "梯子", "蓝色传送门", "白色传送门", "未知6", "罐子", "未知8",
            "未知9", "蜗牛", "钉耙", "脑子","未知13","未知14","小黄鸭"]
plantsType = ['豌豆向日葵', '阳光豆', '阳光炸弹', '火炬坚果', '阳光土豆雷', '寒冰香蒲', '大蒜花',
              '双发仙人掌', '小盆菇', '阳光向日葵', '冰瓜大喷菇', '墓碑埋雷者', '红眼菇', '阳光胆小菇',
              '雪花寒冰菇', '魅惑毁灭菇', '豌豆睡莲', '冰菇窝瓜', '豌豆许愿池', '毁灭海草', '樱桃辣椒',
              '黄油地刺', '冰炬树桩', '高冰果', '海坚果', '6号路灯花', '豌豆大炮', '仙人三叶草', '玉米卷香蒲',
              '地刺杨桃', '忧郁南瓜头', '磁力坚果', '机枪卷心菜投手', '阳光花盆', '三线玉米投手', '随机植物盒子',
              '魅惑大蒜', '咖啡伞', '仙人三叶花', '西瓜坚果', '汉堡射手', '阳光南瓜掌', '黄油忧郁菇', '西瓜香蒲',
              '阳光菇投手', '金盏吸金磁', '钢刺坚果王', '毁灭加农炮',
              '模仿者', '爆炸坚果', '巨大坚果', '芽', '(反向)双发仙人掌', '<null>', '拖拽植物 (僵尸迷阵)',
              '填补土坑', '<阳光>', '<钻石>', '购买潜水僵尸 (僵尸水族馆)', '购买奖杯 (僵尸水族馆)',
              '空', '空', '空', '空', '空', '空', '空', '空', '空',
              '空', '空', '空', '空', '空', '空',
              '火爆地雷', '火爆坚果墙', '豌豆香蒲', '冰瓜香蒲', '烈火南瓜头', '僵尸豌豆射手',
              '寒冰三叶草', '热狗射手', '寒冰仙人掌', '影流窝瓜王', '黄油JOKER', '向日葵女王', '大蒜辣椒',
              '至尊VIP坚果', '僵尸坚果墙', '魅惑菇射手', '财神金盏花', '猫砂盆', '坑洞坚果', 'QQ弹弹大喷菇',
              '寒冰地刺', '土杨桃', '精灵菇', '川菜投手', '坚果模仿者', '窝瓜坚果', '冰冻坚果', '头脑风暴',
              '宝藏吞噬者', '全息卡牌投影', '成长咖啡豆', '寒光菇', '骄阳豌豆射手', '荧光木槌', '狂野机枪射手',
              '生命重塑者', '双生樱桃', '幸运四叶草', '黄金向日葵','土豆加农炮','惩戒牢笼','备用物资','地刺大嘴花',
                '僵尸豆','禁忌毁灭菇','消消乐糖果','海冰菇','莲叶壳','小猫向日葵']
for _ in range(len(plantsType),256):
    plantsType.append('占位')
plantsType=plantsType+["普僵", "旗帜", "路障", "撑杆", "铁桶", "冰车二爷", "铁门", "黑橄榄", "武装舞王",
               "舞伴", "泳圈普僵", "潜水", "冰车巨人", "雪橇", "海豚机枪", "小丑", "气球舞王", "矿工",
               "跳跳", "冰车雪人", "飞贼", "扶梯", "篮球", "巨人", "小鬼", "僵王", "豌豆僵尸",
               "坚果僵尸", "辣椒僵尸", "机枪僵尸", "冰窝瓜僵尸", "高冰果僵尸", "红眼", "迪斯科",
               "舞者", "骷髅","死灵法师","火焰迪斯科","火焰舞者","小黄鸭僵尸","床车僵尸","小摔哥僵尸"]
plantPutType = ['豌豆向日葵', '阳光豆', '阳光炸弹', '火炬坚果', '阳光土豆雷', '寒冰香蒲', '大蒜花',
                '双发仙人掌', '小盆菇', '阳光向日葵', '冰瓜大喷菇', '墓碑埋雷者', '红眼菇', '阳光胆小菇',
                '雪花寒冰菇', '魅惑毁灭菇', '豌豆睡莲', '冰菇窝瓜', '豌豆许愿池', '毁灭海草', '樱桃辣椒',
                '黄油地刺', '冰炬树桩', '高冰果', '海坚果', '6号路灯花', '豌豆大炮', '仙人三叶草', '玉米卷香蒲',
                '地刺杨桃', '忧郁南瓜头', '磁力坚果', '机枪卷心菜投手', '阳光花盆', '三线玉米投手', '随机植物盒子',
                '魅惑大蒜', '咖啡伞', '仙人三叶花', '西瓜坚果', '汉堡射手', '阳光南瓜掌', '黄油忧郁菇', '西瓜香蒲',
                '阳光菇投手', '金盏吸金磁', '钢刺坚果王', '毁灭加农炮', '模仿者', '爆炸坚果', '巨大坚果', '芽',
                '火爆地雷', '火爆坚果墙', '豌豆香蒲', '冰瓜香蒲', '烈火南瓜头', '僵尸豌豆射手',
                '寒冰三叶草', '热狗射手', '寒冰仙人掌', '影流窝瓜王', '黄油JOKER', '向日葵女王', '大蒜辣椒',
                '至尊VIP坚果', '僵尸坚果墙', '魅惑菇射手', '财神金盏花', '猫砂盆', '坑洞坚果', 'QQ弹弹大喷菇',
                '寒冰地刺', '土杨桃', '精灵菇', '川菜投手', '坚果模仿者', '窝瓜坚果', '冰冻坚果', '头脑风暴',
                '宝藏吞噬者', '全息卡牌投影', '成长咖啡豆', '寒光菇', '骄阳豌豆射手', '荧光木槌', '狂野机枪射手',
                '生命重塑者', '双生樱桃', '幸运四叶草', '黄金向日葵','土豆加农炮','惩戒牢笼','备用物资','地刺大嘴花',
                '僵尸豆','禁忌毁灭菇','消消乐糖果','海冰菇','莲叶壳','小猫向日葵'
                ]
bulletType = ['豌豆', '冰豌豆', '卷心菜', '西瓜', '孢子', '冰西瓜', '火球(隐形)', '星星', '仙人掌刺', '篮球',
              '玉米粒', '毁灭菇', '黄油', '僵尸豌豆', '小阳光菇', '大阳光菇', '黑色豌豆', '寒冰刺', '魅惑箭',
              '银币', '金币', '钻石', '土豆雷', '川菜', '辣椒', '白火球']
keyTpye = ['无', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
           'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
           '小0', '小1', '小2', '小3', '小4', '小5', '小6',
           '小7', '小8', '小9', '小*', '小+', '小-', '小.', '小\\',
           'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12'
           ]

keyCode = ['',  0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x41, 0x42,
           0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F,
           0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x60, 0x61,
           0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6D, 0x6E, 0x6F,
           0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B
           ]


class plant:
    def __init__(self, addr):
        self.addr = addr
        self.no = PVZ_memory.read_ushort(self.addr+0x148)
        self.exist = PVZ_memory.read_bool(self.addr+0x141)
        self.x = PVZ_memory.read_int(self.addr+0x8)
        self.y = PVZ_memory.read_int(self.addr+0xc)
        self.row = PVZ_memory.read_int(self.addr+0x1c)
        self.col = PVZ_memory.read_int(self.addr+0x28)
        self.type = PVZ_memory.read_int(self.addr+0x24)
        self.state = PVZ_memory.read_int(self.addr+0x3c)
        self.hp = PVZ_memory.read_int(self.addr+0x40)
        self.maxhp = PVZ_memory.read_int(self.addr+0x44)
        self.dieTime = PVZ_memory.read_int(self.addr+0x4c)
        self.cinderTime = PVZ_memory.read_int(self.addr+0x50)
        self.effectTime = PVZ_memory.read_int(self.addr+0x54)  # 蘑菇成长
        self.productTime = PVZ_memory.read_int(self.addr+0x58)  # 特殊子弹攻击
        self.attackTime = PVZ_memory.read_int(self.addr+0x90)  # 常规攻击
        self.productInterval = PVZ_memory.read_int(self.addr+0x5c)
        self.sunTime = PVZ_memory.read_int(self.addr+0xdc)
        self.humTime = PVZ_memory.read_int(self.addr+0x128)
        self.mushroomTime = PVZ_memory.read_int(self.addr+0x130)
        self.isVisible = PVZ_memory.read_bool(self.addr+0x18)
        self.isSquash = PVZ_memory.read_bool(self.addr+0x142)
        self.isSleep = PVZ_memory.read_bool(self.addr+0x143)
        self.isLight = PVZ_memory.read_bool(self.addr+0x145)
        self.isAttack = PVZ_memory.read_int(self.addr+0x48)

    def setExist(self, exist):
        PVZ_memory.write_bool(self.addr + 0x141, exist)

    def setX(self, x):
        PVZ_memory.write_int(self.addr + 0x8, x)

    def setY(self, y):
        PVZ_memory.write_int(self.addr + 0xc, y)

    def setRow(self, row):
        PVZ_memory.write_int(self.addr + 0x1c, row)

    def setCol(self, col):
        PVZ_memory.write_int(self.addr + 0x28, col)

    def setType(self, type):
        PVZ_memory.write_int(self.addr + 0x24, type)

    def setState(self, state):
        PVZ_memory.write_int(self.addr + 0x3c, state)

    def setHP(self, hp):
        PVZ_memory.write_int(self.addr + 0x40, hp)
        PVZ_memory.write_int(self.addr + 0x44, hp)

    def setDieTime(self, dieTime):
        PVZ_memory.write_int(self.addr + 0x4c, dieTime)

    def setCinderTime(self, cinderTime):
        PVZ_memory.write_int(self.addr + 0x50, cinderTime)

    def setEffectTime(self, effectTime):
        PVZ_memory.write_int(self.addr + 0x54, effectTime)

    def setProductTime(self, productTime):
        PVZ_memory.write_int(self.addr + 0x58, productTime)

    def setAttackTime(self, attackTime):
        PVZ_memory.write_int(self.addr + 0x90, attackTime)

    def setProductInterval(self, productInterval):
        PVZ_memory.write_int(self.addr + 0x5c, productInterval)

    def setSunTime(self, sunTime):
        PVZ_memory.write_int(self.addr + 0xdc, sunTime)

    def setHumTime(self, humTime):
        PVZ_memory.write_int(self.addr + 0x12c, humTime)

    def setmushroomTime(self, mushroomTime):
        PVZ_memory.write_int(self.addr + 0x130, mushroomTime)

    def setIsVisible(self, isVisible):
        PVZ_memory.write_bool(self.addr + 0x18, isVisible)

    def setIsSquash(self, isSquash):
        PVZ_memory.write_bool(self.addr + 0x142, isSquash)

    def setIsSleep(self, isSleep):
        PVZ_memory.write_bool(self.addr + 0x143, isSleep)

    def setIsLight(self, isLight):
        PVZ_memory.write_bool(self.addr + 0x145, isLight)

    def setIsAttack(self, isAttack):
        PVZ_memory.write_int(self.addr + 0x48, isAttack)


class zombie:
    def __init__(self, addr):
        self.addr = addr
        self.no = PVZ_memory.read_ushort(self.addr+0x158)
        self.exist = PVZ_memory.read_int(self.addr+0xec)
        self.row = PVZ_memory.read_int(self.addr+0x1c)+1
        self.type = PVZ_memory.read_int(self.addr+0x24)
        self.x = PVZ_memory.read_float(self.addr+0x2c)
        self.y = PVZ_memory.read_float(self.addr+0x30)
        self.size = PVZ_memory.read_float(self.addr+0x11c)
        self.state = PVZ_memory.read_int(self.addr+0x28)
        self.hp = PVZ_memory.read_int(self.addr+0xc8)
        self.maxHP = PVZ_memory.read_int(self.addr+0xcc)
        self.hatType = PVZ_memory.read_int(self.addr+0xc4)
        self.hatHP = PVZ_memory.read_int(self.addr+0xd0)
        self.maxHatHP = PVZ_memory.read_int(self.addr+0xd4)
        self.doorHP = PVZ_memory.read_int(self.addr+0xdc)
        self.maxDoorHP = PVZ_memory.read_int(self.addr+0xe0)
        self.slow = PVZ_memory.read_int(self.addr+0xac)
        self.butter = PVZ_memory.read_int(self.addr+0xb0)
        self.frozen = PVZ_memory.read_int(self.addr+0xb4)
        self.isVisible = PVZ_memory.read_bool(self.addr+0x18)
        self.isEating = PVZ_memory.read_bool(self.addr+0x51)
        self.isHpynotized = PVZ_memory.read_bool(self.addr+0xb8)
        self.isBlow = PVZ_memory.read_bool(self.addr+0xb9)
        self.isDying = PVZ_memory.read_bool(self.addr+0xba)
        self.stolenPlant = PVZ_memory.read_ushort(self.addr+0x128)

    def setRow(self, row):
        PVZ_memory.write_int(self.addr+0x1c, row-1)

    def setX(self, x):
        PVZ_memory.write_float(self.addr+0x2c, x)

    def setY(self, y):
        PVZ_memory.write_float(self.addr+0x30, y)

    def setSize(self, size):
        PVZ_memory.write_float(self.addr+0x11c, size)

    def setState(self, state):
        PVZ_memory.write_int(self.addr+0x28, state)

    def setHP(self, hp):
        PVZ_memory.write_int(self.addr+0xc8, hp)
        PVZ_memory.write_int(self.addr+0xcc, hp)

    def setHatHP(self, hatHP):
        PVZ_memory.write_int(self.addr+0xd0, hatHP)
        PVZ_memory.write_int(self.addr+0xd4, hatHP)

    def setDoorHP(self, doorHP):
        PVZ_memory.write_int(self.addr+0xdc, doorHP)
        PVZ_memory.write_int(self.addr+0xe0, doorHP)

    def setSlow(self, slow):
        PVZ_memory.write_int(self.addr+0xac, slow)

    def setButter(self, butter):
        PVZ_memory.write_int(self.addr+0xb0, butter)

    def setFrozen(self, frozen):
        PVZ_memory.write_int(self.addr+0xb4, frozen)

    def setExist(self, exist):
        PVZ_memory.write_int(self.addr+0xec, exist)

    def setIsVisible(self, isVisible):
        PVZ_memory.write_bool(self.addr+0x18, isVisible)

    def setIsEating(self, isEating):
        PVZ_memory.write_bool(self.addr+0x51, isEating)

    def setIsHPynotized(self, isHPynotized):
        PVZ_memory.write_bool(self.addr+0xb8, isHPynotized)

    def setIsBlow(self, isBlow):
        PVZ_memory.write_bool(self.addr+0xb9, isBlow)

    def setIsDying(self, isDying):
        PVZ_memory.write_bool(self.addr+0xba, isDying)

    def setStolenPlant(self, stolenPlant):
        PVZ_memory.write_ushort(self.addr+0x128, stolenPlant)


class item:
    def __init__(self, addr):
        self.addr = addr
        self.no = PVZ_memory.read_ushort(self.addr + 0xe8)
        self.exist = PVZ_memory.read_bool(self.addr+0x20)
        self.row = PVZ_memory.read_int(self.addr + 0x14)+1
        self.col = PVZ_memory.read_int(self.addr + 0x10)+1
        self.type = PVZ_memory.read_int(self.addr + 0x8)
        self.time = PVZ_memory.read_int(self.addr + 0x18)

    def setExist(self, exist):
        PVZ_memory.write_bool(self.addr+0x20, exist)

    def setRow(self, row):
        PVZ_memory.write_int(self.addr+0x14, row-1)

    def setCol(self, col):
        PVZ_memory.write_int(self.addr+0x10, col-1)

    def setTime(self, time):
        PVZ_memory.write_int(self.addr+0x18, time)

class car:
    def __init__(self,addr):
        self.addr=addr
        self.exist = PVZ_memory.read_bool(self.addr+0x30)
        self.no = PVZ_memory.read_ushort(self.addr + 0x44)
        self.row = PVZ_memory.read_int(self.addr + 0x14)

        
    def setExist(self, exist):
        PVZ_memory.write_bool(self.addr + 0x30, exist)

class slot:
    def __init__(self, addr):
        self.addr = addr
        self.no = PVZ_memory.read_ushort(self.addr + 0x2c)
        self.canUse = PVZ_memory.read_bool(self.addr+0x48)
        self.type = PVZ_memory.read_int(self.addr + 0x34)
        self.imitaterType = PVZ_memory.read_int(self.addr + 0x34)
        self.cooldown = PVZ_memory.read_int(self.addr + 0x28)
        self.elapsed = PVZ_memory.read_int(self.addr + 0x24)
        self.isVisible = PVZ_memory.read_bool(self.addr+0x18)
        self.count = PVZ_memory.read_int(self.addr + 0x4c)

    def setCanUse(self, canUse):
        PVZ_memory.write_bool(self.addr+0x48, canUse)

    def setType(self, type):
        PVZ_memory.write_int(self.addr + 0x34, type)

    def setImitaterType(self, imitaterType):
        PVZ_memory.write_int(self.addr + 0x34, imitaterType)

    def setCooldown(self, cooldown):
        PVZ_memory.write_int(self.addr + 0x28, cooldown)

    def setElapsed(self, elapsed):
        PVZ_memory.write_int(self.addr + 0x24, elapsed)

    def setIsVisible(self, isVisible):
        PVZ_memory.write_bool(self.addr + 0x18, isVisible)

    def setCount(self, count):
        PVZ_memory.write_int(self.addr + 0x4c, count)


class plantCharacteristic:
    def __init__(self, type):
        self.addr = 0x007A2010+type*0x24
        self.sun = PVZ_memory.read_int(self.addr)
        self.cd = PVZ_memory.read_int(self.addr+0x4)
        self.canAttack = PVZ_memory.read_bool(self.addr+0x8)
        self.attackInterval = PVZ_memory.read_int(self.addr+0xc)

    def setSun(self, sun):
        PVZ_memory.write_int(self.addr, sun)

    def setCd(self, cd):
        PVZ_memory.write_int(self.addr + 0x4, cd)

    def setCanAttack(self, canAttack):
        PVZ_memory.write_bool(self.addr + 0x8, canAttack)

    def setAttackInterval(self, attackInterval):
        PVZ_memory.write_int(self.addr + 0xc, attackInterval)
