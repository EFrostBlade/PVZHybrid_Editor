import PVZ_asm
import PVZ_Hybrid as pvz
import PVZ_data as data
from tkinter import filedialog
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox, Toplevel, Listbox, Checkbutton, IntVar, font
import importlib.util
import requests
import keyboard
import json
import webbrowser
import ctypes
import sys
import os
import time
import re
import psutil
import win32process
import win32gui
import wmi
import hashlib
import pyperclip
from pyDes import *
import binascii
from pymem import Pymem
from PIL import Image
Image.CUBIC = Image.BICUBIC
current_version = '0.24'
version_url = 'https://gitee.com/EFrostBlade/PVZHybrid_Editor/raw/main/version.txt'
main_window = None
data.update_PVZ_memory(1)
zombie_select = None
plant_select = None
item_select = None
plant_characteristic_type = None
shortcut_entries = []
shortcut_buttons = []
shortcut_comboboxs = []
action_values = []
action_list = ["已失效", "设置阳光", "增加阳光", "自由放置", "免费种植", "取消冷却", "自动收集", "柱子模式", "超级铲子", "永不失败",
               "当前关卡胜利", "秒杀所有僵尸", "解锁全部植物", "放置植物", "搭梯", "清除植物", "放置僵尸", "关卡失败", "存档", "读档",
               "游戏加速", "游戏减速", "随机卡槽"]
# 默认配置
default_config = {
    "shortcuts": {
        "key1": {
            "key": "ctrl+space",
            "action": 0
        },
        "key2": {
            "key": "Ctrl+f2",
            "action": 1
        },
        "key3": {
            "key": "Ctrl+f3",
            "action": 2
        },
        "key4": {
            "key": "Ctrl+f4",
            "action": 3
        },
        "key5": {
            "key": "Ctrl+f5",
            "action": 4
        },
        "key6": {
            "key": "Ctrl+f6",
            "action": 5
        },
        "key7": {
            "key": "Ctrl+f7",
            "action": 6
        },
        "key8": {
            "key": "Ctrl+f8",
            "action": 7
        },
        "key9": {
            "key": "Ctrl+f9",
            "action": 8
        },
        "key10": {
            "key": "Ctrl+f10",
            "action": 9
        },
        "key11": {
            "key": "Ctrl+f11",
            "action": 10
        },
        "key12": {
            "key": "Ctrl+f12",
            "action": 11
        }
    }
}
# 点击关闭退出


def exit_editor(file_path, window, section='main_window_position'):
    config = load_config(file_path)
    config[section] = {
        'x': window.winfo_x(),
        'y': window.winfo_y()
    }
    save_config(config, file_path)
    os._exit(0)


def exit_with_delete_config(config_file_path):
    os.remove(config_file_path)
    os._exit(0)


def resource_path(relative_path):
    """ 获取资源的绝对路径，适用于开发环境和PyInstaller环境 """
    try:
        # PyInstaller创建的临时文件夹的路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# 定义应用程序名称
app_name = 'PVZHybrid_Editor'

# 获取当前用户的AppData目录路径
appdata_path = os.getenv('APPDATA')

# 在AppData目录下为你的应用创建一个配置文件夹
app_config_path = os.path.join(appdata_path, app_name)
if not os.path.exists(app_config_path):
    os.makedirs(app_config_path)

# 定义配置文件的路径
config_file_path = os.path.join(app_config_path, 'config.json')

# 创建配置文件的函数


def create_config(file_path, default_config):
    with open(file_path, 'w') as file:
        json.dump(default_config, file, indent=4, ensure_ascii=False)

# 读取配置文件的函数


def load_config(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            return json.load(file)
    except:
        delete_config()

# 修改配置文件的函数


def modify_config(file_path, section, key, value):
    config = load_config(file_path)
    if section not in config:
        config[section] = {}
    config[section][key] = value
    save_config(config, file_path)


# 更新配置文件的函数
def save_config(config, file_path):
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)


def chooseGame():
    global main_window

    def openPVZ_memory(process1):
        try:
            data.update_PVZ_memory(
                Pymem(int(re.search(r'(\d+)', process1).group(1))))
            data.update_PVZ_pid(int(re.search(r'(\d+)', process1).group(1)))
        except:
            Messagebox.show_error("没有足够的权限，请确保游戏未以管理员身份运行",
                                  title="注入进程失败", parent=choose_process_window)
            choose_process_window.quit()
            choose_process_window.destroy()
        else:
            choose_process_window.quit()
            choose_process_window.destroy()

    def tryFindGame():
        try:
            hwnd = win32gui.FindWindow("MainWindow", None)
            pid = win32process.GetWindowThreadProcessId(hwnd)
            data.update_PVZ_memory(Pymem(pid[1]))
            data.update_PVZ_pid(pid[1])
            choose_process_window.quit()
            choose_process_window.destroy()
        except:
            Messagebox.show_error("请确保游戏已开启且未以管理员身份运行\n如果仍无法注入游戏可以尝试使用管理员身份开启本修改器",
                                  title="未找到游戏", parent=choose_process_window)
            return

    # def retry():
    #     global PVZ_memory
    #     choose_process_window.quit()
    #     choose_process_window.destroy()
    #     data.update_PVZ_memory(1
    #     # choosegame()
    #     return PVZ_memory

    def close():
        choose_process_window.quit()
        choose_process_window.destroy()
        data.update_PVZ_memory(0)
        data.update_PVZ_pid(0)

    def getSelecthwnd():
        hwnd_title = dict()

        def get_all_hwnd(hwnd, mouse):
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
        win32gui.EnumWindows(get_all_hwnd, 0)
        selecthwnd = list()
        for h, t in hwnd_title.items():
            if t != "":
                pid = win32process.GetWindowThreadProcessId((h))
                pn = psutil.Process(pid[1]).name()
                selecthwnd.append((pid[1], [t], [pn]))
        return selecthwnd

    choose_process_window = ttk.Toplevel(topmost=True)
    choose_process_window.title("选择进程")
    choose_process_window.geometry("500x500")
    choose_process_window.iconphoto(False, ttk.PhotoImage(
        file=resource_path(r"res\icon\choose.png")))
    choose_process_window.tk.call('tk', 'scaling', 4/3)
    main_window_x = main_window.winfo_x()
    main_window_y = main_window.winfo_y()
    choose_process_window.geometry(f'+{main_window_x+50}+{main_window_y + 50}')
    label = ttk.Label(choose_process_window, text="如果未开启游戏请开启游戏后点击寻找游戏按钮",
                      bootstyle=WARNING, font=("黑体", 16))
    label.pack(pady=20)
    frame1 = ttk.Frame(choose_process_window)
    frame1.pack()
    retry_button = ttk.Button(
        frame1, text='寻找游戏', command=lambda: tryFindGame())
    retry_button.pack(side=LEFT, padx=80)
    close_button = ttk.Button(
        frame1, text='关闭', bootstyle=DANGER, command=lambda: close())
    close_button.pack(side=RIGHT, padx=80)
    label = ttk.Label(choose_process_window,
                      text="如有需要可在下方手动选择游戏窗口\n窗口名一般为植物大战僵尸杂交版\n进程名一般为PlantsVsZombies.exe\n显示格式为pid 窗口名 进程名", bootstyle=INFO, font=("黑体", 16))
    label.pack(pady=(50, 10))
    frame2 = ttk.Frame(choose_process_window)
    frame2.pack()
    combobox = ttk.Combobox(frame2, bootstyle=PRIMARY, width=50)
    combobox.pack(side=LEFT)

    def refreshList():
        selecthwnd = getSelecthwnd()
        # 设置下拉菜单中的值
        combobox['state'] = NORMAL
        combobox['value'] = (selecthwnd)
        combobox['state'] = READONLY
    # 设置下拉菜单的默认值,默认值索引从0开始
        combobox.current(0)
    refreshList()
    refresh_button = ttk.Button(
        frame2, text='刷新列表', bootstyle=INFO, command=lambda: refreshList())
    refresh_button.pack(side=LEFT, padx=(10, 0))
    comfrime_button = ttk.Button(choose_process_window, text='确定',
                                 bootstyle=SUCCESS, command=lambda: openPVZ_memory(combobox.get()))
    comfrime_button.pack(pady=(30, 0))
    choose_process_window.protocol('WM_DELETE_WINDOW', lambda: close())
    choose_process_window.mainloop()


def support():
    global main_window
    support_window = ttk.Toplevel(topmost=True)
    support_window.title("关于")
    support_window.geometry("300x460")
    support_window.iconphoto(False, ttk.PhotoImage(
        file=resource_path((r"res\icon\info.png"))))
    support_window.tk.call('tk', 'scaling', 4/3)
    main_window_x = main_window.winfo_x()
    main_window_y = main_window.winfo_y()
    support_window.geometry(f'+{main_window_x+100}+{main_window_y + 100}')
    ttk.Label(support_window, text="本软件完全免费", font=(
        "黑体", 18), bootstyle=SUCCESS).pack(pady=10)

    def open_qq0():
        webbrowser.open_new(
            "https://qm.qq.com/q/arrZGcHwpG")
    qq0_frame = ttk.Frame(support_window)
    qq0_frame.pack()
    ttk.Label(qq0_frame, text="交流群：", font=(
        "黑体", 8), bootstyle=INFO).pack(side=LEFT)
    ttk.Button(qq0_frame, text="970286809", padding=0, bootstyle=(
        PRIMARY, LINK), cursor="hand2", command=open_qq0).pack(side=LEFT)
    ttk.Label(support_window, text="有问题可以加群反馈",
              font=("黑体", 8), bootstyle=INFO).pack()
    text = ttk.Text(support_window, width=50, height=8)
    scroll = ttk.Scrollbar(support_window)
    # 放到窗口的右侧, 填充Y竖直方向
    scroll.place(x=0, y=155, relx=1, anchor=E, height=150)

    # 两个控件关联
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)

    text.pack()
    str1 = 'b0.24\n' \
           '移除了原本的高级暂停，请使用新版高级暂停\n' \
           '高级暂停遮罩的颜色可以自定义了\n' \
           '新增宝藏吞噬者无坑和骷髅僵尸无坑功能，位于暂未分类标签页 \n' \
           '新增子弹大小修改功能（不影响伤害），对部分植物有效 \n' \
           '新增植物子弹类型修改功能，对部分植物有效 \n' \
           'b0.23\n' \
           '修复了毁灭菇不留坑但仍然无法种植的bug\n' \
           '优化了取消冷却，现在可以在高级暂停时连续种植了\n' \
           '为高级暂停添加了视觉效果提示，现在高级暂停改为由游戏内快捷键触发 \n' \
           '新增存档修改功能，可以快速将关卡修改为已通过或未通过 \n' \
           '推车和补车增加了全部选项，增加了自动补车功能 \n' \
           'b0.22\n' \
           '修复了僵尸掉落导致闪退的bug\n' \
           '修复了开启超级铲子情况下铲除墓碑吞噬者产生的土豆雷闪退的bug\n' \
           '优化了自由放置和柱子模式 \n' \
           '新增毁灭不留坑、僵尸豆产出魅惑僵尸、传送带无延迟、无尽轮数修改功能，位于暂未分类标签页 \n'

    text.insert(INSERT, str1)
    text.config(state=DISABLED)
    github_frame = ttk.Frame(support_window)
    github_frame.pack()
    ttk.Label(github_frame, text="所有代码开源于", font=(
        "黑体", 12), bootstyle=SUCCESS).pack(side=LEFT)

    def open_code():
        webbrowser.open_new("https://github.com/EFrostBlade/PVZHybrid_Editor")
    ttk.Button(github_frame, text="PVZHybrid_Editor(github.com)", padding=0, bootstyle=(
        PRIMARY, LINK), cursor="hand2", command=open_code).pack(side=LEFT)
    ttk.Label(support_window, text="如果您觉得本软件有帮助，欢迎赞助支持开发者",
              font=("黑体", 8), bootstyle=WARNING).pack()

    def open_qq():
        webbrowser.open_new(
            "http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=NXcD3BMkaDeyysTJYZZvJnl7xDZEL7et&authKey=rRxScaHQ7BDXklafDeSFtMLVgXRK8%2Bkd0PdQ2sssDv9AtnJE4HATLSbAjTxJKRGR&noverify=0&group_code=678474090")
    qq_frame = ttk.Frame(support_window)
    qq_frame.pack()
    ttk.Label(qq_frame, text="赞助任意金额后即可加入赞助群：", font=(
        "黑体", 8), bootstyle=WARNING).pack(side=LEFT)
    ttk.Button(qq_frame, text="678474090", padding=0, bootstyle=(
        PRIMARY, LINK), cursor="hand2", command=open_qq).pack(side=LEFT)
    ttk.Label(support_window, text="进群可享受功能优先适配、1对1解决问题等服务",
              font=("黑体", 8), bootstyle=WARNING).pack()
    ttk.Label(support_window, text=r"群里有好东西，赞助后请务必进群\^o^/",
              font=("黑体", 8), bootstyle=WARNING).pack()
    image_frame = ttk.Frame(support_window)
    image_frame.pack()
    AliPay = ttk.PhotoImage(file=resource_path(r"res/support/AliPay.png"))
    WeChatPay = ttk.PhotoImage(
        file=resource_path(r"res/support/WeChatPay.png"))
    AliPay_image = ttk.Label(image_frame, image=AliPay)
    AliPay_image.grid(row=0, column=0, padx=10)
    WeChatPay_image = ttk.Label(image_frame, image=WeChatPay)
    WeChatPay_image.grid(row=0, column=1, padx=10)
    ttk.Label(image_frame, text="支付宝", bootstyle=PRIMARY,
              font=("黑体", 12)).grid(row=1, column=0, pady=5)
    ttk.Label(image_frame, text="微信支付", bootstyle=SUCCESS,
              font=("黑体", 12)).grid(row=1, column=1, pady=5)
    support_window.mainloop()


def delete_config():
    global main_window
    deete_config_window = ttk.Toplevel(topmost=True)
    deete_config_window.title("配置文件出错！")
    deete_config_window.geometry("300x300")
    deete_config_window.tk.call('tk', 'scaling', 4/3)
    main_window_x = main_window.winfo_x()
    main_window_y = main_window.winfo_y()
    deete_config_window.geometry(f'+{main_window_x+100}+{main_window_y + 100}')
    ttk.Label(deete_config_window, text="读取配置文件时发生错误\n将删除配置文件并关闭程序\n请重新启动程序", font=(
        "黑体", 18), bootstyle=DANGER).pack(pady=20)
    ttk.Button(deete_config_window, text="确定", bootstyle=DANGER,
               command=lambda: exit_with_delete_config(config_file_path)).pack()
    deete_config_window.protocol(
        "WM_DELETE_WINDOW", lambda: exit_with_delete_config(config_file_path))
    deete_config_window.mainloop()


def mainWindow():
    global main_window
    main_window = ttk.Window()
    main_window.title("杂交版多功能修改器  "+str(current_version))
    main_window.geometry("600x600")
    main_window.iconphoto(False, ttk.PhotoImage(
        file=resource_path(r"res\icon\editor.png")))
    main_window.tk.call('tk', 'scaling', 4/3)

    def apply_window_position(file_path, window, section='main_window_position'):
        config = load_config(file_path)
        position = config.get(section, {})
        x = position.get('x', 100)  # 默认值为100
        y = position.get('y', 100)  # 默认值为100
        window.geometry(f'+{x}+{y}')

    # 在主窗口创建后调用
    apply_window_position(config_file_path, main_window)

    def open_update_window(latest_version):
        global main_window

        def close():
            update_window.quit()
            update_window.destroy()

        update_window = ttk.Toplevel(topmost=True)
        update_window.title("有新版本")
        update_window.geometry("320x400")
        update_window.iconphoto(False, ttk.PhotoImage(
            file=resource_path((r"res\icon\info.png"))))
        update_window.tk.call('tk', 'scaling', 4/3)
        main_window_x = main_window.winfo_x()
        main_window_y = main_window.winfo_y()
        update_window.geometry(f'+{main_window_x+100}+{main_window_y + 100}')
        ttk.Label(update_window, text="检测到新版本{}".format(
            latest_version), font=("黑体", 18), bootstyle=INFO).pack()
        ttk.Label(update_window, text="本软件完全免费", font=(
            "黑体", 18), bootstyle=SUCCESS).pack(pady=20)
        github_frame = ttk.Frame(update_window)
        github_frame.pack()
        ttk.Label(github_frame, text="前往下载最新版本", font=(
            "黑体", 12), bootstyle=SUCCESS).pack(side=LEFT)

        def open_code():
            webbrowser.open_new(
                "https://gitee.com/EFrostBlade/PVZHybrid_Editor/releases")
        ttk.Button(github_frame, text="PVZHybrid_Editor(gitee.com)", padding=0, bootstyle=(
            PRIMARY, LINK), cursor="hand2", command=open_code).pack(side=LEFT)
        ttk.Label(update_window, text="如果您觉得本软件有帮助，欢迎赞助支持开发者",
                  font=("黑体", 8), bootstyle=WARNING).pack()

        def open_qq():
            webbrowser.open_new(
                "http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=NXcD3BMkaDeyysTJYZZvJnl7xDZEL7et&authKey=rRxScaHQ7BDXklafDeSFtMLVgXRK8%2Bkd0PdQ2sssDv9AtnJE4HATLSbAjTxJKRGR&noverify=0&group_code=678474090")
        qq_frame = ttk.Frame(update_window)
        qq_frame.pack()
        ttk.Label(qq_frame, text="赞助任意金额后即可加入赞助群：", font=(
            "黑体", 8), bootstyle=WARNING).pack(side=LEFT)
        ttk.Button(qq_frame, text="678474090", padding=0, bootstyle=(
            PRIMARY, LINK), cursor="hand2", command=open_qq).pack(side=LEFT)
        ttk.Label(update_window, text="进群可享受功能优先适配、1对1解决问题等服务",
                  font=("黑体", 8), bootstyle=WARNING).pack()
        ttk.Label(update_window, text=r"群里有好东西，赞助后请务必进群\^o^/",
                  font=("黑体", 8), bootstyle=WARNING).pack()
        image_frame = ttk.Frame(update_window)
        image_frame.pack()
        AliPay = ttk.PhotoImage(file=resource_path(r"res/support/AliPay.png"))
        WeChatPay = ttk.PhotoImage(
            file=resource_path(r"res/support/WeChatPay.png"))
        AliPay_image = ttk.Label(image_frame, image=AliPay)
        AliPay_image.grid(row=0, column=0, padx=10)
        WeChatPay_image = ttk.Label(image_frame, image=WeChatPay)
        WeChatPay_image.grid(row=0, column=1, padx=10)
        ttk.Label(image_frame, text="支付宝", bootstyle=PRIMARY,
                  font=("黑体", 12)).grid(row=1, column=0, pady=5)
        ttk.Label(image_frame, text="微信支付", bootstyle=SUCCESS,
                  font=("黑体", 12)).grid(row=1, column=1, pady=5)
        update_window.protocol('WM_DELETE_WINDOW', lambda: close())
        update_window.mainloop()

    try:
        # 从服务器获取最新版本号
        response = requests.get(version_url)
        latest_version = response.text.strip()
        print(latest_version)
        if (latest_version == "The content may contain violation information"):
            Messagebox.show_error('版本号被屏蔽', title='更新检测失败',)
        # 比较版本号
        elif latest_version > current_version:
            # 如果发现新版本，提示用户
            open_update_window(latest_version)
    except Exception as e:
        Messagebox.show_error('无法检查更新，请检查您的网络连接。', title='更新检测失败',)

    # style=ttk.Style()
    # style.configure('small.TButton',font=("黑体",8),padding=(0,0,0,0))
    process_frame = ttk.Frame(main_window)
    process_frame.place(x=0, y=0, relx=1, rely=1, anchor=SE)
    process_label = ttk.Label(process_frame, text="", font=("黑体", 8))
    process_label.pack(side=LEFT)

    def updateGame():
        chooseGame()
        if (type(data.PVZ_memory) != Pymem):
            process_label["text"] = "未找到游戏"
            process_label.config(bootstyle=DANGER)
        else:
            process_label["text"] = "找到进程："+str(data.PVZ_memory.process_id)+str(
                psutil.Process(data.PVZ_memory.process_id).name())
            process_label.config(bootstyle=DANGER)

    def tryFindGame():
        try:
            hwnd = win32gui.FindWindow("MainWindow", None)
            pid = win32process.GetWindowThreadProcessId(hwnd)
            data.update_PVZ_memory(Pymem(pid[1]))
            data.update_PVZ_pid(pid[1])
            process_label["text"] = "找到进程："+str(data.PVZ_memory.process_id)+str(
                psutil.Process(data.PVZ_memory.process_id).name())
            process_label.config(bootstyle=DANGER)
        except:
            updateGame()
    tryFindGame()
    choose_process_button = ttk.Button(process_frame, text="选择游戏", padding=0, cursor="hand2", bootstyle=(
        PRIMARY, LINK), command=lambda: updateGame())
    choose_process_button.pack(side=LEFT)
    back_ground_status = ttk.IntVar(main_window)
    back_ground_check = ttk.Checkbutton(main_window, text="后台运行", variable=back_ground_status,
                                        bootstyle="round-toggle", command=lambda: pvz.backGround(back_ground_status.get()))
    back_ground_check.place(x=3, y=-3, relx=0, rely=1, anchor=SW)

    page_tab = ttk.Notebook(main_window)
    page_tab.pack(padx=5, pady=(5, 25), fill=BOTH, expand=True)
    common_page = ttk.Frame(page_tab)
    common_page.pack()
    page_tab.add(common_page, text="常用功能")
    resource_modify_frame = ttk.Labelframe(
        common_page, text="资源修改", bootstyle=WARNING)
    resource_modify_frame.place(x=0, y=0, anchor=NW)
    upper_limit_status = ttk.BooleanVar(resource_modify_frame)
    upper_limit_check = ttk.Checkbutton(resource_modify_frame, text="解锁资源上限", bootstyle="warning-round-toggle",
                                        variable=upper_limit_status, command=lambda: pvz.upperLimit(upper_limit_status.get()))
    upper_limit_check.grid(row=0, column=0, columnspan=2, sticky=E)
    ttk.Label(resource_modify_frame, text="当前阳光:", bootstyle=WARNING,
              font=("宋体", 14)).grid(row=1, column=0, sticky=E)
    sun_value = ttk.IntVar(resource_modify_frame)
    sun_value_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=sun_value)
    sun_value_entry.grid(row=1, column=1)

    def setSun(event):
        pvz.setSun(sun_value.get())
        resource_modify_frame.focus_set()
    sun_value_entry.bind("<Return>", setSun)
    ttk.Label(resource_modify_frame, text="增加阳光:", bootstyle=WARNING,
              font=("宋体", 14)).grid(row=2, column=0, sticky=E)
    sun_add_value = ttk.IntVar(resource_modify_frame)
    sun_add_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=sun_add_value)
    sun_add_entry.grid(row=2, column=1)
    config = load_config(config_file_path)
    try:
        sun_add_value.set(config["data"]["sunadd"])
    except:
        pass

    def addSun(event):
        pvz.addSun(sun_add_value.get())
        modify_config(config_file_path, "data", "sunadd", sun_add_value.get())
        resource_modify_frame.focus_set()
    sun_add_entry.bind("<Return>", addSun)

    ttk.Label(resource_modify_frame, text="当前银币:", bootstyle=SECONDARY,
              font=("宋体", 14)).grid(row=3, column=0, sticky=E)
    silver_value = ttk.IntVar(resource_modify_frame)
    silver_value_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=silver_value)
    silver_value_entry.grid(row=3, column=1)

    def setSilver(event):
        pvz.setSilver(silver_value.get())
        resource_modify_frame.focus_set()
    silver_value_entry.bind("<Return>", setSilver)
    ttk.Label(resource_modify_frame, text="增加银币:", bootstyle=SECONDARY,
              font=("宋体", 14)).grid(row=4, column=0, sticky=E)
    silver_add_value = ttk.IntVar(resource_modify_frame)
    silver_add_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=silver_add_value)
    silver_add_entry.grid(row=4, column=1)
    config = load_config(config_file_path)
    try:
        silver_add_value.set(config["data"]["silveradd"])
    except:
        pass

    def addSilver(event):
        pvz.addSilver(silver_add_value.get())
        modify_config(config_file_path, "data",
                      "silveradd", silver_add_value.get())
        resource_modify_frame.focus_set()
    silver_add_entry.bind("<Return>", addSilver)

    ttk.Label(resource_modify_frame, text="当前金币:", bootstyle=WARNING,
              font=("宋体", 14)).grid(row=5, column=0, sticky=E)
    gold_value = ttk.IntVar(resource_modify_frame)
    gold_value_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=gold_value)
    gold_value_entry.grid(row=5, column=1)

    def setGold(event):
        pvz.setGold(gold_value.get())
        resource_modify_frame.focus_set()
    gold_value_entry.bind("<Return>", setGold)
    ttk.Label(resource_modify_frame, text="增加金币:", bootstyle=WARNING,
              font=("宋体", 14)).grid(row=6, column=0, sticky=E)
    gold_add_value = ttk.IntVar(resource_modify_frame)
    gold_add_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=gold_add_value)
    gold_add_entry.grid(row=6, column=1)
    config = load_config(config_file_path)
    try:
        gold_add_value.set(config["data"]["goldadd"])
    except:
        pass

    def addGold(event):
        pvz.addGold(gold_add_value.get())
        modify_config(config_file_path, "data",
                      "goldadd", gold_add_value.get())
        resource_modify_frame.focus_set()
    gold_add_entry.bind("<Return>", addGold)

    ttk.Label(resource_modify_frame, text="当前钻石:", bootstyle=PRIMARY,
              font=("宋体", 14)).grid(row=7, column=0, sticky=E)
    diamond_value = ttk.IntVar(resource_modify_frame)
    diamond_value_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=diamond_value)
    diamond_value_entry.grid(row=7, column=1)

    def setDiamond(event):
        pvz.setDiamond(diamond_value.get())
        resource_modify_frame.focus_set()
    diamond_value_entry.bind("<Return>", setDiamond)
    ttk.Label(resource_modify_frame, text="增加钻石:", bootstyle=PRIMARY,
              font=("宋体", 14)).grid(row=8, column=0, sticky=E)
    diamond_add_value = ttk.IntVar(resource_modify_frame)
    diamond_add_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=diamond_add_value)
    diamond_add_entry.grid(row=8, column=1)
    config = load_config(config_file_path)
    try:
        diamond_add_value.set(config["data"]["diamondadd"])
    except:
        pass

    def addDiamond(event):
        pvz.addDiamond(diamond_add_value.get())
        modify_config(config_file_path, "data",
                      "diamondadd", diamond_add_value.get())
        resource_modify_frame.focus_set()
    diamond_add_entry.bind("<Return>", addDiamond)

    quick_start_frame = ttk.LabelFrame(
        common_page, text="快速使用", bootstyle=SUCCESS)
    quick_start_frame.place(x=0, y=0, relx=1, rely=0, anchor=NE)
    over_plant_status = ttk.BooleanVar(quick_start_frame)
    over_plant_check = ttk.Checkbutton(quick_start_frame, text="自由放置", variable=over_plant_status,
                                       bootstyle="success-round-toggle", command=lambda: pvz.overPlant(over_plant_status.get()))
    over_plant_check.grid(row=0, column=0, sticky=W)
    ToolTip(over_plant_check, text="植物可以重叠放置并无视地形", bootstyle=(INFO, INVERSE))
    free_plant_status = ttk.BooleanVar(quick_start_frame)
    free_plant_check = ttk.Checkbutton(quick_start_frame, text="免费种植", variable=free_plant_status,
                                       bootstyle="success-round-toggle", command=lambda: pvz.ignoreSun(free_plant_status.get()))
    free_plant_check.grid(row=1, column=0, sticky=W)
    ToolTip(free_plant_check, text="植物可以不消耗阳光种植", bootstyle=(INFO, INVERSE))
    cancel_cd_status = ttk.BooleanVar(quick_start_frame)
    cancel_cd_check = ttk.Checkbutton(quick_start_frame, text="取消冷却", variable=cancel_cd_status,
                                      bootstyle="success-round-toggle", command=lambda: pvz.cancelCd(cancel_cd_status.get()))
    cancel_cd_check.grid(row=2, column=0, sticky=W)
    ToolTip(cancel_cd_check, text="植物种植后不进入冷却时间", bootstyle=(INFO, INVERSE))
    auto_colect_status = ttk.BooleanVar(quick_start_frame)
    auto_colect_check = ttk.Checkbutton(quick_start_frame, text="自动收集", variable=auto_colect_status,
                                        bootstyle="success-round-toggle", command=lambda: pvz.autoCollect(auto_colect_status.get()))
    auto_colect_check.grid(row=3, column=0, sticky=W)
    ToolTip(auto_colect_check, text="自动收集自然掉落的阳光和僵尸掉落的金币",
            bootstyle=(INFO, INVERSE))
    column_like_status = ttk.BooleanVar(quick_start_frame)
    column_like_check = ttk.Checkbutton(quick_start_frame, text="柱子模式", variable=column_like_status,
                                        bootstyle="success-round-toggle", command=lambda: pvz.column(column_like_status.get()))
    column_like_check.grid(row=4, column=0, sticky=W)
    ToolTip(column_like_check, text="种植一个植物后在同一列的其他行种植相同的植物(可与自由放置配合使用)",
            bootstyle=(INFO, INVERSE))
    shovel_pro_status = ttk.BooleanVar(quick_start_frame)
    shovel_pro_check = ttk.Checkbutton(quick_start_frame, text="超级铲子", variable=shovel_pro_status,
                                       bootstyle="success-round-toggle", command=lambda: pvz.shovelpro(shovel_pro_status.get()))
    shovel_pro_check.grid(row=5, column=0, sticky=W)
    ToolTip(shovel_pro_check, text="铲掉植物返还其阳光消耗并触发亡语效果",
            bootstyle=(INFO, INVERSE))
    never_fail_status = ttk.BooleanVar(quick_start_frame)
    never_fail_check = ttk.Checkbutton(quick_start_frame, text="永不失败", variable=never_fail_status,
                                       bootstyle="success-round-toggle", command=lambda: pvz.ignoreZombies(never_fail_status.get()))
    never_fail_check.grid(row=6, column=0, sticky=W)
    ToolTip(never_fail_check, text="僵尸进家不判定游戏失败", bootstyle=(INFO, INVERSE))
    # pause_pro_status = ttk.BooleanVar(quick_start_frame)
    # pause_pro_check = ttk.Checkbutton(quick_start_frame, text="高级暂停", variable=pause_pro_status,
    #                                   bootstyle="success-round-toggle", command=lambda: pvz.pausePro(pause_pro_status.get()))
    # pause_pro_check.grid(row=7, column=0, sticky=W)
    # ToolTip(pause_pro_check, text="可以暂停种植植物", bootstyle=(INFO, INVERSE))
    win_button = ttk.Button(quick_start_frame, text="当前关卡胜利", padding=0, bootstyle=(
        SUCCESS, OUTLINE), command=lambda: pvz.win())
    win_button.grid(row=8, column=0, sticky=W, pady=(2, 2))
    ToolTip(win_button, text="当前的游戏关卡直接进行胜利结算", bootstyle=(INFO, INVERSE))
    defeat_button = ttk.Button(quick_start_frame, text="当前关卡失败", padding=0, bootstyle=(
        SUCCESS, OUTLINE), command=lambda: pvz.defeat())
    defeat_button.grid(row=9, column=0, sticky=W, pady=(2, 2))
    ToolTip(defeat_button, text="当前的游戏关卡直接进行失败结算", bootstyle=(INFO, INVERSE))
    kill_all_button = ttk.Button(quick_start_frame, text="秒杀所有僵尸", padding=0, bootstyle=(
        SUCCESS, OUTLINE), command=lambda: pvz.killAllZombies())
    kill_all_button.grid(row=10, column=0, sticky=W, pady=(2, 2))
    ToolTip(kill_all_button, text="秒杀当前场上的所有僵尸", bootstyle=(INFO, INVERSE))
    unlock_button = ttk.Button(quick_start_frame, text="解锁全部植物", padding=0, bootstyle=(
        SUCCESS, OUTLINE), command=lambda: pvz.unlock())
    unlock_button.grid(row=11, column=0, sticky=W, pady=(2, 2))
    ToolTip(unlock_button, text="在本次游戏中临时解锁图鉴中的所有植物(包括尚无法获得的隐藏植物)",
            bootstyle=(INFO, INVERSE))
    save_load_frame = ttk.Frame(quick_start_frame)
    save_load_frame.grid(row=12, column=0, sticky=W, pady=(2, 2))
    save_button = ttk.Button(save_load_frame, text="存档", padding=0, bootstyle=(
        SUCCESS, OUTLINE), command=lambda: pvz.save())
    save_button.grid(row=0, column=0, sticky=W, padx=(5, 0), pady=(2, 2))
    load_button = ttk.Button(save_load_frame, text="读档", padding=0, bootstyle=(
        SUCCESS, OUTLINE), command=lambda: pvz.load())
    load_button.grid(row=0, column=1, sticky=W, padx=(10, 0), pady=(2, 2))

    pause_pro_frame = ttk.LabelFrame(
        common_page, text="高级暂停", bootstyle=SUCCESS)
    pause_pro_frame.place(x=0, y=300, relx=1, rely=0, anchor=NE)
    pause_pro_status = ttk.BooleanVar(pause_pro_frame)
    pause_pro_check = ttk.Checkbutton(pause_pro_frame, text="快捷键高级暂停", variable=pause_pro_status,
                                      bootstyle="success-round-toggle", command=lambda: setPauseKey())
    pause_pro_check.grid(row=0, column=0, sticky=W)
    slot_pause_key = ttk.Combobox(
        pause_pro_frame, width=5, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_pause_key.grid(row=1, column=0)
    slot_pause_key.current(0)
    pause_color_frame = ttk.Frame(pause_pro_frame)
    pause_color_frame.grid(row=2, column=0)
    ttk.Label(pause_color_frame, text="R:", font=("黑体", 12), bootstyle=DANGER).grid(
        row=0, column=0)
    pause_r_entry = ttk.Entry(pause_color_frame, width=3, font=(
        "黑体", 12), bootstyle=SECONDARY)
    pause_r_entry.grid(row=0, column=1,  sticky=W)
    ttk.Label(pause_color_frame, text="G:", font=("黑体", 12), bootstyle=SUCCESS).grid(
        row=0, column=2)
    pause_g_entry = ttk.Entry(pause_color_frame, width=3, font=(
        "黑体", 12), bootstyle=SECONDARY)
    pause_g_entry.grid(row=0, column=3, sticky=W)
    ttk.Label(pause_color_frame, text="B:", font=("黑体", 12), bootstyle=PRIMARY).grid(
        row=1, column=0)
    pause_b_entry = ttk.Entry(pause_color_frame, width=3, font=(
        "黑体", 12), bootstyle=SECONDARY)
    pause_b_entry.grid(row=1, column=1,  sticky=W)
    ttk.Label(pause_color_frame, text="A:", font=("黑体", 12), bootstyle=SECONDARY).grid(
        row=1, column=2)
    pause_a_entry = ttk.Entry(pause_color_frame, width=3, font=(
        "黑体", 12), bootstyle=SECONDARY)
    pause_a_entry.grid(row=1, column=3, sticky=W)

    def get_pause_color():
        config = load_config(config_file_path)
        if "pauseColor" not in config["data"]:
            pause_r_entry.insert(0, '66')
            pause_g_entry.insert(0, 'CC')
            pause_b_entry.insert(0, 'FF')
            pause_a_entry.insert(0, 'AA')
        else:
            try:
                pause_r_entry.insert(0, config["data"]["pauseColor"]["R"])
            except:
                pause_r_entry.insert(0, '66')
            try:
                pause_g_entry.insert(0, config["data"]["pauseColor"]["G"])
            except:
                pause_g_entry.insert(0, 'CC')
            try:
                pause_b_entry.insert(0, config["data"]["pauseColor"]["B"])
            except:
                pause_b_entry.insert(0, 'FF')
            try:
                pause_a_entry.insert(0, config["data"]["pauseColor"]["A"])
            except:
                pause_a_entry.insert(0, 'AA')

    get_pause_color()

    def loadPauseKey():
        config = load_config(config_file_path)
        try:
            slot_pause_key.current(config["slotKeys"]["pause"])
        except:
            pass
    loadPauseKey()

    def setPauseKey():
        if (pause_pro_status.get()):
            config = load_config(config_file_path)
            if "slotKeys" not in config:
                config["slotKeys"] = {}
            if (slot_pause_key.current() != -1):
                config["slotKeys"]["pause"] = slot_pause_key.current()
            if "data" not in config:
                config["data"] = {}
            if "pauseColor" not in config["data"]:
                config["data"]["pauseColor"] = {}
            config["data"]["pauseColor"]["R"] = pause_r_entry.get()
            config["data"]["pauseColor"]["G"] = pause_g_entry.get()
            config["data"]["pauseColor"]["B"] = pause_b_entry.get()
            config["data"]["pauseColor"]["A"] = pause_a_entry.get()
            save_config(config, config_file_path)
            pvz.pauseProKey(slot_pause_key.current(), int(pause_r_entry.get(), 16), int(
                pause_g_entry.get(), 16), int(pause_b_entry.get(), 16), int(pause_a_entry.get(), 16))
        else:
            pvz.pauseProKey(False, 0, 0, 0, 0)

    game_speed_frame = ttk.LabelFrame(
        common_page, text="游戏速度", bootstyle=DARK)
    game_speed_frame.place(x=0, y=300, anchor=NW)
    game_speed_label = ttk.Label(game_speed_frame, text="1", bootstyle=DARK)
    game_speed_label.grid(row=0, column=0)
    game_speed_frame.columnconfigure(0, minsize=30)
    game_speed_value = ttk.DoubleVar(game_speed_frame)
    game_speed_value.set(2)

    def changeSpeedValue(value):
        step = 1
        adjusted_value = round(float(value) / step) * step
        game_speed_value.set(adjusted_value)
        if (game_speed_value.get() == 0):
            game_speed_label.config(text="0.25")
        elif (game_speed_value.get() == 1):
            game_speed_label.config(text="0.5")
        elif (game_speed_value.get() == 2):
            game_speed_label.config(text="1")
        elif (game_speed_value.get() == 3):
            game_speed_label.config(text="2")
        elif (game_speed_value.get() == 4):
            game_speed_label.config(text="5")
        elif (game_speed_value.get() == 5):
            game_speed_label.config(text="10")
        elif (game_speed_value.get() == 6):
            game_speed_label.config(text="20")
        pvz.changeGameSpeed(game_speed_value.get())
    game_speed_scale = ttk.Scale(game_speed_frame, from_=0, to=6, orient=HORIZONTAL,
                                 variable=game_speed_value, command=changeSpeedValue)
    game_speed_scale.grid(row=0, column=1)

    def on_mousewheel(event):
        # 计算滚轮的滚动方向和距离
        increment = -1 if event.delta > 0 else 1
        # 获取当前Scale的值
        value = game_speed_value.get() + increment
        # 设置新的Scale值
        step = 1
        adjusted_value = round(float(value) / step) * step
        game_speed_value.set(adjusted_value)
        if (game_speed_value.get() == 0):
            game_speed_label.config(text="0.25")
        elif (game_speed_value.get() == 1):
            game_speed_label.config(text="0.5")
        elif (game_speed_value.get() == 2):
            game_speed_label.config(text="1")
        elif (game_speed_value.get() == 3):
            game_speed_label.config(text="2")
        elif (game_speed_value.get() == 4):
            game_speed_label.config(text="5")
        elif (game_speed_value.get() == 5):
            game_speed_label.config(text="10")
        elif (game_speed_value.get() == 6):
            game_speed_label.config(text="20")
        pvz.changeGameSpeed(game_speed_value.get())
    game_speed_scale.bind("<MouseWheel>", on_mousewheel)

    game_difficult_frame = ttk.LabelFrame(
        common_page, text="游戏难度", bootstyle=DARK)
    game_difficult_frame.place(x=0, y=350, anchor=NW)
    gameDifficult = ttk.IntVar(game_difficult_frame)
    ttk.Radiobutton(game_difficult_frame, text="简单", value=1, variable=gameDifficult, bootstyle=SUCCESS,
                    command=lambda: pvz.setDifficult(gameDifficult.get())).grid(row=0, column=0, padx=5)
    ttk.Radiobutton(game_difficult_frame, text="普通", value=2, variable=gameDifficult, bootstyle=DARK,
                    command=lambda: pvz.setDifficult(gameDifficult.get())).grid(row=0, column=1, padx=5)
    ttk.Radiobutton(game_difficult_frame, text="困难", value=3, variable=gameDifficult, bootstyle=DANGER,
                    command=lambda: pvz.setDifficult(gameDifficult.get())).grid(row=0, column=2, padx=5)

    game_save_frame = ttk.LabelFrame(
        common_page, text="存档修改", bootstyle=DARK)
    game_save_frame.place(x=0, y=400, anchor=NW)
    ttk.Label(game_save_frame, text="冒险第").grid(row=0, column=0)
    adventure_start_level_value = ttk.IntVar(game_save_frame)
    adventure_start_level_combobox = ttk.Combobox(game_save_frame, textvariable=adventure_start_level_value, width=2, values=list(
        range(1, 67+1)), font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    adventure_start_level_combobox.grid(row=0, column=1)
    adventure_start_level_value.set(1)
    ttk.Label(game_save_frame, text="关至第").grid(row=0, column=2)
    adventure_end_level_value = ttk.IntVar(game_save_frame)
    adventure_end_level_combobox = ttk.Combobox(game_save_frame, textvariable=adventure_end_level_value, width=2, values=list(
        range(1, 67+1)), font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    adventure_end_level_combobox.grid(row=0, column=3)
    adventure_end_level_value.set(67)
    ttk.Label(game_save_frame, text="关").grid(row=0, column=4)

    def complete_advantures():
        for i in range(adventure_start_level_value.get()-1, adventure_end_level_value.get()):
            pvz.completeAdvanture(i)
    adventure_complete_button = ttk.Button(
        game_save_frame, text='已完成', bootstyle=(SUCCESS, OUTLINE), padding=0, command=lambda: complete_advantures())
    adventure_complete_button.grid(row=0, column=5, padx=2)

    def lock_advantures():
        for i in range(adventure_start_level_value.get()-1, adventure_end_level_value.get()):
            pvz.lockAdvanture(i)
    adventure_lock_button = ttk.Button(
        game_save_frame, text='未完成', bootstyle=(DANGER, OUTLINE), padding=0, command=lambda: lock_advantures())
    adventure_lock_button.grid(row=0, column=6, padx=2)
    ttk.Label(game_save_frame, text="挑战第").grid(row=1, column=0)
    challenge_start_level_value = ttk.IntVar(game_save_frame)
    challenge_start_level_combobox = ttk.Combobox(game_save_frame, textvariable=challenge_start_level_value, width=2, values=list(
        range(1, 99+1)), font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    challenge_start_level_combobox.grid(row=1, column=1)
    challenge_start_level_value.set(1)
    ttk.Label(game_save_frame, text="关至第").grid(row=1, column=2)
    challenge_end_level_value = ttk.IntVar(game_save_frame)
    challenge_end_level_combobox = ttk.Combobox(game_save_frame, textvariable=challenge_end_level_value, width=2, values=list(
        range(1, 99+1)), font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    challenge_end_level_combobox.grid(row=1, column=3)
    challenge_end_level_value.set(99)
    ttk.Label(game_save_frame, text="关").grid(row=1, column=4)

    def complete_challenges():
        for i in range(challenge_start_level_value.get()-1, challenge_end_level_value.get()):
            pvz.completeChallenge(i)
    adventure_complete_button = ttk.Button(
        game_save_frame, text='已完成', bootstyle=(SUCCESS, OUTLINE), padding=0, command=lambda: complete_challenges())
    adventure_complete_button.grid(row=1, column=5, padx=2)

    def lock_challenges():
        for i in range(challenge_start_level_value.get()-1, challenge_end_level_value.get()):
            pvz.lockChallenge(i)
    adventure_lock_button = ttk.Button(
        game_save_frame, text='未完成', bootstyle=(DANGER, OUTLINE), padding=0, command=lambda: lock_challenges())
    adventure_lock_button.grid(row=1, column=6, padx=2)

    # 读取快捷键配置

    def get_shortcuts():
        config = load_config(config_file_path)
        return config.get('shortcuts', {})

    # 移除所有当前的快捷键监听
    def remove_all_hotkeys():
        for shortcut in get_shortcuts().values():
            keyboard.remove_hotkey(shortcut['key'])

    # 重新加载快捷键并设置监听
    def reload_hotkeys():
        remove_all_hotkeys()
        shortcuts = get_shortcuts()
        for shortcut_id, shortcut_info in shortcuts.items():
            keyboard.add_hotkey(
                shortcut_info['key'], lambda action=shortcut_info['action']: on_triggered(action))

    # 修改快捷键配置并重新加载监听
    def modify_shortcut(shortcut_id, new_key, new_action):
        try:
            keyboard.add_hotkey(new_key, lambda: on_triggered(new_action))
        except:
            Messagebox.show_error("请检查快捷键输入是否正确", title="快捷键非法")
            return
        config = load_config(config_file_path)
        # 保存旧的快捷键值
        old_key = config['shortcuts'].get(shortcut_id, {}).get('key')
        if 'shortcuts' not in config:
            config['shortcuts'] = {}
        config['shortcuts'][shortcut_id] = {
            'key': new_key, 'action': new_action}
        save_config(config, config_file_path)
        # 如果旧的快捷键存在，则移除旧的快捷键监听
        if old_key:
            keyboard.remove_hotkey(old_key)
        # 添加新的快捷键监听
        # 更新快捷键显示
        update_shortcut_display()

    def switch_status(status):
        if (status.get() == True):
            status.set(False)
        elif (status.get() == False):
            status.set(True)
        elif (status.get() == 1):
            status.set(0)
        elif (status.get() == 0):
            status.set(1)

    # 捕获快捷键并在控制台输出
    def on_triggered(action):
        if action == 0:
            switch_status(pause_pro_status)
            pvz.pausePro(pause_pro_status.get())
        elif action == 1:
            pvz.setSun(sun_value.get())
        elif action == 2:
            pvz.addSun(sun_add_value.get())
        elif action == 3:
            switch_status(over_plant_status)
            pvz.overPlant(over_plant_status.get())
        elif action == 4:
            switch_status(free_plant_status)
            pvz.ignoreSun(free_plant_status.get())
        elif action == 5:
            switch_status(cancel_cd_status)
            pvz.cancelCd(cancel_cd_status.get())
        elif action == 6:
            switch_status(auto_colect_status)
            pvz.autoCollect(auto_colect_status.get())
        elif action == 7:
            switch_status(column_like_status)
            pvz.column(column_like_status.get())
        elif action == 8:
            switch_status(shovel_pro_status)
            pvz.shovelpro(shovel_pro_status.get())
        elif action == 9:
            switch_status(never_fail_status)
            pvz.ignoreZombies(never_fail_status.get())
        elif action == 10:
            pvz.win()
        elif action == 11:
            pvz.killAllZombies()
        elif action == 12:
            pvz.unlock()
        elif action == 13:
            putPlants(plantPut_type_combobox.current())
        elif action == 14:
            putLadders()
        elif action == 15:
            clearPlants()
        elif action == 16:
            putZombies()
        elif action == 17:
            putZombies(pvz.defeat())
        elif action == 18:
            putZombies(pvz.save())
        elif action == 19:
            putZombies(pvz.load())
        elif action == 20:
            if (game_speed_value.get() < 6):
                game_speed_value.set(game_speed_value.get()+1)
                pvz.changeGameSpeed(game_speed_value.get())
        elif action == 21:
            if (game_speed_value.get() > 0):
                game_speed_value.set(game_speed_value.get()-1)
                pvz.changeGameSpeed(game_speed_value.get())
        elif action == 22:
            switch_status(random_slots_status)
            pvz.randomSlots(random_slots_status.get())

    # 修改快捷键的窗口

    def open_change_window(shortcut_id, current_key, current_action):
        global main_window
        new_shortcut = []

        def set_new_shortcut():
            if new_shortcut:
                new_key = '+'.join(new_shortcut)
                modify_shortcut(shortcut_id, new_key, current_action)
                update_shortcut_display()
                change_shortcut_window.destroy()

        def record_key(event):
            key = event.keysym.lower() if event.keysym != 'space' else 'space'
            ctrl_pressed = event.state & 0x0004
            if 'control' in key:
                key = 'ctrl'
            elif 'shift' in key:
                key = 'shift'
            elif 'alt' in key:
                key = 'alt'
            elif 'win' in key:
                key = 'win'
            elif event.char == ' ' or (ctrl_pressed and key == '??'):
                key = 'space'
            if key not in new_shortcut:
                new_shortcut.append(key)
                entry.delete(0, END)
                entry.insert(0, '+'.join(new_shortcut))

        change_shortcut_window = ttk.Toplevel(topmost=True)
        change_shortcut_window.title('修改快捷键')
        change_shortcut_window.geometry("200x100")
        change_shortcut_window.iconphoto(False, ttk.PhotoImage(
            file=resource_path(r"res\icon\change.png")))
        change_shortcut_window.tk.call('tk', 'scaling', 4/3)
        main_window_x = main_window.winfo_x()
        main_window_y = main_window.winfo_y()
        change_shortcut_window.geometry(
            f'+{main_window_x+200}+{main_window_y + 200}')

        label = ttk.Label(change_shortcut_window, text='请按下新的快捷键')
        label.pack()

        entry = ttk.Entry(change_shortcut_window)
        entry.pack()
        entry.focus_set()

        # 记录按键
        change_shortcut_window.bind('<Key>', record_key)

        confirm_button = ttk.Button(
            change_shortcut_window, text='确定', bootstyle=SUCCESS, command=set_new_shortcut)
        confirm_button.place(x=20, y=-10, relx=0, rely=1, anchor=SW)

        cancel_button = ttk.Button(change_shortcut_window, text='取消',
                                   bootstyle=DANGER, command=change_shortcut_window.destroy)
        cancel_button.place(x=-20, y=-10, relx=1, rely=1, anchor=SE)

    # 更新快捷键显示
    def update_shortcut_display():
        shortcuts = get_shortcuts()
        for i, (shortcut_id, shortcut_info) in enumerate(shortcuts.items()):
            shortcut_entries[i].delete(0, END)
            shortcut_entries[i].insert(0, shortcut_info['key'])
            shortcut_buttons[i].config(command=lambda i=i, id=shortcut_id, info=shortcut_info: open_change_window(
                id, info['key'], info['action']))

    shortcut_frame = ttk.LabelFrame(common_page, text="快捷按键")
    shortcut_frame.place(x=180, y=0)
    # 创建快捷键显示文本框和修改按钮
    shortcuts = get_shortcuts()
    for i, (shortcut_id, shortcut_info) in enumerate(shortcuts.items()):
        # 显示快捷键的文本框
        entry = ttk.Entry(shortcut_frame, width=18, font=("黑体", 8))
        entry.insert(0, shortcut_info['key'])
        entry.grid(row=i, column=0, padx=2)
        shortcut_entries.append(entry)

        # 修改快捷键的按钮
        button = ttk.Button(shortcut_frame, text='修改', padding=0, bootstyle=(OUTLINE), command=lambda i=i,
                            id=shortcut_id, info=shortcut_info: open_change_window(id, info['key'], info['action']))
        button.grid(row=i, column=1, padx=2)
        shortcut_buttons.append(button)

        combobox = ttk.Combobox(
            shortcut_frame, values=action_list, width=13, state=READONLY)
        combobox.grid(row=i, column=2, padx=2)
        combobox.current(shortcut_info['action'])
        shortcut_comboboxs.append(combobox)

        def modify_action(event, id=shortcut_id, i=i):
            config = load_config(config_file_path)
            modify_shortcut(id, config['shortcuts'][id]
                            ["key"], shortcut_comboboxs[i].current())
        combobox.bind("<<ComboboxSelected>>", modify_action)
    # 设置快捷键监听
    try:
        for shortcut_info in shortcuts.values():
            keyboard.add_hotkey(
                shortcut_info['key'], lambda action=shortcut_info['action']: on_triggered(action))
    except:
        delete_config()

    global zombie_select
    zombie_page = ttk.Frame(page_tab)
    zombie_page.pack()
    page_tab.add(zombie_page, text="僵尸修改")
    zombie_list_frame = ttk.LabelFrame(
        zombie_page, text="僵尸列表", bootstyle=DANGER)
    zombie_list_frame.place(x=0, y=0, anchor=NW, height=260, width=275)
    zombie_list_box_scrollbar = ttk.Scrollbar(
        zombie_list_frame, bootstyle=DANGER)
    zombie_list_box = ttk.Treeview(zombie_list_frame, show=TREE, selectmode=BROWSE, padding=0, columns=(
        "zombie_list"), yscrollcommand=zombie_list_box_scrollbar.set, bootstyle=DANGER)
    zombie_list_box_scrollbar.configure(command=zombie_list_box.yview)
    zombie_list_box.place(x=0, y=0, anchor=NW, height=240, width=50)
    zombie_list_box_scrollbar.place(x=45, y=0, height=240, anchor=NW)
    zombie_list = list()

    def refresh_zombie_list():
        zombie_list.clear()
        zombie_list_box.delete(*zombie_list_box.get_children())
        try:
            zombie_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xa0)
        except:
            return
        i = 0
        j = 0
        while i < zombie_num:
            zombie_addresss = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x90)+0x204*j
            zombie_exist = data.PVZ_memory.read_bytes(zombie_addresss+0xec, 1)
            if (zombie_exist == b'\x00'):
                zombie_list.append(data.zombie(zombie_addresss))
                i = i+1
            j = j+1
        n = 0
        for k in range(zombie_num):
            zombie_list_box.insert("", END, iid=n, text=str(zombie_list[k].no))
            if (zombie_select != None):
                if (zombie_select.exist == 0):
                    if (zombie_select.no == zombie_list[k].no):
                        zombie_list_box.selection_set((str(n),))
            n = n+1

    refresh_zombie_list()
    zombie_attribute_frame = ttk.Frame(zombie_list_frame)
    zombie_attribute_frame.place(x=80, y=0, height=240, width=190)
    zombie_state_frame = ttk.Frame(zombie_attribute_frame)
    zombie_state_frame.grid(row=0, column=0, columnspan=12, sticky=W)
    ttk.Label(zombie_state_frame, text="僵尸类型:").grid(
        row=0, column=0, columnspan=2, sticky=W)
    zombie_type_value = ttk.IntVar(zombie_state_frame)
    zombie_type_entry = ttk.Entry(zombie_state_frame, textvariable=zombie_type_value, width=18, font=(
        "黑体", 8), state=READONLY, bootstyle=SECONDARY)
    zombie_type_entry.grid(row=0, column=2, columnspan=5, sticky=W)
    ttk.Label(zombie_state_frame, text="状态:").grid(row=1, column=0, sticky=W)
    zombie_state_value = ttk.IntVar(zombie_state_frame)
    zombie_state_entry = ttk.Entry(
        zombie_state_frame, textvariable=zombie_state_value, width=3, font=("黑体", 8), bootstyle=SECONDARY)
    zombie_state_entry.grid(row=1, column=1, sticky=W)

    def setZombieState(event):
        zombie_select.setState(zombie_state_value.get())
        zombie_state_frame.focus_set()
    zombie_state_entry.bind("<Return>", setZombieState)
    ttk.Label(zombie_state_frame, text="大小:").grid(row=1, column=3, sticky=W)
    zombie_size_value = ttk.DoubleVar(zombie_state_frame)
    zombie_size_entry = ttk.Entry(
        zombie_state_frame, textvariable=zombie_size_value, width=6, font=("黑体", 8), bootstyle=SECONDARY)
    zombie_size_entry.grid(row=1, column=4, sticky=W)

    def setZombieSize(event):
        zombie_select.setSize(zombie_size_value.get())
        zombie_state_frame.focus_set()
    zombie_size_entry.bind("<Return>", setZombieSize)
    zombie_position_frame = ttk.LabelFrame(
        zombie_attribute_frame, text="位置", bootstyle=DANGER)
    zombie_position_frame.grid(row=2, column=0, columnspan=4, sticky=W)
    ttk.Label(zombie_position_frame, text="x坐标:").grid(
        row=0, column=0, columnspan=3, sticky=W)
    zombie_x_value = ttk.DoubleVar(zombie_position_frame)
    zombie_x_entry = ttk.Entry(zombie_position_frame, textvariable=zombie_x_value, width=6, font=(
        "黑体", 8), bootstyle=SECONDARY)
    zombie_x_entry.grid(row=0, column=3, columnspan=3, sticky=W)

    def setZombieX(event):
        print(zombie_x_value.get())
        zombie_select.setX(zombie_x_value.get())
        zombie_position_frame.focus_set()
    zombie_x_entry.bind("<Return>", setZombieX)
    ttk.Label(zombie_position_frame, text="y坐标:").grid(
        row=1, column=0, columnspan=3, sticky=W)
    zombie_y_value = ttk.DoubleVar(zombie_position_frame)
    zombie_y_entry = ttk.Entry(zombie_position_frame, textvariable=zombie_y_value, width=6, font=(
        "黑体", 8), bootstyle=SECONDARY)
    zombie_y_entry.grid(row=1, column=3, columnspan=3, sticky=W)

    def setZombieY(event):
        zombie_select.setY(zombie_y_value.get())
        zombie_position_frame.focus_set()
    zombie_y_entry.bind("<Return>", setZombieY)
    ttk.Label(zombie_position_frame, text="第").grid(row=2, column=0, sticky=W)
    zombie_row_value = ttk.IntVar(zombie_position_frame)
    zombie_row_combobox = ttk.Combobox(zombie_position_frame, textvariable=zombie_row_value, width=2, values=[
                                       1, 2, 3, 4, 5, 6], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    zombie_row_combobox.grid(row=2, column=1, columnspan=3, sticky=W)
    ttk.Label(zombie_position_frame, text="行").grid(row=2, column=4, sticky=W)

    def setZombieRow(event):
        zombie_select.setRow(zombie_row_value.get())
        zombie_position_frame.focus_set()
    zombie_row_combobox.bind("<<ComboboxSelected>>", setZombieRow)
    zombie_hp_frame = ttk.LabelFrame(
        zombie_attribute_frame, text="血量", bootstyle=DANGER)
    zombie_hp_frame.grid(row=2, column=4, columnspan=8, sticky=W)
    zombie_hp_frame.grid_columnconfigure(0, minsize=50)
    ttk.Label(zombie_hp_frame, text="本体:").grid(row=0, column=0)
    zombie_hp_value = ttk.IntVar(zombie_hp_frame)
    zombie_hp_entry = ttk.Entry(
        zombie_hp_frame, textvariable=zombie_hp_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    zombie_hp_entry.grid(row=0, column=1, ipady=0)

    def setZombieHP(event):
        zombie_select.setHP(zombie_hp_value.get())
        zombie_hp_frame.focus_set()
    zombie_hp_entry.bind("<Return>", setZombieHP)
    zombie_hatHP_label = ttk.Label(zombie_hp_frame, text="帽子:")
    zombie_hatHP_label.grid(row=1, column=0)
    zombie_hatHP_value = ttk.IntVar(zombie_hp_frame)
    zombie_hatHP_entry = ttk.Entry(
        zombie_hp_frame, textvariable=zombie_hatHP_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    zombie_hatHP_entry.grid(row=1, column=1, ipady=0)

    def setZombieHatHP(event):
        zombie_select.setHatHP(zombie_hatHP_value.get())
        zombie_hp_frame.focus_set()
    zombie_hatHP_entry.bind("<Return>", setZombieHatHP)
    ttk.Label(zombie_hp_frame, text="铁门:").grid(row=2, column=0, padx=(2, 0))
    zombie_doorHP_value = ttk.IntVar(zombie_hp_frame)
    zombie_doorHP_entry = ttk.Entry(
        zombie_hp_frame, textvariable=zombie_doorHP_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    zombie_doorHP_entry.grid(row=2, column=1, ipady=0)

    def setZombieDoorHP(event):
        zombie_select.setDoorHP(zombie_doorHP_value.get())
        zombie_hp_frame.focus_set()
    zombie_doorHP_entry.bind("<Return>", setZombieDoorHP)
    zombie_control_frame = ttk.LabelFrame(
        zombie_attribute_frame, text="控制时间", bootstyle=DANGER)
    zombie_control_frame.grid(row=3, column=0, columnspan=3, sticky=W)
    ttk.Label(zombie_control_frame, text="减速:").grid(row=0, column=0)
    zombie_slow_value = ttk.IntVar(zombie_control_frame)
    zombie_slow_entry = ttk.Entry(
        zombie_control_frame, textvariable=zombie_slow_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    zombie_slow_entry.grid(row=0, column=1, ipady=0)

    def setZombieSlow(event):
        zombie_select.setSlow(zombie_slow_value.get())
        zombie_control_frame.focus_set()
    zombie_slow_entry.bind("<Return>", setZombieSlow)
    zombie_butter_label = ttk.Label(zombie_control_frame, text="黄油:")
    zombie_butter_label.grid(row=1, column=0)
    zombie_butter_value = ttk.IntVar(zombie_control_frame)
    zombie_butter_entry = ttk.Entry(
        zombie_control_frame, textvariable=zombie_butter_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    zombie_butter_entry.grid(row=1, column=1, ipady=0)

    def setZombieButter(event):
        zombie_select.setButter(zombie_butter_value.get())
        zombie_control_frame.focus_set()
    zombie_butter_entry.bind("<Return>", setZombieButter)
    ttk.Label(zombie_control_frame, text="冻结:").grid(
        row=2, column=0, padx=(2, 0))
    zombie_frozen_value = ttk.IntVar(zombie_control_frame)
    zombie_frozen_entry = ttk.Entry(
        zombie_control_frame, textvariable=zombie_frozen_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    zombie_frozen_entry.grid(row=2, column=1, ipady=0)

    def setZombieFrozen(event):
        zombie_select.setFrozen(zombie_frozen_value.get())
        zombie_control_frame.focus_set()
    zombie_frozen_entry.bind("<Return>", setZombieFrozen)
    zombie_flag_frame = ttk.LabelFrame(
        zombie_attribute_frame, text="状态标志", bootstyle=DANGER)
    zombie_flag_frame.grid(row=3, column=3, columnspan=8, sticky=W)
    zombie_exist_flag = ttk.BooleanVar(zombie_flag_frame)

    def change_zombie_exist():
        if (zombie_exist_flag.get() == False):
            zombie_select.setExist(2)
    ttk.Checkbutton(zombie_flag_frame, text="存在", bootstyle="danger-round-toggle",
                    variable=zombie_exist_flag, command=lambda: change_zombie_exist()).grid(row=0, column=0)
    zombie_isVisible_flag = ttk.BooleanVar(zombie_flag_frame)

    def change_zombie_isVisible():
        zombie_select.setIsVisible(not zombie_isVisible_flag.get())
    ttk.Checkbutton(zombie_flag_frame, text="隐形", bootstyle="danger-round-toggle",
                    variable=zombie_isVisible_flag, command=lambda: change_zombie_isVisible()).grid(row=0, column=1)
    zombie_isEating_flag = ttk.BooleanVar(zombie_flag_frame)

    def change_zombie_isEating():
        zombie_select.setIsEating(zombie_isEating_flag.get())
    ttk.Checkbutton(zombie_flag_frame, text="啃咬", bootstyle="danger-round-toggle",
                    variable=zombie_isEating_flag, command=lambda: change_zombie_isEating()).grid(row=1, column=0)
    zombie_isHpynotized_flag = ttk.BooleanVar(zombie_flag_frame)

    def change_zombie_isHpynotized():
        zombie_select.setIsHPynotized(zombie_isHpynotized_flag.get())
    ttk.Checkbutton(zombie_flag_frame, text="魅惑", bootstyle="danger-round-toggle",
                    variable=zombie_isHpynotized_flag, command=lambda: change_zombie_isHpynotized()).grid(row=1, column=1)
    zombie_isBlow_flag = ttk.BooleanVar(zombie_flag_frame)

    def change_zombie_isBlow():
        zombie_select.setIsBlow(zombie_isBlow_flag.get())
    ttk.Checkbutton(zombie_flag_frame, text="吹飞", bootstyle="danger-round-toggle",
                    variable=zombie_isBlow_flag, command=lambda: change_zombie_isBlow()).grid(row=2, column=0)
    zombie_isDying_flag = ttk.BooleanVar(zombie_flag_frame)

    def change_zombie_isDying():
        zombie_select.setIsDying(not zombie_isDying_flag.get())
    ttk.Checkbutton(zombie_flag_frame, text="濒死", bootstyle="danger-round-toggle",
                    variable=zombie_isDying_flag, command=lambda: change_zombie_isDying()).grid(row=2, column=1)

    zombie_put_frame = ttk.LabelFrame(
        zombie_page, text="放置僵尸", bootstyle=DANGER)
    zombie_put_frame.place(x=280, y=0, anchor=NW, height=120, width=130)
    ttk.Label(zombie_put_frame, text="第").grid(row=0, column=0)
    zombiePut_start_row_value = ttk.IntVar(zombie_put_frame)
    zombiePut_start_row_combobox = ttk.Combobox(zombie_put_frame, textvariable=zombiePut_start_row_value, width=2, values=[
                                                1, 2, 3, 4, 5, 6], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    zombiePut_start_row_combobox.grid(row=0, column=1)
    zombiePut_start_row_value.set(1)
    ttk.Label(zombie_put_frame, text="行").grid(row=0, column=2)
    zombiePut_start_col_value = ttk.IntVar(zombie_put_frame)
    zombiePut_start_col_combobox = ttk.Combobox(zombie_put_frame, textvariable=zombiePut_start_col_value, width=2, values=[
                                                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    zombiePut_start_col_combobox.grid(row=0, column=3)
    zombiePut_start_col_value.set(1)
    ttk.Label(zombie_put_frame, text="列").grid(row=0, column=4)
    ttk.Label(zombie_put_frame, text="至").grid(row=1, column=0)
    zombiePut_end_row_value = ttk.IntVar(zombie_put_frame)
    zombiePut_end_row_combobox = ttk.Combobox(zombie_put_frame, textvariable=zombiePut_end_row_value, width=2, values=[
                                              1, 2, 3, 4, 5, 6], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    zombiePut_end_row_combobox.grid(row=1, column=1)
    zombiePut_end_row_value.set(1)
    ttk.Label(zombie_put_frame, text="行").grid(row=1, column=2)
    zombiePut_end_col_value = ttk.IntVar(zombie_put_frame)
    zombiePut_end_col_combobox = ttk.Combobox(zombie_put_frame, textvariable=zombiePut_end_col_value, width=2, values=[
                                              1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    zombiePut_end_col_combobox.grid(row=1, column=3)
    zombiePut_end_col_value.set(1)
    ttk.Label(zombie_put_frame, text="列").grid(row=1, column=4)
    zombiePut_type_combobox = ttk.Combobox(zombie_put_frame, width=15, values=data.zombiesType, font=(
        "黑体", 8), bootstyle=SECONDARY, state=READONLY)
    zombiePut_type_combobox.grid(row=2, column=0, columnspan=4, sticky=W)
    zombiePut_type_combobox.current(0)
    zombiePut_num = ttk.IntVar(zombie_put_frame)
    zombiePut_num_entry = ttk.Entry(
        zombie_put_frame, textvariable=zombiePut_num, font=("黑体", 8), width=7)
    zombiePut_num_entry.grid(row=3, column=0, columnspan=2, sticky=W)
    ttk.Label(zombie_put_frame, text="只").grid(row=3, column=2)
    zombiePut_num.set(1)

    def putZombies(type, num):
        for _ in range(0, num):
            startRow = zombiePut_start_row_value.get()-1
            startCol = zombiePut_start_col_value.get()-1
            endRow = zombiePut_end_row_value.get()-1
            endCol = zombiePut_end_col_value.get()-1
            if (type == 25):
                pvz.putBoss
            print(startRow, startCol, endRow, endCol, type)
            if (pvz.getMap != False):
                rows = pvz.getMap()-1
                if startRow > rows:
                    startRow = rows
                if endRow > rows:
                    endRow = rows
                if startRow > endRow or startCol > endCol:
                    Messagebox.show_error("起始行列大于终止行列", title="输入错误")
                else:
                    for i in range(startRow, endRow+1):
                        for j in range(startCol, endCol+1):
                            pvz.putZombie(i, j, type)
    ttk.Button(zombie_put_frame, text="放置僵尸", padding=0, bootstyle=(OUTLINE, DANGER), command=lambda: putZombies(
        zombiePut_type_combobox.current(), zombiePut_num.get())).grid(row=3, column=0, columnspan=5, sticky=E)

    zombie_seed_frame = ttk.LabelFrame(
        zombie_page, text="修改出怪", bootstyle=DANGER)
    zombie_seed_frame.place(x=280, y=130, anchor=NW, height=100, width=130)
    pausee_spawn_status = ttk.BooleanVar(zombie_seed_frame)
    pausee_spawn_check = ttk.Checkbutton(zombie_seed_frame, text="暂停刷怪", variable=pausee_spawn_status,
                                         bootstyle="success-round-toggle", command=lambda: pvz.pauseSpawn(pausee_spawn_status.get()))
    pausee_spawn_check.grid(row=0, column=0, sticky=W)

    # zombie_characteristic_frame=ttk.Labelframe(zombie_page,text="基础属性",bootstyle=DANGER)
    # zombie_characteristic_frame.place(x=280,y=210,anchor=NW,height=200,width=150)

    zombie_spoils_frame = ttk.LabelFrame(
        zombie_page, text="击杀掉落", bootstyle=DANGER)
    zombie_spoils_frame.place(x=0, y=260, anchor=NW, height=200, width=275)
    spoil_1_percent = ttk.IntVar(zombie_spoils_frame)
    spoil_1_percent_spinbox = ttk.Spinbox(
        zombie_spoils_frame, from_=0, to=100, width=3, textvariable=spoil_1_percent)
    spoil_1_percent_spinbox.grid(row=1, column=0)
    ttk.Label(zombie_spoils_frame, text="%").grid(row=1, column=1)
    spoil_1_combobox = ttk.Combobox(zombie_spoils_frame, width=8, values=[
                                    "无", "银币", "金币", "钻石", "中阳光", "小阳光", "大阳光", "奖杯", "纸条", "植物卡片", "潜艇伟伟迷"], state=READONLY)
    spoil_1_combobox.grid(row=1, column=2)
    spoil_1_combobox.current(0)
    spoil_1_card = ttk.Combobox(
        zombie_spoils_frame, width=12, values=data.plantsType)
    spoil_1_card.insert(0, "选择植物")
    spoil_1_card.configure(state=DISABLED)
    spoil_1_card.grid(row=1, column=3)

    def setCard1(event):
        if (spoil_1_combobox.current() == 9):
            spoil_1_card.configure(state=READONLY)
        else:
            spoil_1_card.configure(state=DISABLED)
    spoil_1_combobox.bind("<<ComboboxSelected>>", setCard1)
    spoil_2_percent = ttk.IntVar(zombie_spoils_frame)
    spoil_2_percent_spinbox = ttk.Spinbox(
        zombie_spoils_frame, from_=0, to=100, width=3, textvariable=spoil_2_percent)
    spoil_2_percent_spinbox.grid(row=2, column=0)
    ttk.Label(zombie_spoils_frame, text="%").grid(row=2, column=1)
    spoil_2_combobox = ttk.Combobox(zombie_spoils_frame, width=8, values=[
                                    "无", "银币", "金币", "钻石", "中阳光", "小阳光", "大阳光", "奖杯", "纸条", "植物卡片", "潜艇伟伟迷"], state=READONLY)
    spoil_2_combobox.grid(row=2, column=2)
    spoil_2_combobox.current(0)
    spoil_2_card = ttk.Combobox(
        zombie_spoils_frame, width=12, values=data.plantsType)
    spoil_2_card.insert(0, "选择植物")
    spoil_2_card.configure(state=DISABLED)
    spoil_2_card.grid(row=2, column=3)

    def setCard2(event):
        if (spoil_2_combobox.current() == 9):
            spoil_2_card.configure(state=READONLY)
        else:
            spoil_2_card.configure(state=DISABLED)
    spoil_2_combobox.bind("<<ComboboxSelected>>", setCard2)
    spoil_3_percent = ttk.IntVar(zombie_spoils_frame)
    spoil_3_percent_spinbox = ttk.Spinbox(
        zombie_spoils_frame, from_=0, to=100, width=3, textvariable=spoil_3_percent)
    spoil_3_percent_spinbox.grid(row=3, column=0)
    ttk.Label(zombie_spoils_frame, text="%").grid(row=3, column=1)
    spoil_3_combobox = ttk.Combobox(zombie_spoils_frame, width=8, values=[
                                    "无", "银币", "金币", "钻石", "中阳光", "小阳光", "大阳光", "奖杯", "纸条", "植物卡片", "潜艇伟伟迷"], state=READONLY)
    spoil_3_combobox.grid(row=3, column=2)
    spoil_3_combobox.current(0)
    spoil_3_card = ttk.Combobox(
        zombie_spoils_frame, width=12, values=data.plantsType)
    spoil_3_card.insert(0, "选择植物")
    spoil_3_card.configure(state=DISABLED)
    spoil_3_card.grid(row=3, column=3)

    def setCard3(event):
        if (spoil_3_combobox.current() == 9):
            spoil_3_card.configure(state=READONLY)
        else:
            spoil_3_card.configure(state=DISABLED)
    spoil_3_combobox.bind("<<ComboboxSelected>>", setCard3)
    spoil_4_percent = ttk.IntVar(zombie_spoils_frame)
    spoil_4_percent_spinbox = ttk.Spinbox(
        zombie_spoils_frame, from_=0, to=100, width=3, textvariable=spoil_4_percent)
    spoil_4_percent_spinbox.grid(row=4, column=0)
    ttk.Label(zombie_spoils_frame, text="%").grid(row=4, column=1)
    spoil_4_combobox = ttk.Combobox(zombie_spoils_frame, width=8, values=[
                                    "无", "银币", "金币", "钻石", "中阳光", "小阳光", "大阳光", "奖杯", "纸条", "植物卡片", "潜艇伟伟迷"], state=READONLY)
    spoil_4_combobox.grid(row=4, column=2)
    spoil_4_combobox.current(0)
    spoil_4_card = ttk.Combobox(
        zombie_spoils_frame, width=12, values=data.plantsType)
    spoil_4_card.insert(0, "选择植物")
    spoil_4_card.configure(state=DISABLED)
    spoil_4_card.grid(row=4, column=3)

    def setCard4(event):
        if (spoil_4_combobox.current() == 9):
            spoil_4_card.configure(state=READONLY)
        else:
            spoil_4_card.configure(state=DISABLED)
    spoil_4_combobox.bind("<<ComboboxSelected>>", setCard4)
    spoils_card_frame = ttk.Frame(zombie_spoils_frame)
    spoils_card_frame.grid(row=5, column=0)

    def load_spoils_config():
        config = load_config(config_file_path)
        try:
            spoil_1_percent.set(config["spoils"]["spoil1"]["percent"])
        except:
            pass
        try:
            spoil_1_combobox.current(config["spoils"]["spoil1"]["type"])
        except:
            pass
        try:
            spoil_1_card.current(config["spoils"]["spoil1"]["card"])
        except:
            pass
        try:
            spoil_2_percent.set(config["spoils"]["spoil2"]["percent"])
        except:
            pass
        try:
            spoil_2_combobox.current(config["spoils"]["spoil2"]["type"])
        except:
            pass
        try:
            spoil_2_card.current(config["spoils"]["spoil2"]["card"])
        except:
            pass
        try:
            spoil_3_percent.set(config["spoils"]["spoil3"]["percent"])
        except:
            pass
        try:
            spoil_3_combobox.current(config["spoils"]["spoil3"]["type"])
        except:
            pass
        try:
            spoil_3_card.current(config["spoils"]["spoil3"]["card"])
        except:
            pass
        try:
            spoil_4_percent.set(config["spoils"]["spoil4"]["percent"])
        except:
            pass
        try:
            spoil_4_combobox.current(config["spoils"]["spoil4"]["type"])
        except:
            pass
        try:
            spoil_4_card.current(config["spoils"]["spoil4"]["card"])
        except:
            pass
    load_spoils_config()

    def setSpoils():
        if (zombie_spoils_status.get()):
            config = load_config(config_file_path)
            if "spoils" not in config:
                config["spoils"] = {}
            spoils_config = list()
            if "spoil1" not in config["spoils"]:
                config["spoils"]["spoil1"] = {}
            config["spoils"]["spoil1"]["percent"] = spoil_1_percent.get()
            config["spoils"]["spoil1"]["type"] = spoil_1_combobox.current()
            config["spoils"]["spoil1"]["card"] = spoil_1_card.current()
            if (spoil_1_percent.get() != 0 and spoil_1_combobox.current() != 0):
                spoils_config.append(config["spoils"]["spoil1"])
            if "spoil2" not in config["spoils"]:
                config["spoils"]["spoil2"] = {}
            config["spoils"]["spoil2"]["percent"] = spoil_2_percent.get()
            config["spoils"]["spoil2"]["type"] = spoil_2_combobox.current()
            config["spoils"]["spoil2"]["card"] = spoil_2_card.current()
            if (spoil_2_percent.get() != 0 and spoil_2_combobox.current() != 0):
                spoils_config.append(config["spoils"]["spoil2"])
            if "spoil3" not in config["spoils"]:
                config["spoils"]["spoil3"] = {}
            config["spoils"]["spoil3"]["percent"] = spoil_3_percent.get()
            config["spoils"]["spoil3"]["type"] = spoil_3_combobox.current()
            config["spoils"]["spoil3"]["card"] = spoil_3_card.current()
            if (spoil_3_percent.get() != 0 and spoil_3_combobox.current() != 0):
                spoils_config.append(config["spoils"]["spoil3"])
            if "spoil4" not in config["spoils"]:
                config["spoils"]["spoil4"] = {}
            config["spoils"]["spoil4"]["percent"] = spoil_4_percent.get()
            config["spoils"]["spoil4"]["type"] = spoil_4_combobox.current()
            config["spoils"]["spoil4"]["card"] = spoil_4_card.current()
            if (spoil_4_percent.get() != 0 and spoil_4_combobox.current() != 0):
                spoils_config.append(config["spoils"]["spoil4"])
            save_config(config, config_file_path)
            pvz.spoils(spoils_config)
        else:
            pvz.spoils(False)

    zombie_spoils_status = ttk.BooleanVar(zombie_spoils_frame)
    zombie_spoils_check = ttk.Checkbutton(zombie_spoils_frame, text="开启", variable=zombie_spoils_status,
                                          bootstyle="success-round-toggle", command=lambda: setSpoils())
    zombie_spoils_check.grid(row=5, column=0, columnspan=4, sticky=W)
    # ttk.Label(zombie_spoils_frame,text="卡片").grid(row=5,column=0)
    # spoil_card_combobox=ttk.Combobox(zombie_spoils_frame,width=8,values=data.plantsType,state=READONLY)
    # spoil_card_combobox.grid(row=5,column=1)
    # def setSpoilCard(event):
    #     data.PVZ_memory.write_int(0x0042FFB9,spoil_card_combobox.current())
    # spoil_card_combobox.bind("<<ComboboxSelected>>",setSpoilCard)

    def get_zombie_select(event):
        global zombie_select
        try:
            index = int(zombie_list_box.selection()[0])
            zombie_select = zombie_list[index]
        except:
            return

    def get_zombie_attribute():
        global zombie_select
        if zombie_select != None:
            try:
                zombie_type_value.set(
                    str(zombie_select.type)+":"+data.zombiesType[zombie_select.type])
                if (zombie_attribute_frame.focus_get() != zombie_state_entry):
                    zombie_state_value.set(zombie_select.state)
                if (zombie_attribute_frame.focus_get() != zombie_size_entry):
                    zombie_size_value.set(zombie_select.size)
                if (zombie_attribute_frame.focus_get() != zombie_x_entry):
                    zombie_x_value.set(round(zombie_select.x, 2))
                if (zombie_attribute_frame.focus_get() != zombie_y_entry):
                    zombie_y_value.set(round(zombie_select.y, 2))
                zombie_row_value.set(zombie_select.row)
                if (zombie_attribute_frame.focus_get() != zombie_hp_entry):
                    zombie_hp_value.set(zombie_select.hp)
                if (zombie_select.hatType == 0):
                    zombie_hatHP_label["text"] = "无:"
                elif (zombie_select.hatType == 1):
                    zombie_hatHP_label["text"] = "路障:"
                elif (zombie_select.hatType == 2):
                    zombie_hatHP_label["text"] = "铁桶:"
                elif (zombie_select.hatType == 3):
                    zombie_hatHP_label["text"] = "橄榄帽:"
                elif (zombie_select.hatType == 4):
                    zombie_hatHP_label["text"] = "矿工帽:"
                elif (zombie_select.hatType == 7):
                    zombie_hatHP_label["text"] = "雪橇车:"
                elif (zombie_select.hatType == 8):
                    zombie_hatHP_label["text"] = "坚果:"
                elif (zombie_select.hatType == 9):
                    zombie_hatHP_label["text"] = "高冰果:"
                elif (zombie_select.hatType == 10):
                    zombie_hatHP_label["text"] = "钢盔:"
                elif (zombie_select.hatType == 11):
                    zombie_hatHP_label["text"] = "绿帽:"
                else:
                    zombie_hatHP_label["text"] = str(
                        zombie_select.hatType)+"未知:"
                if (zombie_attribute_frame.focus_get() != zombie_hatHP_entry):
                    zombie_hatHP_value.set(zombie_select.hatHP)
                if (zombie_attribute_frame.focus_get() != zombie_doorHP_entry):
                    zombie_doorHP_value.set(zombie_select.doorHP)
                if (zombie_attribute_frame.focus_get() != zombie_slow_entry):
                    zombie_slow_value.set(zombie_select.slow)
                if (zombie_attribute_frame.focus_get() != zombie_butter_entry):
                    zombie_butter_value.set(zombie_select.butter)
                if (zombie_attribute_frame.focus_get() != zombie_frozen_entry):
                    zombie_frozen_value.set(zombie_select.frozen)
                if (zombie_select.exist == 0):
                    zombie_exist_flag.set(True)
                else:
                    zombie_exist_flag.set(False)
            except:
                pass
            zombie_isVisible_flag.set(not zombie_select.isVisible)
            zombie_isEating_flag.set(zombie_select.isEating)
            zombie_isHpynotized_flag.set(zombie_select.isHpynotized)
            zombie_isBlow_flag.set(zombie_select.isBlow)
            zombie_isDying_flag.set(not zombie_select.isDying)

    zombie_list_box.bind("<<TreeviewSelect>>", get_zombie_select)

    plant_page = ttk.Frame(page_tab)
    plant_page.pack()
    page_tab.add(plant_page, text="植物修改")
    plant_list_frame = ttk.LabelFrame(
        plant_page, text="植物列表", bootstyle=SUCCESS)
    plant_list_frame.place(x=0, y=0, anchor=NW, height=390, width=235)
    plant_list_box_scrollbar = ttk.Scrollbar(
        plant_list_frame, bootstyle=SUCCESS)
    plant_list_box = ttk.Treeview(plant_list_frame, show=TREE, selectmode=BROWSE, padding=0, columns=(
        "plant_list"), yscrollcommand=plant_list_box_scrollbar.set, bootstyle=SUCCESS)
    plant_list_box_scrollbar.configure(command=plant_list_box.yview)
    plant_list_box.place(x=0, y=0, anchor=NW, height=370, width=50)
    plant_list_box_scrollbar.place(x=45, y=0, height=370, anchor=NW)
    plant_list = list()

    def refresh_plant_list():
        plant_list.clear()
        plant_list_box.delete(*plant_list_box.get_children())
        try:
            plant_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xbc)
        except:
            return
        i = 0
        j = 0
        while i < plant_num:
            plant_addresss = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xac)+0x204*j
            plant_exist = data.PVZ_memory.read_bytes(plant_addresss+0x141, 1)
            if (plant_exist == b'\x00'):
                plant_list.append(data.plant(plant_addresss))
                i = i+1
            j = j+1
        n = 0
        for k in range(plant_num):
            plant_list_box.insert("", END, iid=n, text=str(plant_list[k].no))
            if (plant_select != None):
                if (plant_select.exist == 0):
                    if (plant_select.no == plant_list[k].no):
                        plant_list_box.selection_set((str(n),))
            n = n+1

    refresh_plant_list()
    plant_attribute_frame = ttk.Frame(plant_list_frame)
    plant_attribute_frame.place(x=80, y=0, height=370, width=150)
    plant_state_frame = ttk.Frame(plant_attribute_frame)
    plant_state_frame.grid(row=0, column=0, columnspan=12, sticky=W)
    ttk.Label(plant_state_frame, text="植物类型:").grid(
        row=0, column=0, columnspan=2, sticky=W)
    plant_type_value = ttk.IntVar(plant_state_frame)
    plant_type_entry = ttk.Entry(plant_state_frame, textvariable=plant_type_value, width=12, font=(
        "黑体", 8), state=READONLY, bootstyle=SECONDARY)
    plant_type_entry.grid(row=0, column=2, columnspan=5, sticky=W)
    ttk.Label(plant_state_frame, text="状态:").grid(row=1, column=0, sticky=W)
    plant_state_value = ttk.IntVar(plant_state_frame)
    plant_state_entry = ttk.Entry(
        plant_state_frame, textvariable=plant_state_value, width=3, font=("黑体", 8), bootstyle=SECONDARY)
    plant_state_entry.grid(row=1, column=1, sticky=W)

    def setPlantState(event):
        plant_select.setState(plant_state_value.get())
        plant_state_frame.focus_set()
    plant_state_entry.bind("<Return>", setPlantState)
    plant_position_frame = ttk.LabelFrame(
        plant_attribute_frame, text="位置", bootstyle=SUCCESS)
    plant_position_frame.grid(row=2, column=0, columnspan=4, sticky=W)
    ttk.Label(plant_position_frame, text="x坐标:").grid(
        row=0, column=0, columnspan=3, sticky=W)
    plant_x_value = ttk.IntVar(plant_position_frame)
    plant_x_entry = ttk.Entry(plant_position_frame, textvariable=plant_x_value, width=6, font=(
        "黑体", 8), bootstyle=SECONDARY)
    plant_x_entry.grid(row=0, column=3, columnspan=3, sticky=W)

    def setPlantX(event):
        print(plant_x_value.get())
        plant_select.setX(plant_x_value.get())
        plant_position_frame.focus_set()
    plant_x_entry.bind("<Return>", setPlantX)
    ttk.Label(plant_position_frame, text="y坐标:").grid(
        row=1, column=0, columnspan=3, sticky=W)
    plant_y_value = ttk.IntVar(plant_position_frame)
    plant_y_entry = ttk.Entry(plant_position_frame, textvariable=plant_y_value, width=6, font=(
        "黑体", 8), bootstyle=SECONDARY)
    plant_y_entry.grid(row=1, column=3, columnspan=3, sticky=W)

    def setPlantY(event):
        plant_select.setY(plant_y_value.get())
        plant_position_frame.focus_set()
    plant_y_entry.bind("<Return>", setPlantY)
    plant_row_value = ttk.IntVar(plant_position_frame)
    plant_row_combobox = ttk.Combobox(plant_position_frame, textvariable=plant_row_value, width=2, values=[
                                      1, 2, 3, 4, 5, 6], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    plant_row_combobox.grid(row=2, column=1, columnspan=3, sticky=W)
    ttk.Label(plant_position_frame, text="行").grid(row=2, column=4, sticky=W)

    def setPlantRow(event):
        plant_select.setRow(plant_row_value.get())
        plant_position_frame.focus_set()
    plant_row_combobox.bind("<<ComboboxSelected>>", setPlantRow)
    plant_col_value = ttk.IntVar(plant_position_frame)
    plant_col_combobox = ttk.Combobox(plant_position_frame, textvariable=plant_col_value, width=2, values=[
                                      1, 2, 3, 4, 5, 6, 7, 8, 9], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    plant_col_combobox.grid(row=2, column=5, columnspan=3, sticky=W)
    ttk.Label(plant_position_frame, text="列").grid(row=2, column=8, sticky=W)

    def setPlantCol(event):
        plant_select.setCol(plant_col_value.get())
        plant_position_frame.focus_set()
    plant_col_combobox.bind("<<ComboboxSelected>>", setPlantCol)
    ttk.Label(plant_state_frame, text="血量:").grid(row=1, column=3)
    plant_hp_value = ttk.IntVar(plant_state_frame)
    plant_hp_entry = ttk.Entry(plant_state_frame, textvariable=plant_hp_value, width=5, font=(
        "黑体", 8), bootstyle=SECONDARY)
    plant_hp_entry.grid(row=1, column=4, ipady=0)

    def setPlantHP(event):
        plant_select.setHP(plant_hp_value.get())
        plant_state_frame.focus_set()
    plant_hp_entry.bind("<Return>", setPlantHP)
    plant_time_frame = ttk.LabelFrame(
        plant_attribute_frame, text="倒计时", bootstyle=SUCCESS)
    plant_time_frame.grid(row=3, column=0, columnspan=3, sticky=W)
    plant_dietime_label = ttk.Label(plant_time_frame, text="死亡:")
    plant_dietime_label.grid(row=0, column=0)
    ToolTip(plant_dietime_label, text="部分具有存在时间植物死亡倒计时",
            bootstyle=(INFO, INVERSE))
    plant_dietime_value = ttk.IntVar(plant_time_frame)
    plant_dietime_entry = ttk.Entry(
        plant_time_frame, textvariable=plant_dietime_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    plant_dietime_entry.grid(row=0, column=1, ipady=0)

    def setPlantDieTime(event):
        plant_select.setDieTime(plant_dietime_value.get())
        plant_time_frame.focus_set()
    plant_dietime_entry.bind("<Return>", setPlantDieTime)
    plant_cindertime_label = ttk.Label(plant_time_frame, text="灰烬:")
    plant_cindertime_label.grid(row=1, column=0)
    ToolTip(plant_cindertime_label, text="部分灰烬生效、女大消失倒计时",
            bootstyle=(INFO, INVERSE))
    plant_cindertime_value = ttk.IntVar(plant_time_frame)
    plant_cindertime_entry = ttk.Entry(
        plant_time_frame, textvariable=plant_cindertime_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    plant_cindertime_entry.grid(row=1, column=1, ipady=0)

    def setPlantCinderTime(event):
        plant_select.setCinderTime(plant_cindertime_value.get())
        plant_time_frame.focus_set()
    plant_cindertime_entry.bind("<Return>", setPlantCinderTime)
    plant_effecttime_label = ttk.Label(plant_time_frame, text="效果:")
    plant_effecttime_label.grid(row=2, column=0, padx=(2, 0))
    ToolTip(plant_effecttime_label, text="部分植物变大、产生效果倒计时",
            bootstyle=(INFO, INVERSE))
    plant_effecttime_value = ttk.IntVar(plant_time_frame)
    plant_effecttime_entry = ttk.Entry(
        plant_time_frame, textvariable=plant_effecttime_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    plant_effecttime_entry.grid(row=2, column=1, ipady=0)

    def setPlantEffectTime(event):
        plant_select.setEffectTime(plant_effecttime_value.get())
        plant_time_frame.focus_set()
    plant_effecttime_entry.bind("<Return>", setPlantEffectTime)
    plant_producttime_label = ttk.Label(plant_time_frame, text="攻击:")
    plant_producttime_label.grid(row=3, column=0, padx=(2, 0))
    ToolTip(plant_producttime_label, text="部分植物攻击倒计时",
            bootstyle=(INFO, INVERSE))
    plant_producttime_value = ttk.IntVar(plant_time_frame)
    plant_producttime_entry = ttk.Entry(
        plant_time_frame, textvariable=plant_producttime_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    plant_producttime_entry.grid(row=3, column=1, ipady=0)

    def setPlantProductTime(event):
        plant_select.setProductTime(plant_producttime_value.get())
        plant_time_frame.focus_set()
    plant_producttime_entry.bind("<Return>", setPlantProductTime)
    plant_productinterval_label = ttk.Label(plant_time_frame, text="间隔:")
    plant_productinterval_label.grid(row=4, column=0, padx=(2, 0))
    ToolTip(plant_productinterval_label,
            text="上述植物攻击间隔", bootstyle=(INFO, INVERSE))
    plant_productinterval_value = ttk.IntVar(plant_time_frame)
    plant_productinterval_entry = ttk.Entry(
        plant_time_frame, textvariable=plant_productinterval_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    plant_productinterval_entry.grid(row=4, column=1, ipady=0)

    def setPlantProductInterval(event):
        plant_select.setProductInterval(plant_productinterval_value.get())
        plant_time_frame.focus_set()
    plant_productinterval_entry.bind("<Return>", setPlantProductInterval)
    plant_attacktime_label = ttk.Label(plant_time_frame, text="射击:")
    plant_attacktime_label.grid(row=5, column=0, padx=(2, 0))
    ToolTip(plant_attacktime_label, text="部分植物攻击倒计时",
            bootstyle=(INFO, INVERSE))
    plant_attacktime_value = ttk.IntVar(plant_time_frame)
    plant_attacktime_entry = ttk.Entry(
        plant_time_frame, textvariable=plant_attacktime_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    plant_attacktime_entry.grid(row=5, column=1, ipady=0)

    def setPlantAttackTime(event):
        plant_select.setAttackTime(plant_attacktime_value.get())
        plant_time_frame.focus_set()
    plant_attacktime_entry.bind("<Return>", setPlantAttackTime)
    plant_suntime_label = ttk.Label(plant_time_frame, text="阳光:")
    plant_suntime_label.grid(row=6, column=0, padx=(2, 0))
    ToolTip(plant_suntime_label, text="女王产生阳光倒计时", bootstyle=(INFO, INVERSE))
    plant_suntime_value = ttk.IntVar(plant_time_frame)
    plant_suntime_entry = ttk.Entry(
        plant_time_frame, textvariable=plant_suntime_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    plant_suntime_entry.grid(row=6, column=1, ipady=0)

    def setPlantSunTime(event):
        plant_select.setSunTime(plant_suntime_value.get())
        plant_time_frame.focus_set()
    plant_suntime_entry.bind("<Return>", setPlantSunTime)
    plant_humtime_label = ttk.Label(plant_time_frame, text="阳光:")
    plant_humtime_label.grid(row=7, column=0, padx=(2, 0))
    ToolTip(plant_humtime_label, text="汉堡王产生阳光倒计时", bootstyle=(INFO, INVERSE))
    plant_humtime_value = ttk.IntVar(plant_time_frame)
    plant_humtime_entry = ttk.Entry(
        plant_time_frame, textvariable=plant_humtime_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    plant_humtime_entry.grid(row=7, column=1, ipady=0)

    def setPlantHumTime(event):
        plant_select.setHumTime(plant_humtime_value.get())
        plant_time_frame.focus_set()
    plant_humtime_entry.bind("<Return>", setPlantHumTime)
    plant_flag_frame = ttk.LabelFrame(
        plant_attribute_frame, text="状态标志", bootstyle=SUCCESS)
    plant_flag_frame.grid(row=3, column=3, columnspan=8, sticky=W)
    plant_exist_flag = ttk.BooleanVar(plant_flag_frame)

    def change_plant_exist():
        plant_select.setExist(not plant_exist_flag.get())
    ttk.Checkbutton(plant_flag_frame, text="存在", bootstyle="success-round-toggle",
                    variable=plant_exist_flag, command=lambda: change_plant_exist()).grid(row=0, column=0)
    plant_isVisible_flag = ttk.BooleanVar(plant_flag_frame)

    def change_plant_isVisible():
        plant_select.setIsVisible(not plant_isVisible_flag.get())
    ttk.Checkbutton(plant_flag_frame, text="隐形", bootstyle="success-round-toggle",
                    variable=plant_isVisible_flag, command=lambda: change_plant_isVisible()).grid(row=1, column=0)
    plant_isAttack_flag = ttk.BooleanVar(plant_flag_frame)

    def change_plant_isAttack():
        plant_select.setIsAttack(plant_isAttack_flag.get())
    ttk.Checkbutton(plant_flag_frame, text="攻击", bootstyle="success-round-toggle",
                    variable=plant_isAttack_flag, command=lambda: change_plant_isAttack()).grid(row=2, column=0)
    plant_isSquash_flag = ttk.BooleanVar(plant_flag_frame)

    def change_plant_isSquash():
        plant_select.setIsSquash(plant_isSquash_flag.get())
    ttk.Checkbutton(plant_flag_frame, text="压扁", bootstyle="success-round-toggle",
                    variable=plant_isSquash_flag, command=lambda: change_plant_isSquash()).grid(row=3, column=0)
    plant_isSleep_flag = ttk.BooleanVar(plant_flag_frame)

    def change_plant_isSleep():
        plant_select.setIsSleep(plant_isSleep_flag.get())
    ttk.Checkbutton(plant_flag_frame, text="睡眠", bootstyle="success-round-toggle",
                    variable=plant_isSleep_flag, command=lambda: change_plant_isSleep()).grid(row=4, column=0)

    plant_put_frame = ttk.LabelFrame(plant_page, text="种植", bootstyle=SUCCESS)
    plant_put_frame.place(x=240, y=0, anchor=NW, height=120, width=130)
    ttk.Label(plant_put_frame, text="第").grid(row=0, column=0)
    plantPut_start_row_value = ttk.IntVar(plant_put_frame)
    plantPut_start_row_combobox = ttk.Combobox(plant_put_frame, textvariable=plantPut_start_row_value, width=2, values=[
                                               1, 2, 3, 4, 5, 6], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    plantPut_start_row_combobox.grid(row=0, column=1)
    plantPut_start_row_value.set(1)
    ttk.Label(plant_put_frame, text="行").grid(row=0, column=2)
    plantPut_start_col_value = ttk.IntVar(plant_put_frame)
    plantPut_start_col_combobox = ttk.Combobox(plant_put_frame, textvariable=plantPut_start_col_value, width=2, values=[
                                               1, 2, 3, 4, 5, 6, 7, 8, 9], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    plantPut_start_col_combobox.grid(row=0, column=3)
    plantPut_start_col_value.set(1)
    ttk.Label(plant_put_frame, text="列").grid(row=0, column=4)
    ttk.Label(plant_put_frame, text="至").grid(row=1, column=0)
    plantPut_end_row_value = ttk.IntVar(plant_put_frame)
    plantPut_end_row_combobox = ttk.Combobox(plant_put_frame, textvariable=plantPut_end_row_value, width=2, values=[
                                             1, 2, 3, 4, 5, 6], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    plantPut_end_row_combobox.grid(row=1, column=1)
    plantPut_end_row_value.set(1)
    ttk.Label(plant_put_frame, text="行").grid(row=1, column=2)
    plantPut_end_col_value = ttk.IntVar(plant_put_frame)
    plantPut_end_col_combobox = ttk.Combobox(plant_put_frame, textvariable=plantPut_end_col_value, width=2, values=[
                                             1, 2, 3, 4, 5, 6, 7, 8, 9], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    plantPut_end_col_combobox.grid(row=1, column=3)
    plantPut_end_col_value.set(1)
    ttk.Label(plant_put_frame, text="列").grid(row=1, column=4)
    plantPut_type_combobox = ttk.Combobox(plant_put_frame, width=10, values=data.plantPutType, font=(
        "黑体", 8), bootstyle=SECONDARY, state=READONLY)
    plantPut_type_combobox.grid(row=2, column=0, columnspan=4, sticky=W)
    plantPut_type_combobox.current(0)

    def putPlants(type):
        startRow = plantPut_start_row_value.get()-1
        startCol = plantPut_start_col_value.get()-1
        endRow = plantPut_end_row_value.get()-1
        endCol = plantPut_end_col_value.get()-1
        if (type >= 52):
            type = type+23
        print(startRow, startCol, endRow, endCol, type)
        if (pvz.getMap != False):
            rows = pvz.getMap()-1
            if startRow > rows:
                startRow = rows
            if endRow > rows:
                endRow = rows
            if startRow > endRow or startCol > endCol:
                Messagebox.show_error("起始行列大于终止行列", title="输入错误")
            else:
                for i in range(startRow, endRow+1):
                    for j in range(startCol, endCol+1):
                        pvz.putPlant(i, j, type)
    ttk.Button(plant_put_frame, text="种植", padding=0, bootstyle=(OUTLINE, SUCCESS), command=lambda: putPlants(
        plantPut_type_combobox.current())).grid(row=2, column=0, columnspan=5, sticky=E)

    def clearPlants():
        try:
            plant_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xbc)
        except:
            return
        i = 0
        j = 0
        while i < plant_num:
            plant_addresss = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xac)+0x204*j
            plant_exist = data.PVZ_memory.read_bytes(plant_addresss+0x141, 1)
            if (plant_exist == b'\x00'):
                data.PVZ_memory.write_bytes(plant_addresss+0x141, b'\x01', 1)
                i = i+1
            j = j+1
    ttk.Button(plant_put_frame, text="清空所有植物", padding=0, bootstyle=(OUTLINE, SUCCESS),
               command=lambda: clearPlants()).grid(row=3, column=0, columnspan=5, pady=(5, 0), sticky=W)

    plant_characteristic_frame = ttk.Labelframe(
        plant_page, text="基础属性", bootstyle=SUCCESS)
    plant_characteristic_frame.place(
        x=240, y=130, anchor=NW, height=140, width=130)
    plant_type_combobox = ttk.Combobox(plant_characteristic_frame, width=10, values=data.plantsType, font=(
        "黑体", 8), bootstyle=SECONDARY, state=READONLY)
    plant_type_combobox.grid(row=0, column=0, columnspan=4, sticky=W)
    ttk.Label(plant_characteristic_frame, text="阳光:").grid(row=1, column=0)
    plant_characteristic_sun_value = ttk.IntVar(plant_characteristic_frame)
    plant_characteristic_sun_entry = ttk.Entry(
        plant_characteristic_frame, textvariable=plant_characteristic_sun_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    plant_characteristic_sun_entry.grid(row=1, column=1, ipady=0)

    def setPlantCharacteristicSun(event):
        plant_characteristic_type.setSun(plant_characteristic_sun_value.get())
        plant_characteristic_frame.focus_set()
    plant_characteristic_sun_entry.bind("<Return>", setPlantCharacteristicSun)
    plant_characteristic_cd_label = ttk.Label(
        plant_characteristic_frame, text="冷却:")
    plant_characteristic_cd_label.grid(row=2, column=0)
    plant_characteristic_cd_value = ttk.IntVar(plant_characteristic_frame)
    plant_characteristic_cd_entry = ttk.Entry(
        plant_characteristic_frame, textvariable=plant_characteristic_cd_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    plant_characteristic_cd_entry.grid(row=2, column=1, ipady=0)

    def setPlantCharacteristicCd(event):
        plant_characteristic_type.setCd(plant_characteristic_cd_value.get())
        plant_characteristic_frame.focus_set()
    plant_characteristic_cd_entry.bind("<Return>", setPlantCharacteristicCd)
    plant_characteristic_canAttack_flag = ttk.BooleanVar(plant_flag_frame)

    def change_plant_characteristic_canAttack():
        plant_characteristic_type.setCanAttack(
            plant_characteristic_canAttack_flag.get())
    ttk.Checkbutton(plant_characteristic_frame, text="可攻击", bootstyle="success-round-toggle", variable=plant_characteristic_canAttack_flag,
                    command=lambda: change_plant_characteristic_canAttack()).grid(row=3, column=0, columnspan=4)
    ttk.Label(plant_characteristic_frame, text="攻击间隔:").grid(row=4, column=0)
    plant_characteristic_attackinterval_value = ttk.IntVar(
        plant_characteristic_frame)
    plant_characteristic_attackinterval_entry = ttk.Entry(
        plant_characteristic_frame, textvariable=plant_characteristic_attackinterval_value, width=5, font=("黑体", 8), bootstyle=SECONDARY)
    plant_characteristic_attackinterval_entry.grid(row=4, column=1, ipady=0)

    def setPlantCharacteristicAttackInterval(event):
        plant_characteristic_type.setAttackInterval(
            plant_characteristic_attackinterval_value.get())
        plant_characteristic_frame.focus_set()
    plant_characteristic_attackinterval_entry.bind(
        "<Return>", setPlantCharacteristicAttackInterval)

    def get_plant_type(event):
        global plant_characteristic_type
        plant_characteristic_type = data.plantCharacteristic(
            plant_type_combobox.current())
        plant_characteristic_sun_value.set(plant_characteristic_type.sun)
        plant_characteristic_cd_value.set(plant_characteristic_type.cd)
        plant_characteristic_attackinterval_value.set(
            plant_characteristic_type.attackInterval)
        plant_characteristic_canAttack_flag.set(
            plant_characteristic_type.canAttack)
        plant_characteristic_frame.focus_set()
    plant_type_combobox.bind("<<ComboboxSelected>>", get_plant_type)

    bullet_frame = ttk.Labelframe(
        plant_page, text="子弹修改", bootstyle=SUCCESS)
    bullet_frame.place(
        x=0, y=390, anchor=NW, height=120, width=300)
    all_bullet_frame = ttk.Frame(bullet_frame)
    all_bullet_frame.pack(anchor=W)
    all_bullet_status = ttk.BooleanVar(all_bullet_frame)
    bullet_type_combobox = ttk.Combobox(all_bullet_frame, width=10, values=data.bulletType, font=(
        "黑体", 8), bootstyle=SECONDARY, state=READONLY)
    bullet_type_combobox.pack(side=RIGHT)
    bullet_type_combobox.current(0)
    ttk.Checkbutton(all_bullet_frame, variable=all_bullet_status, text="修改所有子弹为",
                    bootstyle="success-round-toggle", command=lambda: pvz.setAllBullet(all_bullet_status.get(), bullet_type_combobox.current())).pack(side=RIGHT)
    random_bullet_frame = ttk.Frame(bullet_frame)
    random_bullet_frame.pack(anchor=W)
    random_bullet_hasPepper = ttk.BooleanVar(random_bullet_frame)
    ttk.Checkbutton(random_bullet_frame, text="辣椒",
                    variable=random_bullet_hasPepper).pack(side=RIGHT)
    random_bullet_hasMine = ttk.BooleanVar(random_bullet_frame)
    ttk.Checkbutton(random_bullet_frame, text="土豆雷",
                    variable=random_bullet_hasMine).pack(side=RIGHT)
    random_bullet_hasDoom = ttk.BooleanVar(random_bullet_frame)
    ttk.Checkbutton(random_bullet_frame, text="毁灭菇",
                    variable=random_bullet_hasDoom).pack(side=RIGHT)
    ttk.Label(random_bullet_frame, text="包含").pack(side=RIGHT)
    random_bullet_status = ttk.BooleanVar(random_bullet_frame)
    ttk.Checkbutton(random_bullet_frame, variable=random_bullet_status, text="随机所有子弹",
                    bootstyle="success-round-toggle", command=lambda: pvz.randomBullet(random_bullet_status.get(), random_bullet_hasDoom.get(), random_bullet_hasMine.get(), random_bullet_hasPepper.get())).pack(side=RIGHT)
    attack_speed_frame = ttk.Frame(bullet_frame)
    attack_speed_frame.pack(anchor=W)
    attack_speed_label = ttk.Label(attack_speed_frame, text="植物攻速倍率:")
    attack_speed_label.pack(side=LEFT)
    ToolTip(attack_speed_label,
            text="过高会导致植物无法攻击", bootstyle=(INFO, INVERSE))
    attack_speed_multiple = ttk.IntVar(attack_speed_frame)
    attack_speed_multiple.set(1)
    attack_speed_entry = ttk.Entry(attack_speed_frame, font=("黑体", 8), width=3,
                                   textvariable=attack_speed_multiple)
    attack_speed_entry.pack(side=LEFT)
    attack_animation_status = ttk.BooleanVar(attack_speed_frame)
    attack_animation_check = ttk.Checkbutton(attack_speed_frame, variable=attack_animation_status, text="攻击无视动画",
                                             bootstyle="success-round-toggle", command=lambda: pvz.cancelAttackAnimation(attack_animation_status.get()))
    attack_animation_check.pack(side=LEFT)
    ToolTip(attack_animation_check,
            text="部分植物有效，可无视动画进行攻击，提高攻速上限", bootstyle=(INFO, INVERSE))
    bullet_size_frame = ttk.Frame(bullet_frame)
    bullet_size_frame.pack(anchor=W)
    bullet_size = ttk.IntVar(bullet_size_frame)
    bullet_size_entry = ttk.Entry(bullet_size_frame, width=3, textvariable=bullet_size, font=(
        "黑体", 8), bootstyle=SECONDARY)
    bullet_size_entry.pack(side=RIGHT)
    bullet_size.set(1)
    bullet_size_status = ttk.BooleanVar(bullet_size_frame)
    ttk.Checkbutton(bullet_size_frame, variable=bullet_size_status, text="修改子弹大小倍数(正整数)",
                    bootstyle="success-round-toggle", command=lambda: pvz.setBulletSize(bullet_size_status.get(), bullet_size.get())).pack(side=RIGHT)

    def setAttackSpeed(event):
        pvz.setAttackSpeed(attack_speed_multiple.get())
        attack_speed_frame.focus_set()
    attack_speed_entry.bind("<Return>", setAttackSpeed)

    plant_bullet_frame = ttk.Labelframe(
        plant_page, text="植物子弹修改", bootstyle=SUCCESS)
    plant_bullet_frame.place(
        x=370, y=0, anchor=NW, height=150, width=100)
    plant_type_bullet_combobox = ttk.Combobox(plant_bullet_frame, width=10, values=data.plantsType, font=(
        "黑体", 8), bootstyle=SECONDARY)
    plant_type_bullet_combobox.pack()
    plant_type_bullet_combobox.insert(0, '选择植物')
    plant_type_bullet_combobox.config(state=READONLY)
    plant_bullet_status = ttk.BooleanVar(plant_bullet_frame)
    plantBulletMode = ttk.IntVar(plant_bullet_frame)
    ttk.Checkbutton(plant_bullet_frame, variable=plant_bullet_status, text="修改子弹为",
                    bootstyle="success-round-toggle", command=lambda: pvz.setPlantBullet(plant_bullet_status.get(), plant_type_bullet_combobox.current(), plant_bullet_type_combobox.current(), plantBulletMode.get())).pack()
    plant_bullet_type_combobox = ttk.Combobox(plant_bullet_frame, width=10, values=data.bulletType, font=(
        "黑体", 8), bootstyle=SECONDARY, state=READONLY)
    plant_bullet_type_combobox.pack()
    plant_bullet_type_combobox.current(0)
    plant_bullet_mode_frame = ttk.Frame(plant_bullet_frame)
    plant_bullet_mode_frame.pack()
    ttk.Radiobutton(plant_bullet_mode_frame, text="普通", value=0, variable=plantBulletMode, bootstyle=PRIMARY,
                    command=lambda: pvz.setDifficult(gameDifficult.get())).grid(row=0, column=0, padx=2)
    ttk.Radiobutton(plant_bullet_mode_frame, text="慢速", value=8, variable=plantBulletMode, bootstyle=PRIMARY,
                    command=lambda: pvz.setDifficult(gameDifficult.get())).grid(row=0, column=1, padx=2)
    ttk.Radiobutton(plant_bullet_mode_frame, text="追踪", value=9, variable=plantBulletMode, bootstyle=PRIMARY,
                    command=lambda: pvz.setDifficult(gameDifficult.get())).grid(row=1, column=0, padx=2)
    ttk.Radiobutton(plant_bullet_mode_frame, text="反向", value=6, variable=plantBulletMode, bootstyle=PRIMARY,
                    command=lambda: pvz.setDifficult(gameDifficult.get())).grid(row=1, column=1, padx=2)
    plantBulletMode.set(0)

    def get_plant_select(event):
        global plant_select
        try:
            index = int(plant_list_box.selection()[0])
            plant_select = plant_list[index]
        except:
            return

    def get_plant_attribute():
        global plant_select
        if plant_select != None:
            try:
                plant_type_value.set(
                    str(plant_select.type)+":"+data.plantsType[plant_select.type])
                if (plant_attribute_frame.focus_get() != plant_state_entry):
                    plant_state_value.set(plant_select.state)
                if (plant_attribute_frame.focus_get() != plant_x_entry):
                    plant_x_value.set(plant_select.x)
                if (plant_attribute_frame.focus_get() != plant_y_entry):
                    plant_y_value.set(plant_select.y)
                plant_row_value.set(plant_select.row)
                plant_col_value.set(plant_select.col)
                if (plant_attribute_frame.focus_get() != plant_hp_entry):
                    plant_hp_value.set(plant_select.hp)
                if (plant_attribute_frame.focus_get() != plant_dietime_entry):
                    plant_dietime_value.set(plant_select.dieTime)
                if (plant_attribute_frame.focus_get() != plant_cindertime_entry):
                    plant_cindertime_value.set(plant_select.cinderTime)
                if (plant_attribute_frame.focus_get() != plant_effecttime_entry):
                    plant_effecttime_value.set(plant_select.effectTime)
                if (plant_attribute_frame.focus_get() != plant_producttime_entry):
                    plant_producttime_value.set(plant_select.productTime)
                if (plant_attribute_frame.focus_get() != plant_attacktime_entry):
                    plant_attacktime_value.set(plant_select.attackTime)
                if (plant_attribute_frame.focus_get() != plant_productinterval_entry):
                    plant_productinterval_value.set(
                        plant_select.productInterval)
                if (plant_attribute_frame.focus_get() != plant_suntime_entry):
                    plant_suntime_value.set(plant_select.sunTime)
                if (plant_attribute_frame.focus_get() != plant_humtime_entry):
                    plant_humtime_value.set(plant_select.humTime)
            except:
                pass
            plant_isVisible_flag.set(not plant_select.isVisible)
            plant_exist_flag.set(not plant_select.exist)
            plant_isAttack_flag.set(plant_select.isAttack)
            plant_isSquash_flag.set(plant_select.isSquash)
            plant_isSleep_flag.set(plant_select.isSleep)

    plant_list_box.bind("<<TreeviewSelect>>", get_plant_select)

    grid_page = ttk.Frame(page_tab)
    grid_page.pack()
    page_tab.add(grid_page, text="场地修改")
    item_list_frame = ttk.LabelFrame(grid_page, text="物品列表", bootstyle=DARK)
    item_list_frame.place(x=0, y=0, anchor=NW, height=140, width=200)
    item_list_box_scrollbar = ttk.Scrollbar(item_list_frame, bootstyle=DARK)
    item_list_box = ttk.Treeview(item_list_frame, show=TREE, selectmode=BROWSE, padding=0, columns=(
        "item_list"), yscrollcommand=item_list_box_scrollbar.set, bootstyle=DARK)
    item_list_box_scrollbar.configure(command=item_list_box.yview)
    item_list_box.place(x=0, y=0, anchor=NW, height=120, width=70)
    item_list_box_scrollbar.place(x=65, y=0, height=120, anchor=NW)
    item_list = list()

    def refresh_item_list():
        item_list.clear()
        item_list_box.delete(*item_list_box.get_children())
        try:
            item_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x12c)
        except:
            return
        i = 0
        j = 0
        while i < item_num:
            item_addresss = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x11c)+0xec*j
            item_exist = data.PVZ_memory.read_bytes(item_addresss+0x20, 1)
            if (item_exist == b'\x00'):
                item_list.append(data.item(item_addresss))
                i = i+1
            j = j+1
        n = 0
        for k in range(item_num):
            item_list_box.insert("", END, iid=n, text=str(
                item_list[k].no)+data.itemType[item_list[k].type])
            if (item_select != None):
                if (item_select.exist == 0):
                    if (item_select.no == item_list[k].no):
                        item_list_box.selection_set((str(n),))
            n = n+1
    refresh_item_list()
    item_attribute_frame = ttk.Frame(item_list_frame)
    item_attribute_frame.place(x=80, y=0, height=120, width=115)
    item_exist_flag = ttk.BooleanVar(item_attribute_frame)

    def change_item_exist():
        item_select.setExist(not item_exist_flag.get())
    ttk.Checkbutton(item_attribute_frame, text="存在", bootstyle="dark-round-toggle", variable=item_exist_flag,
                    command=lambda: change_item_exist()).grid(row=0, column=0, columnspan=4, sticky=W)
    item_row_value = ttk.IntVar(item_attribute_frame)
    item_row_combobox = ttk.Combobox(item_attribute_frame, textvariable=item_row_value, width=2, values=[
                                     1, 2, 3, 4, 5, 6], font=("黑体", 8), bootstyle=SECONDARY)
    item_row_combobox.grid(row=1, column=0)
    ttk.Label(item_attribute_frame, text="行").grid(row=1, column=1)

    def setItemRow(event):
        item_select.setRow(item_row_value.get())
        item_attribute_frame.focus_set()
    item_row_combobox.bind("<<ComboboxSelected>>", setItemRow)
    item_col_value = ttk.IntVar(item_attribute_frame)
    item_col_combobox = ttk.Combobox(item_attribute_frame, textvariable=item_col_value, width=2, values=[
                                     1, 2, 3, 4, 5, 6, 7, 8, 9], font=("黑体", 8), bootstyle=SECONDARY)
    item_col_combobox.grid(row=1, column=2)
    ttk.Label(item_attribute_frame, text="列").grid(row=1, column=3)

    def setItemCol(event):
        item_select.setCol(item_col_value.get())
        item_attribute_frame.focus_set()
    item_col_combobox.bind("<<ComboboxSelected>>", setItemCol)
    item_time_value = ttk.IntVar(item_attribute_frame)

    def setItemTime(event):
        item_select.setTime(item_time_meter.amountusedvar.get())
        item_attribute_frame.focus_set()
    item_time_meter = ttk.Meter(item_attribute_frame, metersize=80, bootstyle=DARK, amounttotal=18000, showtext=True,
                                metertype="semi", interactive=True, textfont="-size 7", subtext="剩余时间", subtextfont="-size 7", subtextstyle="dark")

    def setItemTimeMeterFocus(event):
        item_time_meter.focus_set()
    item_time_meter.indicator.bind("<Button-1>", setItemTimeMeterFocus)
    item_time_meter.indicator.bind("<ButtonRelease-1>", setItemTime)

    def clearLadders():
        try:
            item_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x12c)
        except:
            return
        i = 0
        j = 0
        while i < item_num:
            item_addresss = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x11c)+0xec*j
            item_exist = data.PVZ_memory.read_bytes(item_addresss+0x20, 1)
            if (item_exist == b'\x00'):
                data.PVZ_memory.write_bytes(item_addresss+0x20, b'\x01', 1)
                i = i+1
            j = j+1

    ladder_put_frame = ttk.LabelFrame(grid_page, text="搭梯", bootstyle=DARK)
    ladder_put_frame.place(x=200, y=0, anchor=NW, height=90, width=130)
    ttk.Label(ladder_put_frame, text="第").grid(row=0, column=0)
    ladder_start_row_value = ttk.IntVar(ladder_put_frame)
    item_start_row_combobox = ttk.Combobox(ladder_put_frame, textvariable=ladder_start_row_value, width=2, values=[
                                           1, 2, 3, 4, 5, 6], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    item_start_row_combobox.grid(row=0, column=1)
    ladder_start_row_value.set(1)
    ttk.Label(ladder_put_frame, text="行").grid(row=0, column=2)
    ladder_start_col_value = ttk.IntVar(ladder_put_frame)
    item_start_col_combobox = ttk.Combobox(ladder_put_frame, textvariable=ladder_start_col_value, width=2, values=[
                                           1, 2, 3, 4, 5, 6, 7, 8, 9], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    item_start_col_combobox.grid(row=0, column=3)
    ladder_start_col_value.set(1)
    ttk.Label(ladder_put_frame, text="列").grid(row=0, column=4)
    ttk.Label(ladder_put_frame, text="至").grid(row=1, column=0)
    ladder_end_row_value = ttk.IntVar(ladder_put_frame)
    item_end_row_combobox = ttk.Combobox(ladder_put_frame, textvariable=ladder_end_row_value, width=2, values=[
                                         1, 2, 3, 4, 5, 6], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    item_end_row_combobox.grid(row=1, column=1)
    ladder_end_row_value.set(1)
    ttk.Label(ladder_put_frame, text="行").grid(row=1, column=2)
    ladder_end_col_value = ttk.IntVar(ladder_put_frame)
    item_end_col_combobox = ttk.Combobox(ladder_put_frame, textvariable=ladder_end_col_value, width=2, values=[
                                         1, 2, 3, 4, 5, 6, 7, 8, 9], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    item_end_col_combobox.grid(row=1, column=3)
    ladder_end_col_value.set(1)
    ttk.Label(ladder_put_frame, text="列").grid(row=1, column=4)

    def putLadders():
        startRow = ladder_start_row_value.get()-1
        startCol = ladder_start_col_value.get()-1
        endRow = ladder_end_row_value.get()-1
        endCol = ladder_end_col_value.get()-1
        print(startRow, startCol, endRow, endCol)
        if (pvz.getMap != False):
            rows = pvz.getMap()-1
            if startRow > rows:
                startRow = rows
            if endRow > rows:
                endRow = rows
            if startRow > endRow or startCol > endCol:
                Messagebox.show_error("起始行列大于终止行列", title="输入错误")
            else:
                for i in range(startRow, endRow+1):
                    for j in range(startCol, endCol+1):
                        pvz.putLadder(i, j)
    ttk.Button(ladder_put_frame, text="搭梯", padding=0, bootstyle=(OUTLINE, DARK),
               command=lambda: putLadders()).grid(row=2, column=0, columnspan=5, sticky=E)

    car_frame = ttk.LabelFrame(grid_page, text="小车", bootstyle=DANGER)
    car_frame.place(x=330, y=0, anchor=NW, height=120, width=160)
    start_car_value = ttk.IntVar(ladder_put_frame)
    start_car_combobox = ttk.Combobox(car_frame, textvariable=start_car_value, width=5, values=[
        1, 2, 3, 4, 5, 6, '全部'], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    start_car_combobox.grid(row=0, column=0)
    start_car_combobox.current(6)

    def startCar():
        rows = pvz.getMap()
        if (rows == False):
            return
        else:
            if (start_car_combobox.current() == 6):
                try:
                    car_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                        data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x110)
                except:
                    return
                i = 0
                j = 0
                start_car_list = [0]*rows
                while i < car_num:
                    car_addresss = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                        data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x100)+0x48*j
                    car_exist = data.PVZ_memory.read_bytes(
                        car_addresss+0x30, 1)
                    if (car_exist == b'\x00'):
                        try:
                            c = data.car(car_addresss)
                            if (start_car_list[c.row] == 0):
                                pvz.startCar(car_addresss)
                                start_car_list[c.row] = 1
                        except:
                            pass
                        i = i+1
                    j = j+1

            elif (start_car_combobox.current() > rows-1):
                return
            else:
                try:
                    car_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                        data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x110)
                except:
                    return
                i = 0
                j = 0
                while i < car_num:
                    car_addresss = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                        data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x100)+0x48*j
                    car_exist = data.PVZ_memory.read_bytes(
                        car_addresss+0x30, 1)
                    if (car_exist == b'\x00'):
                        c = data.car(car_addresss)
                        if (c.row == start_car_combobox.current()):
                            pvz.startCar(car_addresss)
                            return
                        i = i+1
                    j = j+1
    ttk.Button(car_frame, text="启动小车", padding=0, bootstyle=(OUTLINE, DANGER),
               command=lambda: startCar()).grid(row=0, column=1)
    recover_car_value = ttk.IntVar(ladder_put_frame)
    recover_car_combobox = ttk.Combobox(car_frame, textvariable=recover_car_value, width=5, values=[
        1, 2, 3, 4, 5, 6, '全部'], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    recover_car_combobox.grid(row=1, column=0)
    recover_car_combobox.current(6)

    def recoveryCar():
        rows = pvz.getMap()
        if (rows == False):
            return
        else:
            if (recover_car_combobox.current() == 6):
                pass
            elif (recover_car_combobox.current() > rows-1):
                return
            pvz.recoveryCars()
            try:
                car_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                    data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x110)
            except:
                return
            if (recover_car_combobox.current() < 6):
                i = 0
                j = 0
                delete_car_list = [0]*rows
                print(delete_car_list)
                delete_car_list[recover_car_combobox.current()] = 1
                while i < car_num:
                    car_addresss = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                        data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x100)+0x48*j
                    car_exist = data.PVZ_memory.read_bytes(
                        car_addresss+0x30, 1)
                    if (car_exist == b'\x00'):
                        c = data.car(car_addresss)
                        try:
                            if (c.row != recover_car_combobox.current() and delete_car_list[c.row] == 0):
                                print(c.row)
                                print(delete_car_list)
                                c.setExist(True)
                                delete_car_list[c.row] = 1
                        except:
                            pass
                        i = i+1
                    j = j+1
    ttk.Button(car_frame, text="恢复小车", padding=0, bootstyle=(OUTLINE, DANGER),
               command=lambda: recoveryCar()).grid(row=1, column=1)
    endless_car_status = ttk.BooleanVar()
    ttk.Checkbutton(car_frame, text="无尽小车", variable=endless_car_status, padding=0, bootstyle="danger-round-toggle",
                    command=lambda: pvz.endlessCar(endless_car_status.get())).grid(row=2, column=1)
    init_car_status = ttk.BooleanVar()
    ttk.Checkbutton(car_frame, text="初始有车", variable=init_car_status, padding=0, bootstyle="danger-round-toggle",
                    command=lambda: pvz.initCar(init_car_status.get())).grid(row=3, column=0)
    auto_car_status = ttk.BooleanVar()
    ttk.Checkbutton(car_frame, text="自动补车", variable=auto_car_status, padding=0, bootstyle="danger-round-toggle",
                    command=lambda: pvz.autoCar(auto_car_status.get())).grid(row=3, column=1)

    def get_item_select(event):
        global item_select
        try:
            index = int(item_list_box.selection()[0])
            item_select = item_list[index]
        except:
            return

    def get_item_attribute():
        global item_select
        if item_select != None:
            item_exist_flag.set(not item_select.exist)
            item_row_value.set(item_select.row)
            item_col_value.set(item_select.col)
            if (item_select.type == 2):
                try:
                    if (item_attribute_frame.focus_get() != item_time_meter):
                        item_time_value.set(item_select.time)
                        item_time_meter.grid(row=2, column=0, columnspan=4)
                        item_time_meter.configure(
                            amountused=item_time_value.get())
                except:
                    pass
            else:
                item_time_meter.grid_forget()

    item_list_box.bind("<<TreeviewSelect>>", get_item_select)

    formation_frame = ttk.LabelFrame(grid_page, text="布阵", bootstyle=SUCCESS)
    formation_frame.place(x=0, y=140)
    # 设置字体
    small_font = ('黑体', 8)

    # 场地数据和梯子属性
    plants_data = [[[] for _ in range(9)] for _ in range(6)]
    ladders_data = [[0 for _ in range(9)] for _ in range(6)]

    # 更新场地格子显示的植物类型

    def update_field():
        for i, row in enumerate(plants_data):
            for j, indices in enumerate(row):
                text = '\n'.join([data.plantsType[index]
                                 for index in indices]) if indices else ''
                buttons[i][j].config(
                    text=text, bg='gray' if ladders_data[i][j] else '#90ee90')

    # 管理植物类型的窗口

    def manage_plants(i, j):
        formation_plant_window = ttk.Toplevel(formation_frame)
        formation_plant_window.title('管理植物')
        formation_plant_window.geometry("200x300")

        main_window_x = main_window.winfo_x()
        main_window_y = main_window.winfo_y()
        formation_plant_window.geometry(
            f'+{main_window_x+150}+{main_window_y + 150}')
        # 列表框
        listbox = Listbox(formation_plant_window, height=10, font=small_font)
        listbox.pack()

        # 将已有植物类型添加到列表框
        for index in plants_data[i][j]:
            listbox.insert(tk.END, data.plantsType[index])

        # Combobox
        combobox = ttk.Combobox(
            formation_plant_window, values=data.plantsType, font=small_font)
        combobox.pack()

        # 梯子属性复选框
        ladder_check = IntVar(value=ladders_data[i][j])
        ladder_checkbox = Checkbutton(
            formation_plant_window, text='是否有梯子', variable=ladder_check)
        ladder_checkbox.pack()

        # 添加植物类型
        def add_plant():
            selected_plant = combobox.get()
            if selected_plant in data.plantsType:
                index = data.plantsType.index(selected_plant)
                plants_data[i][j].append(index)
                listbox.insert(tk.END, selected_plant)

        # 删除选中的植物类型
        def delete_plant():
            selections = listbox.curselection()
            if selections:
                for index in selections[::-1]:
                    del plants_data[i][j][listbox.index(index)]
                    listbox.delete(index)
        button_frame = ttk.Frame(formation_plant_window)
        button_frame.pack()
        # 添加按钮
        add_button = ttk.Button(button_frame, text='添加',
                                command=add_plant)
        add_button.pack(side=LEFT, padx=10, pady=5)

        # 删除按钮
        delete_button = ttk.Button(button_frame, text='删除',
                                   command=delete_plant, bootstyle=DANGER)
        delete_button.pack(side=LEFT, padx=10, pady=5)

        # 更新并关闭窗口
        def close_and_update():
            # 更新梯子属性
            ladders_data[i][j] = ladder_check.get()
            update_field()
            formation_plant_window.destroy()

        # 完成按钮
        done_button = ttk.Button(formation_plant_window, text='完成',
                                 command=close_and_update, bootstyle=SUCCESS)
        done_button.pack()

    # 创建场地格子按钮
    buttons = [[tk.Label(formation_frame, text='', width=9, height=4, font=small_font, borderwidth=2,
                         relief='groove', bg='#90ee90') for j in range(9)] for i in range(6)]
    for i in range(6):
        for j in range(9):
            buttons[i][j].grid(row=i, column=j, padx=1, pady=1, sticky='nsew')
            buttons[i][j].bind('<Button-1>', lambda e, i=i,
                               j=j: manage_plants(i, j))
    update_field()

    # 保存场地数据到 JSON 文件

    def creat_formation_config(plants_data, ladders_data):
        if (new_formation_config_entry.get() == ""):
            Messagebox.show_error("请输入阵型名称", title="创建阵型失败")
        else:
            config = load_config(config_file_path)
            if "formation" not in config:
                config["formation"] = {}
            if new_formation_config_entry.get() not in config["formation"]:
                config["formation"][new_formation_config_entry.get()] = {}
            config["formation"][new_formation_config_entry.get()
                                ]['plants'] = plants_data
            config["formation"][new_formation_config_entry.get()
                                ]['ladders'] = ladders_data
            save_config(config, config_file_path)
            Messagebox.show_info(
                "阵型”"+new_formation_config_entry.get()+"”已创建", title="创建阵型成功")
            update_formation_config_combobox()
            formation_config_combobox.set(new_formation_config_entry.get())

    def save_formation_config(plants_data, ladders_data):
        config = load_config(config_file_path)
        if "formation" not in config:
            config["formation"] = {}
        if formation_config_combobox.get() not in config["formation"]:
            Messagebox.show_error("阵型名称不存在，请先新建阵型", title="保存阵型失败")
        config["formation"][formation_config_combobox.get()
                            ]['plants'] = plants_data
        config["formation"][formation_config_combobox.get()
                            ]['ladders'] = ladders_data
        save_config(config, config_file_path)
        Messagebox.show_info(
            "阵型"+formation_config_combobox.get()+"”修改成功", title="修改阵型成功")

    # 创建保存和读取按钮
    formation_config_frame = ttk.Frame(formation_frame)
    formation_config_frame.grid(row=6, column=0, columnspan=9, pady=(10, 0))
    new_formation_config_entry = ttk.Entry(
        formation_config_frame, width=10, font=("宋体", 8))
    new_formation_config_entry.pack(side=LEFT, padx=2)
    new_formation_config_button = ttk.Button(formation_config_frame, text='新建阵型', bootstyle=SUCCESS, padding=0,
                                             command=lambda: creat_formation_config(plants_data, ladders_data))
    new_formation_config_button.pack(side=LEFT, padx=2)
    formation_config_combobox = ttk.Combobox(
        formation_config_frame, width=12, bootstyle='secondary', font=("宋体", 8))
    formation_config_combobox.pack(side=LEFT, padx=2)
    formation_config_combobox.insert(0, "选择阵型")
    formation_config_combobox.configure(state=READONLY)

    def update_formation_config_combobox():
        config = load_config(config_file_path)
        if "formation" not in config:
            return
        formation_config_combobox.configure(
            values=list(config['formation'].keys()))
    update_formation_config_combobox()

    def load_formation_config(event, plants_data, ladders_data):
        config = load_config(config_file_path)
        loaded_data = config["formation"][formation_config_combobox.get()]
        for i in range(6):
            for j in range(9):
                plants_data[i][j] = loaded_data['plants'][i][j]
                ladders_data[i][j] = loaded_data['ladders'][i][j]
        update_field()
    formation_config_combobox.bind(
        "<<ComboboxSelected>>", lambda event, plants=plants_data, ladders=ladders_data: load_formation_config(event, plants, ladders))
    load_formation_config_button = ttk.Button(
        formation_config_frame, text='修改配置', bootstyle=WARNING, padding=0, command=lambda: save_formation_config(plants_data, ladders_data))
    load_formation_config_button.pack(side=LEFT, padx=2)

    def delete_formation_config():
        config = load_config(config_file_path)
        if "formation" not in config:
            config["formation"] = {}
        if formation_config_combobox.get() not in config["formation"]:
            Messagebox.show_error("阵型名称不存在", title="删除阵型失败")
        del config["formation"][formation_config_combobox.get()]
        save_config(config, config_file_path)
        Messagebox.show_info(
            "阵型"+formation_config_combobox.get()+"”已删除", title="删除阵型成功")
        update_formation_config_combobox()
    delete_formation_button = ttk.Button(formation_config_frame, text='删除阵型',
                                         bootstyle=DANGER, padding=0, command=lambda: delete_formation_config())
    delete_formation_button.pack(side=LEFT, padx=2)

    def clear_grid():
        clearPlants()
        clearLadders()
    clear_game_grid = ttk.Button(formation_config_frame, text='清空游戏场地',
                                 bootstyle=DARK, padding=0, command=lambda: clear_grid())
    clear_game_grid.pack(side=LEFT, padx=2)

    def get_game_formation(plants_data, ladders_data):
        for r in range(0, 6):
            for c in range(0, 9):
                plants_data[r][c].clear()
                ladders_data[r][c] = 0
        try:
            plant_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xbc)
        except:
            return
        i = 0
        j = 0
        while i < plant_num:
            plant_addresss = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xac)+0x204*j
            plant_exist = data.PVZ_memory.read_bytes(plant_addresss+0x141, 1)
            if (plant_exist == b'\x00'):
                p = data.plant(plant_addresss)
                if (p.row > 5 or p.col > 8):
                    continue
                plants_data[p.row][p.col].append(p.type)
                i = i+1
            j = j+1
        try:
            item_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x12c)
        except:
            return
        i = 0
        j = 0
        while i < item_num:
            item_addresss = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x11c)+0xec*j
            item_exist = data.PVZ_memory.read_bytes(item_addresss+0x20, 1)
            if (item_exist == b'\x00'):
                it = data.item(item_addresss)
                if it.type == 3:
                    ladders_data[it.row-1][it.col-1] = 1
                i = i+1
            j = j+1
        update_field()
    get_game_formation_button = ttk.Button(
        formation_config_frame, text='从游戏加载', bootstyle=INFO, padding=0, command=lambda: get_game_formation(plants_data, ladders_data))
    get_game_formation_button.pack(side=LEFT, padx=2)

    def set_game_formation(plants_data, ladders_data):
        rols = pvz.getMap()
        if rols == False:
            Messagebox.show_error("请在关卡内使用", title="应用阵型失败")
            return
        for r in range(0, rols):
            for c in range(0, 9):
                for p in plants_data[r][c]:
                    pvz.putPlant(r, c, p)
                if ladders_data[r][c] == 1:
                    pvz.putLadder(r, c)

    set_game_formation_button = ttk.Button(
        formation_config_frame, text='应用到游戏', bootstyle=PRIMARY, padding=0, command=lambda: set_game_formation(plants_data, ladders_data))
    set_game_formation_button.pack(side=LEFT, padx=2)

    slot_page = ttk.Frame(page_tab)
    slot_page.pack()
    page_tab.add(slot_page, text="卡槽修改")
    slots_configuration_mode = ttk.BooleanVar(slot_page)
    slots_configuration_mode.set(False)
    slots_frame = ttk.LabelFrame(slot_page, text="监视模式", bootstyle=SUCCESS)
    slots_frame.place(x=0, y=0)
    slot_list = list()

    def refresh_slot_list():
        slot_list.clear()
        try:
            slot_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x144)+0x24)
        except:
            return
        i = 0
        while i < slot_num:
            slot_addresss = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x144)+0x28+0x50*i
            slot_list.append(data.slot(slot_addresss))
            i = i+1

    slot_type_comboboxes = []
    slot_elapsed_values = []
    slot_elapsed_entrys = []
    slot_cooldown_values = []
    slot_cooldown_entrys = []
    slot_cd_progressBars = []
    slot_isVisible_flags = []
    # slot_canUse_flags = []

    def create_slot_ui(slot_number):
        ttk.Label(slots_frame, text=f"{slot_number}").grid(
            row=slot_number-1, column=0, sticky=W)
        ttk.Label(slots_frame, text="植物:").grid(
            row=slot_number-1, column=1, sticky=W)

        slot_type_combobox = ttk.Combobox(
            slots_frame, width=12, values=data.plantsType, state='readonly', bootstyle='secondary')
        slot_type_combobox.grid(row=slot_number-1, column=2, sticky=W)
        slot_type_comboboxes.append(slot_type_combobox)

        def set_slot_type(event, index=slot_number-1):
            if (slots_configuration_mode.get() == False):
                slot_list[index].setType(slot_type_combobox.current())
                slots_frame.focus_set()
        slot_type_combobox.bind("<<ComboboxSelected>>", set_slot_type)

        slot_elapsed_value = ttk.IntVar()
        slot_elapsed_values.append(slot_elapsed_value)
        slot_elapsed_entry = ttk.Entry(
            slots_frame, textvariable=slot_elapsed_value, width=5, font=("黑体", 8), bootstyle='secondary')
        slot_elapsed_entrys.append(slot_elapsed_entry)

        def set_slot_elapsed(event, index=slot_number-1):
            if (slots_configuration_mode.get() == False):
                slot_list[index].setElapsed(slot_elapsed_value.get())
                slots_frame.focus_set()
        slot_elapsed_entry.bind("<Return>", set_slot_elapsed)

        slot_cooldown_value = ttk.IntVar()
        slot_cooldown_values.append(slot_cooldown_value)
        slot_cooldown_entry = ttk.Entry(
            slots_frame, textvariable=slot_cooldown_value, width=5, font=("黑体", 8), bootstyle='secondary')
        slot_cooldown_entrys.append(slot_cooldown_entry)

        def set_slot_cooldown(event, index=slot_number-1):
            if (slots_configuration_mode.get() == False):
                slot_list[index].setCooldown(slot_cooldown_value.get())
                slots_frame.focus_set()
        slot_cooldown_entry.bind("<Return>", set_slot_cooldown)

        slot_cooldown_label = ttk.Label(slots_frame, text="冷却进度")
        slot_cooldown_label.grid(row=slot_number-1, column=3, padx=(2, 0))
        slot_cd_progressBar = ttk.Progressbar(slots_frame, length=80, mode=DETERMINATE, maximum=slot_cooldown_value.get(
        ), variable=slot_elapsed_value, bootstyle="success-striped")
        slot_cd_progressBar.grid(row=slot_number-1, column=4, ipady=0)
        slot_cd_progressBars.append(slot_cd_progressBar)

        def set_cd_progressBar_focus(event):
            if (slots_configuration_mode.get() == False):
                slot_cd_progressBar.focus_set()

        def set_cd_value(event, index=slot_number-1):
            if (slots_configuration_mode.get() == False):
                fraction = event.x / slot_cd_progressBar.winfo_width()
                new_value = int(fraction * slot_cd_progressBar['maximum'])
                slot_elapsed_value.set(new_value)
                slot_list[index].setElapsed(slot_elapsed_value.get())
        slot_cd_progressBar.bind("<Button-1>", set_cd_progressBar_focus)
        slot_cd_progressBar.bind("<ButtonRelease-1>", set_cd_value)

        slot_isVisible_flag = ttk.BooleanVar(slots_frame)
        slot_isVisible_flags.append(slot_isVisible_flag)

        def change_slot_isVisible(index=slot_number-1):
            if (slots_configuration_mode.get() == False):
                slot_list[index].setIsVisible(not slot_isVisible_flag.get())
        ttk.Checkbutton(slots_frame, text="隐形", bootstyle="danger-round-toggle", variable=slot_isVisible_flag,
                        command=lambda: change_slot_isVisible()).grid(row=slot_number-1, column=5)
        # slot_canUse_flag=ttk.BooleanVar(slots_frame)
        # slot_canUse_flags.append(slot_canUse_flag)
        # def change_slot_canUse(index=slot_number-1):
        #     slot_list[index].setCanUse(slot_canUse_flag.get())
        # ttk.Checkbutton(slots_frame,text="可用",bootstyle="danger-round-toggle",variable=slot_canUse_flag,command=lambda:change_slot_canUse()).grid(row=slot_number-1,column=6)
    # 为slots 1至14创建UI组件
    for slot_number in range(1, 15):
        create_slot_ui(slot_number)

    slots_config_frame = ttk.LabelFrame(
        slot_page, text="卡槽设置", bootstyle=SUCCESS)
    slots_config_frame.place(x=0, y=0, relx=1, anchor=NE)
    slot_num_frame = ttk.Frame(slots_config_frame)
    slot_num_frame.pack()
    ttk.Label(slot_num_frame, text="卡槽格数：").pack(side=LEFT)
    slots_num_value = ttk.IntVar()
    slots_num_combobox = ttk.Combobox(slot_num_frame, textvariable=slots_num_value, width=2, values=[
                                      0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], font=("黑体", 8), bootstyle=SECONDARY, state=READONLY)
    slots_num_combobox.pack(side=LEFT)

    def setSlotsNum(event):
        data.PVZ_memory.write_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(
            data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x144)+0x24, slots_num_value.get())
        slot_num_frame.focus_set()
    slots_num_combobox.bind("<<ComboboxSelected>>", setSlotsNum)
    no_slot_status = ttk.BooleanVar(slots_config_frame)
    no_slot_check = ttk.Checkbutton(slots_config_frame, text="无需选卡", variable=no_slot_status,
                                    bootstyle="success-round-toggle", command=lambda: pvz.noSolt(no_slot_status.get()))
    no_slot_check.pack(pady=5, anchor=W)
    ToolTip(no_slot_check, text="可以不选卡片即开始游戏", bootstyle=(INFO, INVERSE))
    change_all_frame = ttk.Frame(slots_config_frame)
    change_all_frame.pack(pady=(0, 10))
    ttk.Label(change_all_frame, text="修改所有卡槽：").pack(anchor=W)
    change_all_combobox = ttk.Combobox(
        change_all_frame, width=12, values=data.plantsType, state='readonly', bootstyle='secondary')
    change_all_combobox.pack()
    random_slots_status = ttk.BooleanVar(slots_config_frame)
    random_slots_check = ttk.Checkbutton(slots_config_frame, text="卡槽随机变化", variable=random_slots_status,
                                         bootstyle="success-round-toggle", command=lambda: pvz.randomSlots(random_slots_status.get()))
    random_slots_check.pack(pady=5, anchor=W)

    def change_all_slots(event):
        if (slots_configuration_mode.get() == False):
            for slot in slot_list:
                slot.setType(change_all_combobox.current())
    change_all_combobox.bind("<<ComboboxSelected>>", change_all_slots)

    card_select_frame = ttk.LabelFrame(slot_page, text="选卡配置", bootstyle=DARK)
    card_select_frame.place(x=0, y=180, relx=1, anchor=NE)

    def changeSlotsConfiguration():
        if (slots_configuration_mode.get() == True):
            slots_frame.configure(text="配置模式", bootstyle=DARK)
        else:
            slots_frame.configure(text="监视模式", bootstyle=SUCCESS)
    slots_configuration_change = ttk.Checkbutton(
        card_select_frame, text="配置模式", variable=slots_configuration_mode, bootstyle="dark-round-toggle", command=lambda: changeSlotsConfiguration())
    slots_configuration_change.pack()
    ToolTip(slots_configuration_change,
            text="开启后左侧卡槽进入配置模式，可以配置选卡方案", bootstyle=(INFO, INVERSE))
    # card_select_combobox = ttk.Combobox(card_select_frame, width=12, values=data.plantsType, state='readonly', bootstyle='secondary')
    # card_select_combobox.pack()
    # ttk.Button(card_select_frame,text="选卡",command=lambda:pvz.selectCard(card_select_combobox.current())).pack()
    # ttk.Button(card_select_frame,text="退卡",command=lambda:pvz.deselectCard(card_select_combobox.current())).pack()
    new_solts_config_frame = ttk.Frame(card_select_frame)
    new_solts_config_frame.pack()
    new_solts_config_entry = ttk.Entry(
        new_solts_config_frame, width=8, font=("宋体", 8))
    new_solts_config_entry.pack(side=LEFT)

    def create_slots_config():
        if (slots_configuration_mode.get() == True):
            if (new_solts_config_entry.get() == ""):
                Messagebox.show_error("请输入配置名称", title="创建配置失败")
            else:
                config = load_config(config_file_path)
                if "slots" not in config:
                    config["slots"] = {}
                if new_solts_config_entry.get() not in config["slots"]:
                    config["slots"][new_solts_config_entry.get()] = {}
                plants = []
                for c in slot_type_comboboxes:
                    plants.append(c.current())
                config["slots"][new_solts_config_entry.get()]["plants"] = plants
                save_config(config, config_file_path)
                Messagebox.show_info(
                    "配置”"+new_solts_config_entry.get()+"”已创建", title="创建配置成功")
                update_slots_config_combobox()
                slots_config_combobox.set(new_solts_config_entry.get())
        else:
            Messagebox.show_error("请在配置模式下修改卡槽配置", title="创建配置失败")
    new_solts_config_button = ttk.Button(new_solts_config_frame, text="新建", padding=0, bootstyle=(
        DARK, OUTLINE), command=lambda: create_slots_config())
    new_solts_config_button.pack(side=LEFT)
    slots_config_combobox = ttk.Combobox(
        card_select_frame, width=12, bootstyle='secondary')
    slots_config_combobox.pack()
    slots_config_combobox.insert(0, "选择配置")
    slots_config_combobox.configure(state=READONLY)

    def update_slots_config_combobox():
        config = load_config(config_file_path)
        if "slots" not in config:
            return
        slots_config_combobox.configure(values=list(config['slots'].keys()))
    update_slots_config_combobox()

    def set_config_slots(event):
        if (slots_configuration_mode.get() == False):
            slots_configuration_mode.set(True)
            changeSlotsConfiguration()
        config = load_config(config_file_path)
        n = 0
        for i in config["slots"][slots_config_combobox.get()]["plants"]:
            slot_type_comboboxes[n].current(i)
            n = n+1
    slots_config_combobox.bind("<<ComboboxSelected>>", set_config_slots)
    card_select_button_frame = ttk.Frame(card_select_frame)
    card_select_button_frame.pack()

    def save_slots_config():
        if (slots_configuration_mode.get() == True):
            config = load_config(config_file_path)
            if "slots" not in config:
                config["slots"] = {}
            if slots_config_combobox.get() not in config["slots"]:
                Messagebox.show_error("配置名称不存在，请先新建配置", title="保存配置失败")
            plants = []
            for c in slot_type_comboboxes:
                plants.append(c.current())
            config["slots"][slots_config_combobox.get()]["plants"] = plants
            save_config(config, config_file_path)
            Messagebox.show_info(
                "配置”"+slots_config_combobox.get()+"”已保存", title="保存配置成功")
            update_slots_config_combobox()
        else:
            Messagebox.show_error("请在配置模式下修改卡槽配置", title="保存配置失败")

    def delete_slots_config():
        if (slots_configuration_mode.get() == True):
            config = load_config(config_file_path)
            if "slots" not in config:
                config["slots"] = {}
            if slots_config_combobox.get() not in config["slots"]:
                Messagebox.show_error("配置名称不存在", title="删除配置失败")
            del config["slots"][slots_config_combobox.get()]
            save_config(config, config_file_path)
            Messagebox.show_info(
                "配置"+slots_config_combobox.get()+"”已删除", title="删除配置成功")
            update_slots_config_combobox()
        else:
            Messagebox.show_error("请在配置模式下修改卡槽配置", title="删除配置失败")

    def select_slots_config():
        card_list = [999]*14
        try:
            selected_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x774)+0xd24)
        except:
            Messagebox.show_error("请在选卡界面使用选卡\n关卡内请点击应用", title="选卡失败")
            return
        if (selected_num != 0):
            i = 0
            j = 0
            while j < selected_num:
                if (i == 48):
                    i = i+27
                if (data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x774)+0xc8+0x3c*i) == 1):
                    n = int((data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                        data.PVZ_memory.read_int(data.baseAddress)+0x774)+0xa4+0x3c*i)-79)/51)
                    print("卡槽第"+str(n)+"张卡为"+data.plantsType[i])
                    card_list[n] = i
                    j = j+1
                i = i+1
        for c in slot_type_comboboxes:
            selected_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x774)+0xd24)
            limit_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x144)+0x24)
            print(selected_num, limit_num)
            if (selected_num < limit_num):
                if (c.current() > 47 and c.current() < 75):
                    Messagebox.show_error(
                        "不能选择特殊卡牌\n如需使用特殊卡牌，请开始游戏后点击应用", title="选卡失败")
                    for c in reversed(card_list):
                        if (c != 999):
                            print(c)
                            pvz.deselectCard(c)
                    return
                if c.current() not in card_list:
                    pvz.selectCard(c.current())
                    print(c.current())
                    card_list[selected_num] = (c.current())
                else:
                    print("------")
                    Messagebox.show_error(
                        "不能选择重复卡片\n如需使用相同卡牌，请开始游戏后点击应用", title="选卡失败")
                    for c in reversed(card_list):
                        if (c != 999):
                            print(c)
                            pvz.deselectCard(c)
                    return

    def clear_slots():
        card_list = [999]*14
        try:
            selected_num = data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.baseAddress)+0x774)+0xd24)
        except:
            Messagebox.show_error("请在选卡界面使用", title="清除选卡失败")
            return
        if (selected_num != 0):
            i = 0
            j = 0
            while j < selected_num:
                if (i == 48):
                    i = i+27
                if (data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x774)+0xc8+0x3c*i) == 1 or data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x774)+0xc8+0x3c*i) == 0):
                    n = int((data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                        data.PVZ_memory.read_int(data.baseAddress)+0x774)+0xa4+0x3c*i)-79)/51)
                    print("卡槽第"+str(n)+"张卡为"+data.plantsType[i])
                    card_list[n] = i
                    j = j+1
                i = i+1
        for c in reversed(card_list):
            if (c != 999):
                print(c)
                pvz.deselectCard(c)

    def apply_slots_config():
        if (slots_configuration_mode.get() == True):
            i = 0
            for c in slot_type_comboboxes:
                slot_list[i].setType(c.current())
                i = i+1
            slots_configuration_mode.set(False)
            changeSlotsConfiguration()
        else:
            Messagebox.show_error("请在配置模式下应用卡槽配置", title="应用配置失败")

    ttk.Button(card_select_button_frame, text="保存", padding=0, bootstyle=(
        DARK, OUTLINE), command=lambda: save_slots_config()).grid(row=0, column=0)
    ttk.Button(card_select_button_frame, text="删除", padding=0, bootstyle=(
        DARK, OUTLINE), command=lambda: delete_slots_config()).grid(row=0, column=1)
    ttk.Button(card_select_button_frame, text="选卡", padding=0, bootstyle=(
        DARK, OUTLINE), command=lambda: select_slots_config()).grid(row=1, column=0)
    ttk.Button(card_select_button_frame, text="清除选卡", padding=0, bootstyle=(
        DARK, OUTLINE), command=lambda: clear_slots()).grid(row=1, column=1)
    ttk.Button(card_select_button_frame, text="应用", padding=0, bootstyle=(
        DARK, OUTLINE), command=lambda: apply_slots_config()).grid(row=1, column=2)

    card_select_frame = ttk.LabelFrame(
        slot_page, text="快捷种植", bootstyle=PRIMARY)
    card_select_frame.place(x=0, y=455, relx=0, anchor=NW)
    ttk.Label(card_select_frame, text="1:").grid(row=0, column=0)
    slot_1_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_1_key.grid(row=0, column=1)
    slot_1_key.current(0)
    ttk.Label(card_select_frame, text="2:").grid(row=0, column=2)
    slot_2_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_2_key.grid(row=0, column=3)
    slot_2_key.current(0)
    ttk.Label(card_select_frame, text="3:").grid(row=0, column=4)
    slot_3_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_3_key.grid(row=0, column=5)
    slot_3_key.current(0)
    ttk.Label(card_select_frame, text="4:").grid(row=0, column=6)
    slot_4_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_4_key.grid(row=0, column=7)
    slot_4_key.current(0)
    ttk.Label(card_select_frame, text="5:").grid(row=0, column=8)
    slot_5_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_5_key.grid(row=0, column=9)
    slot_5_key.current(0)
    ttk.Label(card_select_frame, text="6:").grid(row=0, column=10)
    slot_6_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_6_key.grid(row=0, column=11)
    slot_6_key.current(0)
    ttk.Label(card_select_frame, text="7:").grid(row=0, column=12)
    slot_7_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_7_key.grid(row=0, column=13)
    slot_7_key.current(0)
    shovel_key_label = ttk.Label(card_select_frame, text="铲:")
    shovel_key_label.grid(row=0, column=14)
    slot_shovel_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_shovel_key.grid(row=0, column=15)
    slot_shovel_key.current(0)
    ToolTip(shovel_key_label, text="使用铲子", bootstyle=(INFO, INVERSE))
    hp_key_label = ttk.Label(card_select_frame, text="血:")
    hp_key_label.grid(row=0, column=16)
    slot_hp_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_hp_key.grid(row=0, column=17)
    slot_hp_key.current(0)
    ToolTip(hp_key_label, text="显示僵尸血量", bootstyle=(INFO, INVERSE))
    ttk.Label(card_select_frame, text="8:").grid(row=1, column=0)
    slot_8_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_8_key.grid(row=1, column=1)
    slot_8_key.current(0)
    ttk.Label(card_select_frame, text="9:").grid(row=1, column=2)
    slot_9_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_9_key.grid(row=1, column=3)
    slot_9_key.current(0)
    ttk.Label(card_select_frame, text="10:").grid(row=1, column=4)
    slot_10_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_10_key.grid(row=1, column=5)
    slot_10_key.current(0)
    ttk.Label(card_select_frame, text="11:").grid(row=1, column=6)
    slot_11_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_11_key.grid(row=1, column=7)
    slot_11_key.current(0)
    ttk.Label(card_select_frame, text="12:").grid(row=1, column=8)
    slot_12_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_12_key.grid(row=1, column=9)
    slot_12_key.current(0)
    ttk.Label(card_select_frame, text="13:").grid(row=1, column=10)
    slot_13_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_13_key.grid(row=1, column=11)
    slot_13_key.current(0)
    ttk.Label(card_select_frame, text="14:").grid(row=1, column=12)
    slot_14_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_14_key.grid(row=1, column=13)
    slot_14_key.current(0)
    top_key_label = ttk.Label(card_select_frame, text="顶:")
    top_key_label.grid(row=1, column=14)
    slot_top_key = ttk.Combobox(
        card_select_frame, width=3, values=data.keyTpye, font=("黑体", 8), state=READONLY)
    slot_top_key.grid(row=1, column=15)
    slot_top_key.current(0)
    ToolTip(top_key_label, text="卡槽置顶", bootstyle=(INFO, INVERSE))

    def loadSlotKey():
        config = load_config(config_file_path)
        try:
            slot_1_key.current(config["slotKeys"]["1"])
        except:
            pass
        try:
            slot_2_key.current(config["slotKeys"]["2"])
        except:
            pass
        try:
            slot_3_key.current(config["slotKeys"]["3"])
        except:
            pass
        try:
            slot_4_key.current(config["slotKeys"]["4"])
        except:
            pass
        try:
            slot_5_key.current(config["slotKeys"]["5"])
        except:
            pass
        try:
            slot_6_key.current(config["slotKeys"]["6"])
        except:
            pass
        try:
            slot_7_key.current(config["slotKeys"]["7"])
        except:
            pass
        try:
            slot_8_key.current(config["slotKeys"]["8"])
        except:
            pass
        try:
            slot_9_key.current(config["slotKeys"]["9"])
        except:
            pass
        try:
            slot_10_key.current(config["slotKeys"]["10"])
        except:
            pass
        try:
            slot_11_key.current(config["slotKeys"]["11"])
        except:
            pass
        try:
            slot_12_key.current(config["slotKeys"]["12"])
        except:
            pass
        try:
            slot_13_key.current(config["slotKeys"]["13"])
        except:
            pass
        try:
            slot_14_key.current(config["slotKeys"]["14"])
        except:
            pass
        try:
            slot_shovel_key.current(config["slotKeys"]["shovel"])
        except:
            pass
        try:
            slot_hp_key.current(config["slotKeys"]["hp"])
        except:
            pass
        try:
            slot_top_key.current(config["slotKeys"]["top"])
        except:
            pass
    loadSlotKey()

    def setSlotKey():
        if (slot_key_status.get()):
            config = load_config(config_file_path)
            if "slotKeys" not in config:
                config["slotKeys"] = {}
            slot_key_list = list()
            if (slot_1_key.current() != -1):
                config["slotKeys"]["1"] = slot_1_key.current()
                slot_key_list.append(slot_1_key.current())
            if (slot_2_key.current() != -1):
                if (slot_2_key.current() not in slot_key_list or slot_2_key.current() == 0):
                    config["slotKeys"]["2"] = slot_2_key.current()
                    slot_key_list.append(slot_2_key.current())
                else:
                    Messagebox.show_error("快捷键2重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()
            if (slot_3_key.current() != -1):
                if (slot_3_key.current() not in slot_key_list or slot_3_key.current() == 0):
                    config["slotKeys"]["3"] = slot_3_key.current()
                    slot_key_list.append(slot_3_key.current())
                else:
                    Messagebox.show_error("快捷键3重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()

            if (slot_4_key.current() != -1):
                if (slot_4_key.current() not in slot_key_list or slot_4_key.current() == 0):
                    config["slotKeys"]["4"] = slot_4_key.current()
                    slot_key_list.append(slot_4_key.current())
                else:
                    Messagebox.show_error("快捷键4重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()

            if (slot_5_key.current() != -1):
                if (slot_5_key.current() not in slot_key_list or slot_5_key.current() == 0):
                    config["slotKeys"]["5"] = slot_5_key.current()
                    slot_key_list.append(slot_5_key.current())
                else:
                    Messagebox.show_error("快捷键5重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()

            if (slot_6_key.current() != -1):
                if (slot_6_key.current() not in slot_key_list or slot_6_key.current() == 0):
                    config["slotKeys"]["6"] = slot_6_key.current()
                    slot_key_list.append(slot_6_key.current())
                else:
                    Messagebox.show_error("快捷键6重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()

            if (slot_7_key.current() != -1):
                if (slot_7_key.current() not in slot_key_list or slot_7_key.current() == 0):
                    config["slotKeys"]["7"] = slot_7_key.current()
                    slot_key_list.append(slot_7_key.current())
                else:
                    Messagebox.show_error("快捷键7重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()

            if (slot_8_key.current() != -1):
                if (slot_8_key.current() not in slot_key_list or slot_8_key.current() == 0):
                    config["slotKeys"]["8"] = slot_8_key.current()
                    slot_key_list.append(slot_8_key.current())
                else:
                    Messagebox.show_error("快捷键8重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()

            if (slot_9_key.current() != -1):
                if (slot_9_key.current() not in slot_key_list or slot_9_key.current() == 0):
                    config["slotKeys"]["9"] = slot_9_key.current()
                    slot_key_list.append(slot_9_key.current())
                else:
                    Messagebox.show_error("快捷键9重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()

            if (slot_10_key.current() != -1):
                if (slot_10_key.current() not in slot_key_list or slot_10_key.current() == 0):
                    config["slotKeys"]["10"] = slot_10_key.current()
                    slot_key_list.append(slot_10_key.current())
                else:
                    Messagebox.show_error("快捷键10重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()

            if (slot_11_key.current() != -1):
                if (slot_11_key.current() not in slot_key_list or slot_11_key.current() == 0):
                    config["slotKeys"]["11"] = slot_11_key.current()
                    slot_key_list.append(slot_11_key.current())
                else:
                    Messagebox.show_error("快捷键11重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()

            if (slot_12_key.current() != -1):
                if (slot_12_key.current() not in slot_key_list or slot_12_key.current() == 0):
                    config["slotKeys"]["12"] = slot_12_key.current()
                    slot_key_list.append(slot_12_key.current())
                else:
                    Messagebox.show_error("快捷键12重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()

            if (slot_13_key.current() != -1):
                if (slot_13_key.current() not in slot_key_list or slot_13_key.current() == 0):
                    config["slotKeys"]["13"] = slot_13_key.current()
                    slot_key_list.append(slot_13_key.current())
                else:
                    Messagebox.show_error("快捷键13重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()

            if (slot_14_key.current() != -1):
                if (slot_14_key.current() not in slot_key_list or slot_14_key.current() == 0):
                    config["slotKeys"]["14"] = slot_14_key.current()
                    slot_key_list.append(slot_14_key.current())
                else:
                    Messagebox.show_error("快捷键14重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()
            if (slot_shovel_key.current() != -1):
                if (slot_shovel_key.current() not in slot_key_list or slot_shovel_key.current() == 0):
                    config["slotKeys"]["shovel"] = slot_shovel_key.current()
                    slot_key_list.append(slot_shovel_key.current())
                else:
                    Messagebox.show_error("铲子快捷键重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()
            if (slot_hp_key.current() != -1):
                if (slot_hp_key.current() not in slot_key_list or slot_hp_key.current() == 0):
                    config["slotKeys"]["hp"] = slot_hp_key.current()
                    slot_key_list.append(slot_hp_key.current())
                else:
                    Messagebox.show_error("显血快捷键重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()
            if (slot_top_key.current() != -1):
                if (slot_top_key.current() not in slot_key_list or slot_top_key.current() == 0):
                    config["slotKeys"]["top"] = slot_top_key.current()
                    slot_key_list.append(slot_top_key.current())
                else:
                    Messagebox.show_error("卡槽置顶快捷键重复", title="不可设置相同快捷键")
                    slot_key_status.set(False)
                    return ()

            save_config(config, config_file_path)
            slot_key_list = config["slotKeys"]
            pvz.slotKey(slot_key_list)
        else:
            pvz.slotKey(False)

    slot_key_status = ttk.BooleanVar(card_select_frame)
    slot_key_check = ttk.Checkbutton(card_select_frame, text="开启", variable=slot_key_status,
                                     bootstyle="primary-round-toggle", command=lambda: setSlotKey())
    slot_key_check.grid(row=1, column=16, columnspan=4)

    # 定义一个函数来更新slot的属性
    def get_slot_attribute():
        for index, slot in enumerate(slot_list):
            try:
                slot_type_comboboxes[index].current(slot.type)
                if (slot_page.focus_get() != slot_cooldown_entrys[index] and slot_page.focus_get() != slot_cd_progressBars[index]):
                    slot_cooldown_values[index].set(slot.cooldown)
                    slot_cd_progressBars[index].configure(
                        maximum=slot_cooldown_values[index].get())
                if (slot_page.focus_get() != slot_elapsed_entrys[index] and slot_page.focus_get() != slot_cd_progressBars[index]):
                    slot_elapsed_values[index].set(slot.elapsed)
                slot_isVisible_flags[index].set(not slot.isViible)
                # slot_canUse_flags[index].set(slot.canUse)
            except:
                pass
        try:
            slots_num_value.set(data.PVZ_memory.read_int(data.PVZ_memory.read_int(
                data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x144)+0x24))
        except:
            pass

    other_page = ttk.Frame(page_tab)
    other_page.pack()
    page_tab.add(other_page, text="暂未分类")
    endless_frame = ttk.Frame(other_page)
    other_toggle_frame = ttk.LabelFrame(other_page, text="未分类开关")
    other_toggle_frame.pack(anchor=W)

    doom_no_hole_status = ttk.BooleanVar(other_toggle_frame)
    bone_no_hole_status = ttk.BooleanVar(other_toggle_frame)
    treasure_no_hole_status = ttk.BooleanVar(other_toggle_frame)
    doom_no_hole_check = ttk.Checkbutton(other_toggle_frame, text="毁灭不留坑", variable=doom_no_hole_status,
                                         bootstyle="success-round-toggle", command=lambda: pvz.noHole(doom_no_hole_status.get(), bone_no_hole_status.get(), treasure_no_hole_status.get()))
    doom_no_hole_check.pack()
    bone_no_hole_check = ttk.Checkbutton(other_toggle_frame, text="骷髅不留坑", variable=bone_no_hole_status,
                                         bootstyle="success-round-toggle", command=lambda: pvz.noHole(doom_no_hole_status.get(), bone_no_hole_status.get(), treasure_no_hole_status.get()))
    bone_no_hole_check.pack()
    treasure_no_hole_check = ttk.Checkbutton(other_toggle_frame, text="宝藏不留坑", variable=treasure_no_hole_status,
                                             bootstyle="success-round-toggle", command=lambda: pvz.noHole(doom_no_hole_status.get(), bone_no_hole_status.get(), treasure_no_hole_status.get()))
    treasure_no_hole_check.pack()
    zombiebean_hpynotized_status = ttk.BooleanVar(other_toggle_frame)
    zombiebean_hpynotized_check = ttk.Checkbutton(other_toggle_frame, text="僵尸豆魅惑", variable=zombiebean_hpynotized_status,
                                                  bootstyle="success-round-toggle", command=lambda: pvz.zombiebeanHpynotized(zombiebean_hpynotized_status.get()))
    zombiebean_hpynotized_check.pack()
    conveyor_belt_full_status = ttk.BooleanVar(other_toggle_frame)
    conveyor_belt_full_check = ttk.Checkbutton(other_toggle_frame, text="传送带全满", variable=conveyor_belt_full_status,
                                               bootstyle="success-round-toggle", command=lambda: pvz.conveyorBeltFull(conveyor_belt_full_status.get()))
    conveyor_belt_full_check.pack()
    endless_frame.pack(anchor=W)
    ttk.Label(endless_frame, text="无尽轮数").pack(side=LEFT)
    endless_round = ttk.IntVar(endless_frame)
    endless_round_entry = ttk.Entry(
        endless_frame, width=5, textvariable=endless_round)
    endless_round_entry.pack(side=LEFT)

    def setEndlessRound(event):
        pvz.setEndlessRound(endless_round.get())
        endless_frame.focus_set()
    endless_round_entry.bind("<Return>", setEndlessRound)

    def refreshData():
        if (page_tab.index('current') == 0):
            gameDifficult.set(pvz.getDifficult())
            if (pvz.getMap() != False):
                try:
                    if (main_window.focus_get() != sun_value_entry):
                        sun_value.set(pvz.getSun())
                    if (main_window.focus_get() != silver_value_entry):
                        silver_value.set(pvz.getSilver())
                    if (main_window.focus_get() != gold_value_entry):
                        gold_value.set(pvz.getGold())
                    if (main_window.focus_get() != diamond_value_entry):
                        diamond_value.set(pvz.getDiamond())
                except:
                    pass
        if (page_tab.index('current') == 1):
            if (pvz.getMap() != False):
                refresh_zombie_list()
                get_zombie_attribute()
        if (page_tab.index('current') == 2):
            if (pvz.getMap() != False):
                refresh_plant_list()
                get_plant_attribute()
        if (page_tab.index('current') == 3):
            if (pvz.getMap() != False):
                refresh_item_list()
                get_item_attribute()
        if (page_tab.index('current') == 4):
            if (slots_configuration_mode.get() == False):
                refresh_slot_list()
                get_slot_attribute()
        if (page_tab.index('current') == 5):
            if (main_window.focus_get() != endless_round_entry):
                endless_round.set(pvz.getEndlessRound())

        main_window.after(100, refreshData)

    def load_plugin(main_window):
        pyc_name = filedialog.askopenfilename(
            title='选择pyc文件',
            filetypes=[('PYC files', '*.pyc')]
        )
        if pyc_name:
            print(f"选中的文件: {pyc_name}")
            # 这里可以添加加载和使用pyc文件的代码
        else:
            print("没有选择文件")
        spec = importlib.util.spec_from_file_location("module.name", pyc_name)
        plugin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin)
        plugin.open_plugin_window(main_window)
        # plugin=ctypes.CDLL(pyc_name)
        # plugin.open_plugin_window(main_window)
        # import {pyc_name} as plugin

    plugin_button = ttk.Button(main_window, text="载入插件", padding=0, bootstyle=(
        PRIMARY, LINK), cursor="hand2", command=lambda: load_plugin(main_window))
    plugin_button.place(x=100, y=0, relx=0, rely=1, anchor=SW)

    support_button = ttk.Button(main_window, text="更新公告", padding=0, bootstyle=(
        PRIMARY, LINK), cursor="hand2", command=lambda: support())
    support_button.place(x=0, y=0, relx=1, anchor=NE)
    main_window.after(100, refreshData)

    main_window.protocol("WM_DELETE_WINDOW", lambda: exit_editor(
        config_file_path, main_window))
    main_window.mainloop()


if __name__ == '__main__':
    mainWindow()
