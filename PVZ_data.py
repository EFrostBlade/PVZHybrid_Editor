from pymem import Pymem

PVZ_memory = Pymem()
PVZ_pid = 0
PVZ_version = "未找到游戏"
zombies_HP_addresses = None


def update_PVZ_memory(memory):
    global PVZ_memory
    PVZ_memory = memory


def update_PVZ_pid(pid):
    global PVZ_pid
    PVZ_pid = pid


def update_PVZ_version(version):
    global PVZ_version
    global zombies_HP_addresses
    PVZ_version = version
    zombies_HP_addresses = get_zombies_HP_addresses(PVZ_version)
    print(PVZ_version)


baseAddress = 0x006A9EC0

zombiesType = [
    "普僵",
    "旗帜",
    "路障",
    "撑杆",
    "铁桶",
    "冰车二爷",
    "铁门",
    "黑橄榄",
    "武装舞王",
    "舞伴",
    "泳圈普僵",
    "潜水",
    "冰车巨人",
    "雪橇",
    "海豚机枪",
    "小丑",
    "气球舞王",
    "矿工",
    "跳跳",
    "冰车雪人",
    "飞贼",
    "扶梯",
    "篮球",
    "巨人",
    "小鬼",
    "僵王",
    "豌豆僵尸",
    "坚果僵尸",
    "辣椒僵尸",
    "机枪僵尸",
    "冰窝瓜僵尸",
    "高冰果僵尸",
    "红眼",
    "迪斯科",
    "舞者",
    "骷髅",
    "死灵法师",
    "火焰迪斯科",
    "火焰舞者",
    "小黄鸭僵尸",
    "床车僵尸",
    "小摔哥僵尸",
    "橄榄巨人",
    "橄榄小鬼",
    "雪人矿工",
    "狂野机枪僵尸",
    "火炬坚果僵尸",
    "机枪撑杆僵尸",
    "机枪海豚僵尸",
    "僵尸坚果巨人",
    "僵尸豌豆小鬼",
    "鲨鱼僵尸",
    "寒冰射手僵尸",
    "海妖僵尸",
    "缠绕潜水僵尸",
    "钻石僵尸",
    "防爆门僵尸",
    "骑鸭僵尸",
    "小推车小鬼僵尸",
    "罐子僵尸",  # 59
    "催眠师僵尸",  # 60
    "园丁僵尸",  # 61
    "红眼舞王",  # 62
    "巨人伴舞",  # 63
]
zombieSpaw = zombiesType + [
    "绿帽概率",
    "橄榄废稿头概率",
    "舞王废稿头概率",
    "巨人废稿头概率",
]
itemType = [
    "未知0",
    "墓碑",
    "坑洞",
    "梯子",
    "蓝色传送门",
    "白色传送门",
    "未知6",
    "罐子",
    "未知8",
    "未知9",
    "蜗牛",
    "钉耙",
    "脑子",
    "未知13",
    "未知14",
    "小黄鸭",
]
plantsType = [
    "豌豆向日葵",
    "阳光豆",
    "阳光炸弹",
    "火炬坚果",
    "阳光土豆雷",
    "寒冰香蒲",
    "大蒜花",
    "双发仙人掌",
    "小盆菇",
    "阳光向日葵",
    "冰瓜大喷菇",
    "墓碑埋雷者",
    "红眼菇",
    "阳光胆小菇",
    "雪花寒冰菇",
    "魅惑毁灭菇",
    "豌豆睡莲",
    "冰菇窝瓜",
    "豌豆许愿池",
    "毁灭海草",
    "樱桃辣椒",
    "黄油地刺",
    "冰炬树桩",
    "高冰果",
    "海坚果",
    "6号路灯花",
    "豌豆大炮",
    "仙人三叶草",
    "玉米卷香蒲",
    "地刺杨桃",
    "忧郁南瓜头",
    "磁力坚果",
    "机枪卷心菜投手",
    "阳光花盆",
    "三线玉米投手",
    "随机植物盒子",
    "魅惑大蒜",
    "咖啡伞",
    "仙人三叶花",
    "西瓜坚果",
    "汉堡射手",
    "阳光南瓜掌",
    "黄油忧郁菇",
    "西瓜香蒲",
    "阳光菇投手",
    "金盏吸金磁",
    "钢刺坚果王",
    "毁灭加农炮",
    "模仿者",
    "爆炸坚果",
    "巨大坚果",
    "芽",
    "(反向)双发仙人掌",
    "<null>",
    "拖拽植物 (僵尸迷阵)",
    "填补土坑",
    "<阳光>",
    "<钻石>",
    "购买潜水僵尸 (僵尸水族馆)",
    "购买奖杯 (僵尸水族馆)",
    "空",
    "空",
    "空",
    "空",
    "空",
    "空",
    "空",
    "空",
    "空",
    "空",
    "空",
    "空",
    "空",
    "空",
    "空",
    "火爆地雷",
    "火爆坚果墙",
    "豌豆香蒲",
    "冰瓜香蒲",
    "烈火南瓜头",
    "僵尸豌豆射手",
    "寒冰三叶草",
    "热狗射手",
    "寒冰仙人掌",
    "影流窝瓜王",
    "黄油JOKER",
    "向日葵女王",
    "大蒜辣椒",
    "至尊VIP坚果",
    "僵尸坚果墙",
    "魅惑菇射手",
    "财神金盏花",
    "猫砂盆",
    "坑洞坚果",
    "QQ弹弹大喷菇",
    "寒冰地刺",
    "土杨桃",
    "精灵菇",
    "川菜投手",
    "坚果模仿者",
    "窝瓜坚果",
    "冰冻坚果",
    "头脑风暴",
    "宝藏吞噬者",
    "全息卡牌投影",
    "成长咖啡豆",
    "寒光菇",
    "骄阳豌豆射手",
    "荧光木槌",
    "狂野机枪射手",
    "生命重塑者",
    "双生樱桃",
    "幸运四叶草",
    "黄金向日葵",
    "土豆加农炮",
    "惩戒牢笼",
    "备用物资",
    "地刺大嘴花",
    "僵尸豆",
    "禁忌毁灭菇",
    "消消乐糖果",
    "海冰菇",
    "莲叶壳",
    "小猫向日葵",
    "礼盒机",
    "招财猫",
    "水晶蜗牛",
    "坚果存钱罐",
    "吸金磁射手",
    "钻石种子",
    "抽奖盒子豪华版",
    "炫彩杨桃",
    "坚果保龄球",
    "进化豆",
    "流星",
    "苹果闹钟",
    "海豌豆",
    "豌豆海草",
    "海洋星",
    "套盒坚果",
    "鱼饵菇",
    "花盆睡莲",
    "忧郁菇投手",
    "受伤的向日葵",
    "医用咖啡豆",
    "受伤的大喷菇",
    "寒冰加农炮",
    "黄金西瓜投手",
    "寒冰菇王",
    "自费盒子",
    "内卷投手",
    "制冰豆",
    "伪装的向日葵",
    "骄阳玉米投手",
    "辣椒重塑者",
    "棱镜向日葵",
    "大王钢齿花",
    "促销豆",
    "促销坚果",
    "促销花盆",
    "天使向日葵",
    "回收高坚果",  # 161
    "彩虹糖果",  # 162
    "百变高坚果",  # 163
    "逆时闹钟",  # 164
    "阳光加农炮",  # 165
    "禁忌寒冰菇",  # 166
]
for _ in range(len(plantsType), 256):
    plantsType.append("占位")
plantsType = plantsType + [
    "普僵",
    "旗帜",
    "路障",
    "撑杆",
    "铁桶",
    "冰车二爷",
    "铁门",
    "黑橄榄",
    "武装舞王",
    "舞伴",
    "泳圈普僵",
    "潜水",
    "冰车巨人",
    "雪橇",
    "海豚豌豆骑士",
    "小丑",
    "气球舞王",
    "矿工",
    "跳跳",
    "冰车雪人",
    "飞贼",
    "扶梯",
    "篮球",
    "巨人",
    "小鬼",
    "僵王",
    "豌豆僵尸",
    "坚果僵尸",
    "辣椒僵尸",
    "机枪僵尸",
    "冰窝瓜僵尸",
    "高冰果僵尸",
    "红眼",
    "迪斯科",
    "舞者",
    "骷髅",
    "死灵法师",
    "火焰迪斯科",
    "火焰舞者",
    "小黄鸭僵尸",
    "床车僵尸",
    "小摔哥僵尸",
    "橄榄巨人",
    "橄榄小鬼",
    "雪人矿工",
    "狂野机枪僵尸",
    "火炬坚果僵尸",
    "机枪撑杆僵尸",
    "机枪海豚僵尸",
    "僵尸坚果巨人",
    "僵尸豌豆小鬼",
    "鲨鱼僵尸",
    "寒冰射手僵尸",
    "海妖僵尸",
    "缠绕潜水僵尸",
    "钻石僵尸",
    "防爆门僵尸",
    "骑鸭僵尸",
    "小推车小鬼僵尸",
    "罐子僵尸",  # 315
    "催眠师僵尸",  # 316
    "园丁僵尸",  # 317
    "红眼舞王",  # 318
    "巨人伴舞",  # 319
]

ExcludedPutCards = [
    "阳光豆",
    "墓碑埋雷者",
    "豌豆睡莲",
    "毁灭海草",
    "随机植物盒子",
    "毁灭加农炮",
    "宝藏吞噬者",
    "全息卡牌投影",
    "成长咖啡豆",
    "荧光木槌",
    "生命重塑者",
    "幸运四叶草",
    "黄金向日葵",
    "土豆加农炮",
    "备用物资",
    "僵尸豆",
    "莲叶壳",
    "抽奖盒子豪华版",
    "坚果保龄球",
    "进化豆",
    "医用咖啡豆",
    "寒冰加农炮",
    "黄金西瓜投手",
    "自费盒子",
    "制冰豆",
    "促销豆",
    "阳光豆",
    "咖啡伞",
    "豌豆许愿池",
    "天使向日葵",
    "阳光加农炮",
]
DownPlantCards = [
    "小盆菇",
    "阳光花盆",
    "猫砂盆",
    "花盆睡莲",
    "促销花盆",
]
PumpkinPlantCards = [
    "忧郁南瓜头",
    "阳光南瓜掌",
    "烈火南瓜头",
]
AshPlantCards = [
    "阳光炸弹",
    "雪花寒冰菇",
    "魅惑毁灭菇",
    "樱桃辣椒",
    "仙人三叶草",
    "寒冰三叶草",
    "黄油JOKER",
    "大蒜辣椒",
    "魅惑菇射手",
    "头脑风暴",
    "寒光菇",
    "双生樱桃",
    "惩戒牢笼",
    "禁忌毁灭菇",
    "消消乐糖果",
    "流星",
    "苹果闹钟",
    "寒冰菇王",
    "辣椒重塑者",
    "彩虹糖果",
    "逆时闹钟",
    "禁忌寒冰菇",
]


def get_zombies_HP_addresses(PVZ_version):
    print("PVZ_version", PVZ_version)
    if PVZ_version == 2.0:
        return {
            "普僵": 0x005227BB,
            "路障的路障": 0x522892,
            "路障的绿帽": 0x0085A8AF,
            "撑杆": 0x522CBF,
            "撑杆的坚果": 0x0085AA02,
            "铁桶的铁桶": 0x52292B,
            "报纸": 0x52337D,
            "冰车二爷": 0x0085ADCD,
            "铁门的铁门": 0x522949,
            "铁门的路障": 0x0085A0CD,
            "铁门的铁桶": 0x0085A080,
            "橄榄的黑橄榄帽": 0x522BB0,
            "橄榄的废稿头盔": 0x85A794,
            "舞王": 0x523530,
            "舞王的黑橄榄帽": 0x0085A501,
            "舞王的废稿头盔": 0x0085A56D,
            "潜水和投篮的黑橄榄帽": 0x0085A025,
            "大型冰车": 0x522DE1,
            "雪橇车": 0x523139,
            "雪橇小队": 0x0085AB94,
            "海豚": 0x522D64,
            "海豚的路障": 0x0085A6FD,
            "小丑": 0x522FC7,
            "小丑的路障": 0x0085A0EA,
            "气球": 0x005234BF,
            "矿工的橄榄帽": 0x522BEF,
            "矿工本体": 0x0085A6C3,
            "跳跳": 0x523300,
            "跳跳的铁桶": 0x0085A1EC,
            "跳跳的坚果": 0x0085A326,
            "冰车雪人": 0x52296E,
            "蹦极": 0x522A1B,
            "扶梯本体和扶梯": 0x52299C,
            "扶梯的路障": 0x0085A347,
            "扶梯的铁桶": 0x0085A39E,
            "扶梯的坚果": 0x0085A4E0,
            "投石车": 0x522E8D,
            "白眼": 0x523D26,
            "红眼": 0x523E4A,
            "巨人的铁门": 0x0085A5CE,
            "巨人的铁桶": 0x0085A5BA,
            "巨人的黑橄榄帽": 0x0085A6B0,
            "巨人的废稿头盔": 0x0085A656,
            "植物僵尸的铁门": 0x0085A1C6,
            "植物僵尸的路障": 0x0085A1A4,
            "植物僵尸的铁桶": 0x0085A156,
            "坚果僵尸的坚果": 0x52382B,
            "辣椒僵尸的辣椒": 0x523A87,
            "高冰果僵尸的高冰果": 0x52395D,
            "迪斯科僵尸": 0x0085A82D,
            "骷髅": 0x0085AB76,
            "死灵法师": 0x0085ADB2,
            "火焰迪斯科": 0x0085AC14,
            "火焰舞者": 0x0085AD96,
            "床车": 0x0085AE77,
            "小摔哥的睡帽": 0x0085AEC7,
            "小黄鸭的路障": 0x0085AE63,
            "小黄鸭的铁桶": 0x0085AE30,
            "僵王": 0x0085AEE5,
        }
    elif PVZ_version == 2.1 or PVZ_version == 2.2:
        return {
            "普僵": 0x005227BB,
            "路障的路障": 0x00522892,
            "路障的绿帽": 0x008D08AF,
            "路尸的绿帽上限": 0x008D08B9,
            "撑杆": 0x00522CBF,
            "撑杆的坚果": 0x008D0A02,
            "铁桶的铁桶": 0x0052292B,
            "报纸": 0x0052337D,
            "冰车二爷": 0x008D0DCD,
            "铁门的铁门": 0x00522949,
            "铁门的路障": 0x008D00CD,
            "铁门的铁桶": 0x008D0080,
            "橄榄的黑橄榄帽": 0x00522BB0,
            "橄榄的废稿头盔": 0x008D0794,
            "橄榄的废稿头盔上限": 0x008D079E,
            "舞王": 0x00523530,
            "舞王的黑橄榄帽": 0x008D0501,
            "舞王的废稿头盔": 0x008D056D,
            "舞王的废稿头盔上限": 0x008D0577,
            "潜水和投篮的黑橄榄帽": 0x008D0025,
            "大型冰车": 0x00522DE1,
            "雪橇车": 0x00523139,
            "雪橇小队": 0x008D0B94,
            "雪橇小队上限": 0x008D0B9E,
            "海豚": 0x00522D64,
            "海豚的路障": 0x008D06FD,
            "小丑": 0x00522FC7,
            "小丑的路障": 0x008D00EA,
            "气球": 0x005234BF,
            "矿工本体": 0x008D06C3,
            "跳跳": 0x00523300,
            "跳跳的铁桶": 0x008D01EC,
            "跳跳的坚果": 0x008D0326,
            "冰车雪人": 0x0052296E,
            "蹦极": 0x00522A1B,
            "扶梯本体和扶梯": 0x0052299C,
            "扶梯僵尸的路障饰品": 0x008D0347,
            "扶梯的路障": 0x008D039E,
            "扶梯的坚果": 0x008D04E0,
            "投石车": 0x00522E8D,
            "白眼": 0x00523D26,
            "红眼": 0x00523E4A,
            "巨人的铁门": 0x008D05CE,
            "巨人的铁桶": 0x008D05BA,
            "巨人的黑橄榄帽": 0x008D06B0,
            "巨人的废稿头盔": 0x008D0656,
            "巨人的废稿头盔上限": 0x008D0660,
            "植物僵尸的铁门": 0x008D01C6,
            "植物僵尸的路障": 0x008D01A4,
            "植物僵尸的铁桶": 0x008D0156,
            "坚果僵尸的坚果": 0x0052382B,
            "辣椒僵尸的辣椒": 0x00523A87,
            "高冰果僵尸的高冰果": 0x0052395D,
            "迪斯科僵尸": 0x008D082D,
            "骷髅": 0x008D0B76,
            "骷髅上限": 0x008D0B80,
            "死灵法师": 0x008D0DB2,
            "火焰迪斯科": 0x008D0C14,
            "火焰舞者": 0x008D0D96,
            "床车": 0x008D0E77,
            "小摔哥的睡帽": 0x008D0EC7,
            "小摔哥的睡帽上限": 0x008D0ED1,
            "小黄鸭的路障": 0x008D0E63,
            "小黄鸭的铁桶": 0x008D0E30,
            "僵王": 0x008D0EE5,
            "橄榄巨人": 0x008D0F04,
            "橄榄巨人头盔": 0x008D0F18,
            "橄榄小鬼头盔": 0x008D0F8F,
            "雪人矿工": 0x008D0FA3,
            "雪人矿工帽": 0x008D0FC9,
        }
    elif PVZ_version == 2.3:
        return {
            "普僵": 0x005227BB,
            "路障的路障": 0x00522892,
            "路障的绿帽": 0x008D08AA,
            "撑杆": 0x00522CBF,
            "撑杆的坚果": 0x008D09FD,
            "铁桶的铁桶": 0x0052292B,
            "报纸": 0x0052337D,
            "冰车二爷": 0x008D0DAE,
            "铁门的铁门": 0x00522949,
            "铁门的路障": 0x008D00CD,
            "铁门的铁桶": 0x008D0080,
            "橄榄的黑橄榄帽": 0x00522BB0,
            "橄榄的废稿头盔": 0x008D078F,
            "舞王": 0x00523530,
            "舞王的黑橄榄帽": 0x008D04E5,
            "舞王的废稿头盔": 0x008D0551,
            "潜水和投篮的黑橄榄帽": 0x008D0025,
            "大型冰车": 0x00522DE1,
            "雪橇车": 0x00523139,
            "雪橇小队": 0x008D0B75,
            "海豚": 0x00522D64,
            "海豚的路障": 0x008D06E1,
            "小丑": 0x00522FC7,
            "小丑的路障": 0x008D00EA,
            "气球": 0x005234BF,
            "矿工本体": 0x008D06A7,
            "跳跳": 0x00523300,
            "跳跳的铁桶": 0x008D01EC,
            "跳跳的坚果": 0x008D0318,
            "冰车雪人": 0x0052296E,
            "蹦极": 0x00522A1B,
            "扶梯本体和扶梯": 0x0052299C,
            "扶梯僵尸的铁桶": 0x008D0390,
            "扶梯的路障": 0x008D0339,
            "扶梯的坚果": 0x008D04C4,
            "投石车": 0x00522E8D,
            "投石车橄榄帽": 0x008D0025,
            "白眼": 0x00523D26,
            "红眼": 0x00523E4A,
            "巨人的铁门": 0x008D05B2,
            "巨人的铁桶": 0x008D059E,
            "巨人的黑橄榄帽": 0x008D0694,
            "巨人的废稿头盔": 0x008D063A,
            "小鬼": 0x005227BB,
            "植物僵尸本体": 0x005227BB,
            "植物僵尸的铁门": 0x008D01C6,
            "植物僵尸的路障": 0x008D01A4,
            "植物僵尸的铁桶": 0x0052292B,
            "坚果僵尸的坚果": 0x0052382B,
            "辣椒僵尸的辣椒": 0x00523A87,
            "高冰果僵尸的高冰果": 0x008D11D1,
            "机枪射手僵尸": 0x008D11A2,
            "火炬坚果僵尸的坚果头": 0x008D12EC,
            "机枪撑杆僵尸": 0x008D1415,
            "机枪海豚僵尸的路障": 0x008D164F,
            "迪斯科僵尸": 0x008D0828,
            "骷髅": 0x008D0B57,
            "死灵法师": 0x008D0D93,
            "火焰迪斯科": 0x008D0BF5,
            "火焰舞者": 0x008D0D77,
            "床车": 0x008D0E58,
            "小摔哥的睡帽": 0x008D0EA8,
            "小黄鸭的路障": 0x008D0E44,
            "小黄鸭的铁桶": 0x008D0E11,
            "僵王": 0x008D0EC6,
            "橄榄巨人": 0x008D0F01,
            "橄榄巨人头盔": 0x008D0F15,
            "橄榄小鬼": 0x005227BB,
            "橄榄小鬼头盔": 0x008D0F8C,
            "雪人矿工": 0x008D0FC6,
            "雪人矿工帽": 0x008D0FA0,
            "钻石僵尸帽": 0x008D1DF7,
            "鲨鱼僵尸": 0x008D1A97,
            "海妖僵尸": 0x008D1C4D,
            "缠绕潜水僵尸": 0x008D1CDA,
        }
    elif PVZ_version == 2.35 or PVZ_version >= 2.36:
        return {
            "普僵": 0x005227BB,
            "路障的路障": 0x00522892,
            "路障的绿帽": 0x008D08AA,
            "撑杆": 0x00522CBF,
            "撑杆的坚果": 0x008D09FD,
            "铁桶的铁桶": 0x0052292B,
            "报纸": 0x0052337D,
            "冰车二爷": 0x008D0DAE,
            "铁门的铁门": 0x00522949,
            "铁门的路障": 0x008D00CD,
            "铁门的铁桶": 0x008D0080,
            "橄榄的黑橄榄帽": 0x00522BB0,
            "橄榄的废稿头盔": 0x008D078F,
            "舞王": 0x00523530,
            "舞王的黑橄榄帽": 0x008D04E5,
            "舞王的废稿头盔": 0x008D0551,
            "潜水和投篮的黑橄榄帽": 0x008D0025,
            "大型冰车": 0x00522DE1,
            "雪橇车": 0x00523139,
            "雪橇小队": 0x008D0B75,
            "海豚": 0x00522D64,
            "海豚的路障": 0x008D06E1,
            "小丑": 0x00522FC7,
            "小丑的路障": 0x008D00EA,
            "气球": 0x005234BF,
            "矿工本体": 0x008D06A7,
            "跳跳": 0x00523300,
            "跳跳的铁桶": 0x008D01EC,
            "跳跳的坚果": 0x008D0318,
            "冰车雪人": 0x0052296E,
            "蹦极": 0x00522A1B,
            "扶梯本体和扶梯": 0x0052299C,
            "扶梯僵尸的铁桶": 0x008D0390,
            "扶梯的路障": 0x008D0339,
            "扶梯的坚果": 0x008D04C4,
            "投石车": 0x00522E8D,
            "投石车橄榄帽": 0x008D0025,
            "白眼": 0x00523D26,
            "红眼": 0x00523E4A,
            "巨人的铁门": 0x008D05B2,
            "巨人的铁桶": 0x008D059E,
            "巨人的黑橄榄帽": 0x008D0694,
            "巨人的废稿头盔": 0x008D063A,
            "小鬼": 0x005227BB,
            "植物僵尸本体": 0x005227BB,
            "植物僵尸的铁门": 0x008D01C6,
            "植物僵尸的路障": 0x008D01A4,
            "植物僵尸的铁桶": 0x0052292B,
            "坚果僵尸的坚果": 0x0052382B,
            "辣椒僵尸的辣椒": 0x00523A87,
            "高冰果僵尸的高冰果": 0x008D11D1,
            "机枪射手僵尸": 0x008D11A2,
            "火炬坚果僵尸的坚果头": 0x008D12EC,
            "机枪撑杆僵尸": 0x008D1415,
            "机枪海豚僵尸的路障": 0x008D164F,
            "迪斯科僵尸": 0x008D0828,
            "骷髅": 0x008D0B57,
            "死灵法师": 0x008D0D93,
            "火焰迪斯科": 0x008D0BF5,
            "火焰舞者": 0x008D0D77,
            "床车": 0x008D0E58,
            "小摔哥的睡帽": 0x008D0EA8,
            "小黄鸭的路障": 0x008D0E44,
            "小黄鸭的铁桶": 0x008D0E11,
            "僵王": 0x008D0EDA,
            "橄榄巨人": 0x008D0F01,
            "橄榄巨人头盔": 0x008D0F15,
            "橄榄小鬼": 0x005227BB,
            "橄榄小鬼头盔": 0x008D0F8C,
            "雪人矿工": 0x008D0FC6,
            "雪人矿工帽": 0x008D0FA0,
            "钻石僵尸帽": 0x008D1DF7,
            "鲨鱼僵尸": 0x008D1A97,
            "海妖僵尸": 0x008D1C4D,
            "缠绕潜水僵尸": 0x008D1CDA,
        }


plants_HP_addresses = {
    "一般植物": 0x00844DBF,
    "火炬坚果/磁力坚果/西瓜坚果": 0x0045E1A7,
    "雪花寒冰菇/汉堡射手/影流窝瓜王/黄油JOKER/大蒜辣椒": 0x00844DCB,
    "豌豆许愿池": 0x00844DD7,
    "高冰果": 0x0045E215,
    "海坚果": 0x00850008,
    "豌豆大炮": 0x008502A6,
    "忧郁南瓜头/阳光南瓜掌/烈火南瓜头/生命重塑者/莲叶壳": 0x0045E445,
    "魅惑大蒜": 0x0045E242,
    "钢刺坚果王": 0x0045E5C3,
    "毁灭加农炮": 0x00850296,
    "爆炸坚果": 0x0045E1BA,
    "巨大坚果": 0x0045E207,
    "火爆坚果墙": 0x00850357,
    "热狗射手": 0x00850057,
    "向日葵女王": 0x008500BA,
    "至尊VIP坚果": 0x008500E6,
    "至尊VIP坚果长大增加的血量": 0x00867E73,
    "僵尸坚果墙": 0x00850112,
    "Cupid魅惑菇射手": 0x00850130,
    "财神金盏花": 0x00850155,
    "坑洞坚果": 0x00850165,
    "窝瓜坚果": 0x008501AC,
    "窝瓜坚果临界血量": 0x008491AB + 3,  # 注意这里的地址需要加上偏移量
    "冰冻坚果": 0x008501BC,
}

# plantPutType = [
#     "豌豆向日葵",
#     "阳光豆",
#     "阳光炸弹",
#     "火炬坚果",
#     "阳光土豆雷",
#     "寒冰香蒲",
#     "大蒜花",
#     "双发仙人掌",
#     "小盆菇",
#     "阳光向日葵",
#     "冰瓜大喷菇",
#     "墓碑埋雷者",
#     "红眼菇",
#     "阳光胆小菇",
#     "雪花寒冰菇",
#     "魅惑毁灭菇",
#     "豌豆睡莲",
#     "冰菇窝瓜",
#     "豌豆许愿池",
#     "毁灭海草",
#     "樱桃辣椒",
#     "黄油地刺",
#     "冰炬树桩",
#     "高冰果",
#     "海坚果",
#     "6号路灯花",
#     "豌豆大炮",
#     "仙人三叶草",
#     "玉米卷香蒲",
#     "地刺杨桃",
#     "忧郁南瓜头",
#     "磁力坚果",
#     "机枪卷心菜投手",
#     "阳光花盆",
#     "三线玉米投手",
#     "随机植物盒子",
#     "魅惑大蒜",
#     "咖啡伞",
#     "仙人三叶花",
#     "西瓜坚果",
#     "汉堡射手",
#     "阳光南瓜掌",
#     "黄油忧郁菇",
#     "西瓜香蒲",
#     "阳光菇投手",
#     "金盏吸金磁",
#     "钢刺坚果王",
#     "毁灭加农炮",
#     "模仿者",
#     "爆炸坚果",
#     "巨大坚果",
#     "芽",
#     "火爆地雷",
#     "火爆坚果墙",
#     "豌豆香蒲",
#     "冰瓜香蒲",
#     "烈火南瓜头",
#     "僵尸豌豆射手",
#     "寒冰三叶草",
#     "热狗射手",
#     "寒冰仙人掌",
#     "影流窝瓜王",
#     "黄油JOKER",
#     "向日葵女王",
#     "大蒜辣椒",
#     "至尊VIP坚果",
#     "僵尸坚果墙",
#     "魅惑菇射手",
#     "财神金盏花",
#     "猫砂盆",
#     "坑洞坚果",
#     "QQ弹弹大喷菇",
#     "寒冰地刺",
#     "土杨桃",
#     "精灵菇",
#     "川菜投手",
#     "坚果模仿者",
#     "窝瓜坚果",
#     "冰冻坚果",
#     "头脑风暴",
#     "宝藏吞噬者",
#     "全息卡牌投影",
#     "成长咖啡豆",
#     "寒光菇",
#     "骄阳豌豆射手",
#     "荧光木槌",
#     "狂野机枪射手",
#     "生命重塑者",
#     "双生樱桃",
#     "幸运四叶草",
#     "黄金向日葵",
#     "土豆加农炮",
#     "惩戒牢笼",
#     "备用物资",
#     "地刺大嘴花",
#     "僵尸豆",
#     "禁忌毁灭菇",
#     "消消乐糖果",
#     "海冰菇",
#     "莲叶壳",
#     "小猫向日葵",
# ]
goldPlant = [
    "高冰果",
    "豌豆大炮",
    "忧郁南瓜头",
    "汉堡射手",
    "黄油忧郁菇",
    "西瓜香蒲",
    "钢刺坚果王",
    "毁灭加农炮",
    "冰瓜香蒲",
    "热狗射手",
    "向日葵女王",
    "至尊VIP坚果",
    "狂野机枪射手",
    "寒冰加农炮",
    "黄金西瓜投手",
]
goldPlantIndex = [23, 26, 30, 40, 42, 43, 46, 47, 78, 82, 86, 88, 109]
mushroomPlant = [
    8,
    9,
    10,
    12,
    13,
    14,
    15,
    17,
    23,
    24,
    30,
    31,
    40,
    42,
    44,
    47,
    83,
    90,
    94,
    97,
    106,
    119,
    121,
]
peaPlant = [0, 16, 18, 26, 32, 40, 77, 80, 82, 107, 109]
melonPlant = [10, 39, 43, 78]
flowerPlant = [0, 2, 9, 86, 123]
bulletType = [
    "豌豆",
    "冰豌豆",
    "卷心菜",
    "西瓜",
    "孢子",
    "冰西瓜",
    "火球(隐形)",
    "星星",
    "仙人掌刺",
    "篮球",
    "玉米粒",
    "毁灭菇",
    "黄油",
    "僵尸豌豆",
    "小阳光菇",
    "大阳光菇",
    "黑色豌豆",
    "寒冰刺",
    "魅惑箭",
    "银币",
    "金币",
    "钻石",
    "土豆雷",
    "川菜",
    "辣椒",
    "白火球",
    "土豆加农炮(无伤害)",
    "冰孢子",
    "小阳光",
    "豌豆僵尸的火豌豆1",
    "豌豆僵尸的火豌豆2",
    "黄金豌豆",
    "大型豌豆",
    "大型火焰豌豆",
    "大型冰焰豌豆",
    "冰焰豌豆",
    "星星",
    "大星星",
    "黄金豌豆2",
    "冰星星",
    "忧郁菇投手",
    "冰大炮",
    "黄金瓜",
    "火玉米",
]
keyTpye = [
    "无",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "小0",
    "小1",
    "小2",
    "小3",
    "小4",
    "小5",
    "小6",
    "小7",
    "小8",
    "小9",
    "小*",
    "小+",
    "小-",
    "小.",
    "小\\",
    "F1",
    "F2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "F9",
    "F10",
    "F11",
    "F12",
    "~",
]

keyCode = [
    "",
    0x30,
    0x31,
    0x32,
    0x33,
    0x34,
    0x35,
    0x36,
    0x37,
    0x38,
    0x39,
    0x41,
    0x42,
    0x43,
    0x44,
    0x45,
    0x46,
    0x47,
    0x48,
    0x49,
    0x4A,
    0x4B,
    0x4C,
    0x4D,
    0x4E,
    0x4F,
    0x50,
    0x51,
    0x52,
    0x53,
    0x54,
    0x55,
    0x56,
    0x57,
    0x58,
    0x59,
    0x5A,
    0x60,
    0x61,
    0x62,
    0x63,
    0x64,
    0x65,
    0x66,
    0x67,
    0x68,
    0x69,
    0x6A,
    0x6B,
    0x6D,
    0x6E,
    0x6F,
    0x70,
    0x71,
    0x72,
    0x73,
    0x74,
    0x75,
    0x76,
    0x77,
    0x78,
    0x79,
    0x7A,
    0x7B,
    0xC0,
]


class plant:
    def __init__(self, addr):
        self.addr = addr
        self.no = PVZ_memory.read_ushort(self.addr + 0x148)
        self.exist = PVZ_memory.read_bool(self.addr + 0x141)
        self.x = PVZ_memory.read_int(self.addr + 0x8)
        self.y = PVZ_memory.read_int(self.addr + 0xC)
        self.row = PVZ_memory.read_int(self.addr + 0x1C)
        self.col = PVZ_memory.read_int(self.addr + 0x28)
        self.type = PVZ_memory.read_int(self.addr + 0x24)
        # 2c 抖动倒计时
        # 30 抖动动画索引
        self.state = PVZ_memory.read_int(self.addr + 0x3C)
        self.hp = PVZ_memory.read_int(self.addr + 0x40)  # 血量
        self.maxhp = PVZ_memory.read_int(self.addr + 0x44)
        self.dieTime = PVZ_memory.read_int(self.addr + 0x4C)
        self.cinderTime = PVZ_memory.read_int(self.addr + 0x50)
        self.effectTime = PVZ_memory.read_int(self.addr + 0x54)  # 阳光豆长大
        self.productTime = PVZ_memory.read_int(self.addr + 0x58)  # 常规攻击
        self.productInterval = PVZ_memory.read_int(self.addr + 0x5C)  # 常规攻击间隔
        self.attackTime = PVZ_memory.read_int(self.addr + 0x90)
        self.sunTime = PVZ_memory.read_int(self.addr + 0xDC)
        self.humTime = PVZ_memory.read_int(self.addr + 0x128)  # 阳光生产
        self.mushroomTime = PVZ_memory.read_int(self.addr + 0x130)
        self.isVisible = PVZ_memory.read_bool(self.addr + 0x18)
        self.isSquash = PVZ_memory.read_bool(self.addr + 0x142)
        self.isSleep = PVZ_memory.read_bool(self.addr + 0x143)
        self.isLight = PVZ_memory.read_bool(self.addr + 0x145)
        self.isAttack = PVZ_memory.read_int(self.addr + 0x48)

    def setExist(self, exist):
        PVZ_memory.write_bool(self.addr + 0x141, exist)

    def setX(self, x):
        PVZ_memory.write_int(self.addr + 0x8, x)

    def setY(self, y):
        PVZ_memory.write_int(self.addr + 0xC, y)

    def setRow(self, row):
        PVZ_memory.write_int(self.addr + 0x1C, row)

    def setCol(self, col):
        PVZ_memory.write_int(self.addr + 0x28, col)

    def setType(self, type):
        PVZ_memory.write_int(self.addr + 0x24, type)

    def setState(self, state):
        PVZ_memory.write_int(self.addr + 0x3C, state)

    def setHP(self, hp):
        PVZ_memory.write_int(self.addr + 0x40, hp)
        PVZ_memory.write_int(self.addr + 0x44, hp)

    def setDieTime(self, dieTime):
        PVZ_memory.write_int(self.addr + 0x4C, dieTime)

    def setCinderTime(self, cinderTime):
        PVZ_memory.write_int(self.addr + 0x50, cinderTime)

    def setEffectTime(self, effectTime):
        PVZ_memory.write_int(self.addr + 0x54, effectTime)

    def setProductTime(self, productTime):
        PVZ_memory.write_int(self.addr + 0x58, productTime)

    def setAttackTime(self, attackTime):
        PVZ_memory.write_int(self.addr + 0x90, attackTime)

    def setProductInterval(self, productInterval):
        PVZ_memory.write_int(self.addr + 0x5C, productInterval)

    def setSunTime(self, sunTime):
        PVZ_memory.write_int(self.addr + 0xDC, sunTime)

    def setHumTime(self, humTime):
        PVZ_memory.write_int(self.addr + 0x12C, humTime)

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
        self.no = PVZ_memory.read_ushort(self.addr + 0x158)
        self.exist = PVZ_memory.read_int(self.addr + 0xEC)
        self.row = PVZ_memory.read_int(self.addr + 0x1C) + 1
        self.type = PVZ_memory.read_int(self.addr + 0x24)
        self.x = PVZ_memory.read_float(self.addr + 0x2C)
        self.y = PVZ_memory.read_float(self.addr + 0x30)
        self.size = PVZ_memory.read_float(self.addr + 0x11C)
        self.state = PVZ_memory.read_int(self.addr + 0x28)
        self.hp = PVZ_memory.read_int(self.addr + 0xC8)
        self.maxHP = PVZ_memory.read_int(self.addr + 0xCC)
        self.hatType = PVZ_memory.read_int(self.addr + 0xC4)
        self.hatHP = PVZ_memory.read_int(self.addr + 0xD0)
        self.maxHatHP = PVZ_memory.read_int(self.addr + 0xD4)
        self.doorType = PVZ_memory.read_int(self.addr + 0xD8)
        self.doorHP = PVZ_memory.read_int(self.addr + 0xDC)
        self.maxDoorHP = PVZ_memory.read_int(self.addr + 0xE0)
        self.slow = PVZ_memory.read_int(self.addr + 0xAC)
        self.butter = PVZ_memory.read_int(self.addr + 0xB0)
        self.frozen = PVZ_memory.read_int(self.addr + 0xB4)
        self.isVisible = PVZ_memory.read_bool(self.addr + 0x18)
        self.isEating = PVZ_memory.read_bool(self.addr + 0x51)
        self.isHpynotized = PVZ_memory.read_bool(self.addr + 0xB8)
        self.isBlow = PVZ_memory.read_bool(self.addr + 0xB9)
        self.isDying = PVZ_memory.read_bool(self.addr + 0xBA)
        self.isGarlic = PVZ_memory.read_bool(self.addr + 0xBF)
        self.stolenPlant = PVZ_memory.read_ushort(self.addr + 0x128)

    def setRow(self, row):
        PVZ_memory.write_int(self.addr + 0x1C, row - 1)

    def setX(self, x):
        PVZ_memory.write_float(self.addr + 0x2C, x)

    def setY(self, y):
        PVZ_memory.write_float(self.addr + 0x30, y)

    def setSize(self, size):
        PVZ_memory.write_float(self.addr + 0x11C, size)

    def setState(self, state):
        PVZ_memory.write_int(self.addr + 0x28, state)

    def setHP(self, hp):
        PVZ_memory.write_int(self.addr + 0xC8, hp)
        PVZ_memory.write_int(self.addr + 0xCC, hp)

    def setHatHP(self, hatHP):
        PVZ_memory.write_int(self.addr + 0xD0, hatHP)
        PVZ_memory.write_int(self.addr + 0xD4, hatHP)

    def setDoorHP(self, doorHP):
        PVZ_memory.write_int(self.addr + 0xDC, doorHP)
        PVZ_memory.write_int(self.addr + 0xE0, doorHP)

    def setSlow(self, slow):
        PVZ_memory.write_int(self.addr + 0xAC, slow)

    def setButter(self, butter):
        PVZ_memory.write_int(self.addr + 0xB0, butter)

    def setFrozen(self, frozen):
        PVZ_memory.write_int(self.addr + 0xB4, frozen)

    def setExist(self, exist):
        PVZ_memory.write_int(self.addr + 0xEC, exist)

    def setIsVisible(self, isVisible):
        PVZ_memory.write_bool(self.addr + 0x18, isVisible)

    def setIsEating(self, isEating):
        PVZ_memory.write_bool(self.addr + 0x51, isEating)

    def setIsHPynotized(self, isHPynotized):
        PVZ_memory.write_bool(self.addr + 0xB8, isHPynotized)

    def setIsBlow(self, isBlow):
        PVZ_memory.write_bool(self.addr + 0xB9, isBlow)

    def setIsDying(self, isDying):
        PVZ_memory.write_bool(self.addr + 0xBA, isDying)

    def setIsGarlic(self, isGarlic):
        PVZ_memory.write_bool(self.addr + 0xBF, isGarlic)

    def setStolenPlant(self, stolenPlant):
        PVZ_memory.write_ushort(self.addr + 0x128, stolenPlant)


class item:
    def __init__(self, addr):
        self.addr = addr
        self.no = PVZ_memory.read_ushort(self.addr + 0xE8)
        self.exist = PVZ_memory.read_bool(self.addr + 0x20)
        self.row = PVZ_memory.read_int(self.addr + 0x14) + 1
        self.col = PVZ_memory.read_int(self.addr + 0x10) + 1
        self.type = PVZ_memory.read_int(self.addr + 0x8)
        self.time = PVZ_memory.read_int(self.addr + 0x18)
        self.vase_skin = PVZ_memory.read_int(self.addr + 0xC)
        self.vase_zombie = PVZ_memory.read_int(self.addr + 0x3C)
        self.vase_plant = PVZ_memory.read_int(self.addr + 0x40)
        self.vase_type = PVZ_memory.read_int(self.addr + 0x44)
        self.vase_sun = PVZ_memory.read_int(self.addr + 0x50)
        self.vase_see_time = PVZ_memory.read_int(self.addr + 0x4C)

    def setExist(self, exist):
        PVZ_memory.write_bool(self.addr + 0x20, exist)

    def setRow(self, row):
        PVZ_memory.write_int(self.addr + 0x14, row - 1)

    def setCol(self, col):
        PVZ_memory.write_int(self.addr + 0x10, col - 1)

    def setTime(self, time):
        PVZ_memory.write_int(self.addr + 0x18, time)

    def setVaseSkin(self, vase_skin):
        PVZ_memory.write_int(self.addr + 0xC, vase_skin)

    def setVaseZombie(self, vase_zombie):
        PVZ_memory.write_int(self.addr + 0x3C, vase_zombie)

    def setVasePlant(self, vase_plant):
        PVZ_memory.write_int(self.addr + 0x40, vase_plant)

    def setVaseType(self, vase_type):
        PVZ_memory.write_int(self.addr + 0x44, vase_type)

    def setVaseSun(self, vase_sun):
        PVZ_memory.write_int(self.addr + 0x50, vase_sun)

    def setVaseSeeTime(self, vase_see_time):
        PVZ_memory.write_int(self.addr + 0x4C, vase_see_time)


class car:
    def __init__(self, addr):
        self.addr = addr
        self.exist = PVZ_memory.read_bool(self.addr + 0x30)
        self.no = PVZ_memory.read_ushort(self.addr + 0x44)
        self.row = PVZ_memory.read_int(self.addr + 0x14)

    def setExist(self, exist):
        PVZ_memory.write_bool(self.addr + 0x30, exist)


class slot:
    def __init__(self, addr):
        self.addr = addr
        self.no = PVZ_memory.read_ushort(self.addr + 0x2C)
        self.canUse = PVZ_memory.read_bool(self.addr + 0x48)
        self.type = PVZ_memory.read_int(self.addr + 0x34)
        self.imitaterType = PVZ_memory.read_int(self.addr + 0x34)
        self.cooldown = PVZ_memory.read_int(self.addr + 0x28)
        self.elapsed = PVZ_memory.read_int(self.addr + 0x24)
        self.isVisible = PVZ_memory.read_bool(self.addr + 0x18)
        self.count = PVZ_memory.read_int(self.addr + 0x4C)

    def setCanUse(self, canUse):
        PVZ_memory.write_bool(self.addr + 0x48, canUse)

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
        PVZ_memory.write_int(self.addr + 0x4C, count)


class plantCharacteristic:
    def __init__(self, type):
        self.type = type
        if type < 256:
            self.addr = 0x007A2010 + type * 0x24
            self.sun = PVZ_memory.read_int(self.addr)
            self.cd = PVZ_memory.read_int(self.addr + 0x4)
            self.canAttack = PVZ_memory.read_bool(self.addr + 0x8)
            self.attackInterval = PVZ_memory.read_int(self.addr + 0xC)
        else:
            if PVZ_version == 2.0:
                self.addr = 0x008452C8 + type - 256
                self.sun = PVZ_memory.read_int(self.addr)
                self.cd = 0
                self.canAttack = True
                self.attackInterval = 0
            elif PVZ_version == 2.1 or PVZ_version == 2.2:
                self.addr = 0x0088B018 + type - 256
                self.sun = PVZ_memory.read_uchar(self.addr)
                self.cd = 0
                self.canAttack = True
                self.attackInterval = 0
            elif PVZ_version == 2.3:
                self.addr = 0x00088B04D + (type - 256) * 0x4
                self.sun = PVZ_memory.read_int(self.addr)
                self.cd = 0
                self.canAttack = True
                self.attackInterval = 0
            elif PVZ_version == 2.35 or PVZ_version == 2.36 or PVZ_version == 2.37:
                self.addr = 0x0088B05D + (type - 256) * 0x4
                self.sun = PVZ_memory.read_int(self.addr)
                self.cd = 0
                self.canAttack = True
                self.attackInterval = 0
            elif PVZ_version == 2.4:
                self.addr = 0x0088B072 + (type - 256) * 0x4
                self.sun = PVZ_memory.read_int(self.addr)
                self.cd = 0
                self.canAttack = True
                self.attackInterval = 0

    def setSun(self, sun):
        PVZ_memory.write_int(self.addr, sun)

    def setCd(self, cd):
        PVZ_memory.write_int(self.addr + 0x4, cd)

    def setCanAttack(self, canAttack):
        PVZ_memory.write_bool(self.addr + 0x8, canAttack)

    def setAttackInterval(self, attackInterval):
        PVZ_memory.write_int(self.addr + 0xC, attackInterval)


class zombieType:
    def __init__(self, type):
        self.type = type
        if PVZ_version < 2.3:
            if type <= 54:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_int(self.addr + 0x4)
                self.level = PVZ_memory.read_int(self.addr + 0x8)
                self.weight = PVZ_memory.read_int(self.addr + 0x14)
            elif type == 51:
                if PVZ_version == 2.0:
                    self.weight = PVZ_memory.read_uchar(0x0085A887)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    self.weight = PVZ_memory.read_uchar(0x008D0887)
            elif type == 52:
                if PVZ_version == 2.0:
                    self.weight = PVZ_memory.read_uchar(0x0085A75F)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    self.weight = PVZ_memory.read_uchar(0x008D075F)
            elif type == 53:
                if PVZ_version == 2.0:
                    self.weight = PVZ_memory.read_uchar(0x0085A538)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    self.weight = PVZ_memory.read_uchar(0x008D0538)
            elif type == 54:
                if PVZ_version == 2.0:
                    self.weight = PVZ_memory.read_uchar(0x0085A613)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    self.weight = PVZ_memory.read_uchar(0x008D0613)
        elif PVZ_version == 2.3:
            if type <= 55:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_int(self.addr + 0x4)
                self.level = PVZ_memory.read_int(self.addr + 0x8)
                self.weight = PVZ_memory.read_int(self.addr + 0x14)
            elif type == 56:
                self.weight = PVZ_memory.read_uchar(0x008D0882)
            elif type == 57:
                self.weight = PVZ_memory.read_uchar(0x008D0743)
            elif type == 58:
                self.weight = PVZ_memory.read_uchar(0x008D051C)
            elif type == 59:
                self.weight = PVZ_memory.read_uchar(0x008D05F7)
        elif PVZ_version == 2.35 or PVZ_version == 2.36 or PVZ_version == 2.37:
            if type <= 58:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_int(self.addr + 0x4)
                self.level = PVZ_memory.read_int(self.addr + 0x8)
                self.weight = PVZ_memory.read_int(self.addr + 0x14)
            elif type == 59:
                self.weight = PVZ_memory.read_uchar(0x008D0896)
            elif type == 60:
                self.weight = PVZ_memory.read_uchar(0x008D0743)
            elif type == 61:
                self.weight = PVZ_memory.read_uchar(0x008D051C)
            elif type == 62:
                self.weight = PVZ_memory.read_uchar(0x008D05F7)
        elif PVZ_version == 2.4:
            if type <= 63:
                self.addr = 0x007A6000 + type * 0x1C
                self.anime = PVZ_memory.read_int(self.addr + 0x4)
                self.level = PVZ_memory.read_int(self.addr + 0x8)
                self.weight = PVZ_memory.read_int(self.addr + 0x14)
            elif type == 64:
                self.weight = PVZ_memory.read_uchar(0x008D0896)
            elif type == 65:
                self.weight = PVZ_memory.read_uchar(0x008D0743)
            elif type == 66:
                self.weight = PVZ_memory.read_uchar(0x008D051C)
            elif type == 67:
                self.weight = PVZ_memory.read_uchar(0x008D05F7)

    def setAnime(self, anime):
        PVZ_memory.write_int(self.addr + 0x4, anime)

    def setLevel(self, level):
        PVZ_memory.write_int(self.addr + 0x4, level)

    def setWeight(self, weight):
        if PVZ_version < 2.3:
            if self.type <= 50:
                PVZ_memory.write_int(self.addr + 0x14, weight)
            elif self.type == 51:
                if PVZ_version == 2.0:
                    PVZ_memory.write_uchar(0x0085A887, weight)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    PVZ_memory.write_uchar(0x008D089E, weight)
            elif self.type == 52:
                if PVZ_version == 2.0:
                    PVZ_memory.write_uchar(0x0085A75F, weight)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    PVZ_memory.write_uchar(0x008D075F, weight)
            elif self.type == 53:
                if PVZ_version == 2.0:
                    PVZ_memory.write_uchar(0x0085A538, weight)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    PVZ_memory.write_uchar(0x008D0538, weight)
            elif self.type == 54:
                if PVZ_version == 2.0:
                    PVZ_memory.write_uchar(0x0085A613, weight)
                elif PVZ_version == 2.1 or PVZ_version == 2.2:
                    PVZ_memory.write_uchar(0x008D0613, weight)
        elif PVZ_version == 2.3:
            if self.type <= 55:
                PVZ_memory.write_int(self.addr + 0x14, weight)
            elif self.type == 56:
                PVZ_memory.write_uchar(0x008D0882, weight)
            elif self.type == 57:
                PVZ_memory.write_uchar(0x008D0743, weight)
            elif self.type == 58:
                PVZ_memory.write_uchar(0x008D051C, weight)
            elif self.type == 59:
                PVZ_memory.write_uchar(0x008D05F7, weight)
        elif PVZ_version == 2.35 or PVZ_version == 2.36 or PVZ_version == 2.37:
            if self.type <= 58:
                PVZ_memory.write_int(self.addr + 0x14, weight)
            elif self.type == 59:
                PVZ_memory.write_uchar(0x008D0896, weight)
            elif self.type == 60:
                PVZ_memory.write_uchar(0x008D0743, weight)
            elif self.type == 61:
                PVZ_memory.write_uchar(0x008D051C, weight)
            elif self.type == 62:
                PVZ_memory.write_uchar(0x008D05F7, weight)
        elif PVZ_version == 2.4:
            if self.type <= 63:
                PVZ_memory.write_int(self.addr + 0x14, weight)
            elif self.type == 64:
                PVZ_memory.write_uchar(0x008D0896, weight)
            elif self.type == 65:
                PVZ_memory.write_uchar(0x008D0743, weight)
            elif self.type == 66:
                PVZ_memory.write_uchar(0x008D051C, weight)
            elif self.type == 67:
                PVZ_memory.write_uchar(0x008D05F7, weight)
