from PIL import Image
Image.CUBIC = Image.BICUBIC
from pymem import Pymem
import win32gui
import win32process
import psutil
import re
import time
import os
import sys
import ctypes
import webbrowser
import json
import keyboard
import requests
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.tooltip import ToolTip
import PVZ_data as data
import PVZ_Hybrid as pvz
import PVZ_asm
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
current_version = '0.09'
version_url = 'https://gitee.com/EFrostBlade/PVZHybrid_Editor/raw/main/version.txt'
main_window=None
data.update_PVZ_memory(1)
zombie_select=None
plant_select=None
item_select=None
plant_characteristic_type=None
shortcut_entries = []
shortcut_buttons = []
shortcut_comboboxs = []
action_values=[]
action_list=["高级暂停","设置阳光","增加阳光","自由放置","免费种植","取消冷却","自动收集","柱子模式","超级铲子","永不失败",
             "当前关卡胜利","秒杀所有僵尸","解锁全部植物","放置植物","搭梯","清除植物"]
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
#点击关闭退出
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
        json.dump(default_config, file, indent=4)

# 读取配置文件的函数
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return default_config  # 如果文件不存在，返回默认配置

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
            data.update_PVZ_memory(Pymem(int(re.search(r'(\d+)',process1).group(1))))
            data.update_PVZ_pid(int(re.search(r'(\d+)',process1).group(1)))
        except:
            Messagebox.show_error("没有足够的权限，请确保游戏未以管理员身份运行",title="注入进程失败",parent=choose_process_window)
            choose_process_window.quit()
            choose_process_window.destroy()
        else:   
            choose_process_window.quit()
            choose_process_window.destroy()   

    def tryFindGame():
        try:
            hwnd=win32gui.FindWindow("MainWindow",None)
            pid=win32process.GetWindowThreadProcessId(hwnd)
            data.update_PVZ_memory( Pymem(pid[1]))
            data.update_PVZ_pid(pid[1])
            choose_process_window.quit()
            choose_process_window.destroy()
        except:
            Messagebox.show_error("请确保游戏已开启且未以管理员身份运行\n如果仍无法注入游戏可以尝试使用管理员身份开启本修改器",title="未找到游戏",parent=choose_process_window)
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
        def get_all_hwnd(hwnd,mouse):
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
        win32gui.EnumWindows(get_all_hwnd, 0)
        selecthwnd=list()
        for h,t in hwnd_title.items():
            if t != "":
                pid=win32process.GetWindowThreadProcessId((h))
                pn=psutil.Process(pid[1]).name()
                selecthwnd.append((pid[1],[t],[pn]))
        return selecthwnd
    
    choose_process_window = ttk.Toplevel(topmost=True)
    choose_process_window.title("选择进程")
    choose_process_window.geometry("500x500")
    choose_process_window.iconphoto(False,ttk.PhotoImage(file=resource_path(r"res\icon\choose.png")))
    choose_process_window.tk.call('tk', 'scaling', 4/3)  
    main_window_x = main_window.winfo_x()
    main_window_y = main_window.winfo_y()  
    choose_process_window.geometry(f'+{main_window_x+50}+{main_window_y + 50}')
    label = ttk.Label(choose_process_window,text="如果未开启游戏请开启游戏后点击寻找游戏按钮",bootstyle=WARNING, font=("黑体", 16))
    label.pack(pady=20)
    frame1 = ttk.Frame(choose_process_window)
    frame1.pack()
    retry_button = ttk.Button(frame1, text='寻找游戏', command=lambda:tryFindGame())
    retry_button.pack(side=LEFT,padx=80)
    close_button = ttk.Button(frame1, text='关闭',bootstyle=DANGER, command=lambda:close())
    close_button.pack(side=RIGHT,padx=80)
    label = ttk.Label(choose_process_window,text="如有需要可在下方手动选择游戏窗口\n窗口名一般为植物大战僵尸杂交版\n进程名一般为PlantsVsZombies.exe\n显示格式为pid 窗口名 进程名",bootstyle=INFO, font=("黑体", 16))
    label.pack(pady=(50,10))
    frame2 = ttk.Frame(choose_process_window)
    frame2.pack()
    combobox = ttk.Combobox(frame2,bootstyle=PRIMARY,width=50)
    combobox.pack(side=LEFT)
    def refreshList():
        selecthwnd=getSelecthwnd()
        #设置下拉菜单中的值
        combobox['state'] = NORMAL
        combobox['value'] = (selecthwnd)
        combobox['state'] = READONLY
    #设置下拉菜单的默认值,默认值索引从0开始
        combobox.current(0)
    refreshList()
    refresh_button = ttk.Button(frame2, text='刷新列表',bootstyle=INFO, command=lambda:refreshList())
    refresh_button.pack(side=LEFT,padx=(10,0))
    comfrime_button = ttk.Button(choose_process_window, text='确定',bootstyle=SUCCESS, command=lambda:openPVZ_memory(combobox.get()))
    comfrime_button.pack(pady=(30,0))
    choose_process_window.protocol('WM_DELETE_WINDOW',lambda:close())
    choose_process_window.mainloop()

def support():
    global main_window
    support_window=ttk.Toplevel(topmost=True)
    support_window.title("关于")
    support_window.geometry("300x300")
    support_window.iconphoto(False,ttk.PhotoImage(file=resource_path((r"res\icon\info.png"))))
    support_window.tk.call('tk', 'scaling', 4/3)    
    main_window_x = main_window.winfo_x()
    main_window_y = main_window.winfo_y()  
    support_window.geometry(f'+{main_window_x+100}+{main_window_y + 100}')
    ttk.Label(support_window,text="本软件完全免费",font=("黑体",18),bootstyle=SUCCESS).pack(pady=20)
    github_frame=ttk.Frame(support_window)
    github_frame.pack()
    ttk.Label(github_frame,text="所有代码开源于",font=("黑体",12),bootstyle=SUCCESS).pack(side=LEFT)
    def open_code():
        webbrowser.open_new("https://github.com/EFrostBlade/PVZHybrid_Editor")
    ttk.Button(github_frame, text="PVZHybrid_Editor(github.com)",padding=0,bootstyle=(PRIMARY,LINK),cursor="hand2",command=open_code).pack(side=LEFT)
    ttk.Label(support_window,text="如果您觉得本软件有帮助，欢迎赞助支持开发者",font=("黑体",8),bootstyle=WARNING).pack()
    def open_qq():
        webbrowser.open_new("http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=NXcD3BMkaDeyysTJYZZvJnl7xDZEL7et&authKey=rRxScaHQ7BDXklafDeSFtMLVgXRK8%2Bkd0PdQ2sssDv9AtnJE4HATLSbAjTxJKRGR&noverify=0&group_code=678474090")
    qq_frame=ttk.Frame(support_window)
    qq_frame.pack()
    ttk.Label(qq_frame,text="赞助任意金额后即可加入赞助群：",font=("黑体",8),bootstyle=WARNING).pack(side=LEFT)
    ttk.Button(qq_frame, text="678474090",padding=0,bootstyle=(PRIMARY,LINK),cursor="hand2",command=open_qq).pack(side=LEFT)
    ttk.Label(support_window,text="进群可享受功能优先适配、1对1解决问题等服务",font=("黑体",8),bootstyle=WARNING).pack()
    image_frame=ttk.Frame(support_window)
    image_frame.pack()
    AliPay = ttk.PhotoImage(file=resource_path(r"res/support/AliPay.png"))
    WeChatPay = ttk.PhotoImage(file=resource_path(r"res/support/WeChatPay.png"))
    AliPay_image=ttk.Label(image_frame,image=AliPay)
    AliPay_image.grid(row=0,column=0,padx=10)
    WeChatPay_image=ttk.Label(image_frame,image=WeChatPay)
    WeChatPay_image.grid(row=0,column=1,padx=10)
    ttk.Label(image_frame,text="支付宝",bootstyle=PRIMARY,font=("黑体",12)).grid(row=1,column=0,pady=5)
    ttk.Label(image_frame,text="微信支付",bootstyle=SUCCESS,font=("黑体",12)).grid(row=1,column=1,pady=5)
    support_window.mainloop()

def delete_config():
    global main_window
    deete_config_window=ttk.Toplevel(topmost=True)
    deete_config_window.title("配置文件出错！")
    deete_config_window.geometry("300x300")
    deete_config_window.tk.call('tk', 'scaling', 4/3)    
    main_window_x = main_window.winfo_x()
    main_window_y = main_window.winfo_y()  
    deete_config_window.geometry(f'+{main_window_x+100}+{main_window_y + 100}')
    ttk.Label(deete_config_window,text="读取配置文件时发生错误\n将删除配置文件并关闭程序\n请重新启动程序",font=("黑体",18),bootstyle=DANGER).pack(pady=20)
    ttk.Button(deete_config_window,text="确定",bootstyle=DANGER,command=lambda:exit_with_delete_config(config_file_path)).pack()
    deete_config_window.protocol("WM_DELETE_WINDOW", lambda: exit_with_delete_config(config_file_path))
    deete_config_window.mainloop()


def mainWindow():
    global main_window
    main_window=ttk.Window()
    main_window.title("杂交版多功能修改器  "+str(current_version))
    main_window.geometry("500x550")
    main_window.iconphoto(False,ttk.PhotoImage(file=resource_path(r"res\icon\editor.png")))
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

        update_window=ttk.Toplevel(topmost=True)
        update_window.title("有新版本")
        update_window.geometry("320x400")
        update_window.iconphoto(False,ttk.PhotoImage(file=resource_path((r"res\icon\info.png"))))
        update_window.tk.call('tk', 'scaling', 4/3)    
        main_window_x = main_window.winfo_x()
        main_window_y = main_window.winfo_y()  
        update_window.geometry(f'+{main_window_x+100}+{main_window_y + 100}')
        ttk.Label(update_window,text="检测到新版本{}".format(latest_version),font=("黑体",18),bootstyle=INFO).pack()
        ttk.Label(update_window,text="本软件完全免费",font=("黑体",18),bootstyle=SUCCESS).pack(pady=20)
        github_frame=ttk.Frame(update_window)
        github_frame.pack()
        ttk.Label(github_frame,text="前往下载最新版本",font=("黑体",12),bootstyle=SUCCESS).pack(side=LEFT)
        def open_code():
            webbrowser.open_new("https://gitee.com/EFrostBlade/PVZHybrid_Editor/releases")
        ttk.Button(github_frame, text="PVZHybrid_Editor(gitee.com)",padding=0,bootstyle=(PRIMARY,LINK),cursor="hand2",command=open_code).pack(side=LEFT)
        ttk.Label(update_window,text="如果您觉得本软件有帮助，欢迎赞助支持开发者",font=("黑体",8),bootstyle=WARNING).pack()
        def open_qq():
            webbrowser.open_new("http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=NXcD3BMkaDeyysTJYZZvJnl7xDZEL7et&authKey=rRxScaHQ7BDXklafDeSFtMLVgXRK8%2Bkd0PdQ2sssDv9AtnJE4HATLSbAjTxJKRGR&noverify=0&group_code=678474090")
        qq_frame=ttk.Frame(update_window)
        qq_frame.pack()
        ttk.Label(qq_frame,text="赞助任意金额后即可加入赞助群：",font=("黑体",8),bootstyle=WARNING).pack(side=LEFT)
        ttk.Button(qq_frame, text="678474090",padding=0,bootstyle=(PRIMARY,LINK),cursor="hand2",command=open_qq).pack(side=LEFT)
        ttk.Label(update_window,text="进群可享受功能优先适配、1对1解决问题等服务",font=("黑体",8),bootstyle=WARNING).pack()
        image_frame=ttk.Frame(update_window)
        image_frame.pack()
        AliPay = ttk.PhotoImage(file=resource_path(r"res/support/AliPay.png"))
        WeChatPay = ttk.PhotoImage(file=resource_path(r"res/support/WeChatPay.png"))
        AliPay_image=ttk.Label(image_frame,image=AliPay)
        AliPay_image.grid(row=0,column=0,padx=10)
        WeChatPay_image=ttk.Label(image_frame,image=WeChatPay)
        WeChatPay_image.grid(row=0,column=1,padx=10)
        ttk.Label(image_frame,text="支付宝",bootstyle=PRIMARY,font=("黑体",12)).grid(row=1,column=0,pady=5)
        ttk.Label(image_frame,text="微信支付",bootstyle=SUCCESS,font=("黑体",12)).grid(row=1,column=1,pady=5)
        update_window.protocol('WM_DELETE_WINDOW',lambda:close())
        update_window.mainloop()



    try:
        # 从服务器获取最新版本号
        response = requests.get(version_url)
        latest_version = response.text.strip()
        print(latest_version)
        # 比较版本号
        if latest_version > current_version:
            # 如果发现新版本，提示用户
            open_update_window(latest_version)
    except Exception as e:
        Messagebox.show_error('无法检查更新，请检查您的网络连接。',title='更新检测失败',)

    # style=ttk.Style()
    # style.configure('small.TButton',font=("黑体",8),padding=(0,0,0,0))
    process_frame=ttk.Frame(main_window)
    process_frame.place(x=0,y=0,relx=1,rely=1,anchor=SE)
    process_label=ttk.Label(process_frame,text="", font=("黑体", 8))
    process_label.pack(side=LEFT)
    def updateGame():
        chooseGame()
        if(type(data.PVZ_memory)!= Pymem):
            process_label["text"]="未找到游戏"
            process_label.config(bootstyle=DANGER)
        else:
            process_label["text"]="找到进程："+str(data.PVZ_memory.process_id)+str(psutil.Process(data.PVZ_memory.process_id).name())
            process_label.config(bootstyle=DANGER)
    def tryFindGame():
        try:
            hwnd=win32gui.FindWindow("MainWindow",None)
            pid=win32process.GetWindowThreadProcessId(hwnd)
            data.update_PVZ_memory( Pymem(pid[1]))
            data.update_PVZ_pid(pid[1])
            process_label["text"]="找到进程："+str(data.PVZ_memory.process_id)+str(psutil.Process(data.PVZ_memory.process_id).name())
            process_label.config(bootstyle=DANGER)
        except:
            updateGame()
    tryFindGame()
    choose_process_button=ttk.Button(process_frame,text="选择游戏",padding=0,cursor="hand2",bootstyle=(PRIMARY,LINK),command=lambda:updateGame())
    choose_process_button.pack(side=LEFT)
    back_ground_status=ttk.IntVar(main_window)
    back_ground_check=ttk.Checkbutton(main_window,text="后台运行",variable=back_ground_status,bootstyle="round-toggle",command=lambda:pvz.backGround(back_ground_status.get()))
    back_ground_check.place(x=3,y=-3,relx=0,rely=1,anchor=SW)
    
    
    page_tab=ttk.Notebook(main_window)
    page_tab.pack(padx=10, pady=(5,30), fill=BOTH,expand=True)
    common_page=ttk.Frame(page_tab)
    common_page.pack()
    page_tab.add(common_page,text="常用功能")
    resource_modify_frame=ttk.Labelframe(common_page,text="资源修改",bootstyle=WARNING)
    resource_modify_frame.place(x=0,y=0,anchor=NW)
    upper_limit_status=ttk.BooleanVar(resource_modify_frame)
    upper_limit_check=ttk.Checkbutton(resource_modify_frame,text="解锁资源上限",bootstyle="warning-round-toggle",variable=upper_limit_status,command=lambda:pvz.upperLimit(upper_limit_status.get()))
    upper_limit_check.grid(row=0,column=0,columnspan=2,sticky=E)
    ttk.Label(resource_modify_frame,text="当前阳光:",bootstyle=WARNING,font=("宋体",14)).grid(row=1,column=0,sticky=E)
    sun_value=ttk.IntVar(resource_modify_frame)
    sun_value_entry=ttk.Entry(resource_modify_frame,width=8,bootstyle=WARNING,textvariable=sun_value)
    sun_value_entry.grid(row=1,column=1)
    def setSun(event):
        pvz.setSun(sun_value.get())
        resource_modify_frame.focus_set()
    sun_value_entry.bind("<Return>",setSun)
    ttk.Label(resource_modify_frame,text="增加阳光:",bootstyle=WARNING,font=("宋体",14)).grid(row=2,column=0,sticky=E)
    sun_add_value=ttk.IntVar(resource_modify_frame)
    sun_add_entry=ttk.Entry(resource_modify_frame,width=8,bootstyle=WARNING,textvariable=sun_add_value)
    sun_add_entry.grid(row=2,column=1)
    config = load_config(config_file_path)
    try:
        sun_add_value.set(config["data"]["sunadd"])
    except:
        pass
    def addSun(event):
        pvz.addSun(sun_add_value.get())
        modify_config(config_file_path,"data","sunadd",sun_add_value.get())
        resource_modify_frame.focus_set()
    sun_add_entry.bind("<Return>",addSun)
    quick_start_frame=ttk.LabelFrame(common_page,text="快速使用",bootstyle=SUCCESS)
    quick_start_frame.place(x=0,y=150,relx=0,rely=0,anchor=NW)
    over_plant_status=ttk.BooleanVar(quick_start_frame)
    over_plant_check=ttk.Checkbutton(quick_start_frame,text="自由放置",variable=over_plant_status,bootstyle="success-round-toggle",command=lambda:pvz.overPlant(over_plant_status.get()))
    over_plant_check.grid(row=0,column=0,sticky=W)
    ToolTip(over_plant_check,text="植物可以重叠放置并无视地形",bootstyle=(INFO,INVERSE))
    free_plant_status=ttk.BooleanVar(quick_start_frame)
    free_plant_check=ttk.Checkbutton(quick_start_frame,text="免费种植",variable=free_plant_status,bootstyle="success-round-toggle",command=lambda:pvz.ignoreSun(free_plant_status.get()))
    free_plant_check.grid(row=1,column=0,sticky=W)
    ToolTip(free_plant_check,text="植物可以不消耗阳光种植",bootstyle=(INFO,INVERSE))
    cancel_cd_status=ttk.BooleanVar(quick_start_frame)
    cancel_cd_check=ttk.Checkbutton(quick_start_frame,text="取消冷却",variable=cancel_cd_status,bootstyle="success-round-toggle",command=lambda:pvz.cancelCd(cancel_cd_status.get()))
    cancel_cd_check.grid(row=2,column=0,sticky=W)
    ToolTip(cancel_cd_check,text="植物种植后不进入冷却时间",bootstyle=(INFO,INVERSE))
    auto_colect_status=ttk.BooleanVar(quick_start_frame)
    auto_colect_check=ttk.Checkbutton(quick_start_frame,text="自动收集",variable=auto_colect_status,bootstyle="success-round-toggle",command=lambda:pvz.autoCollect(auto_colect_status.get()))
    auto_colect_check.grid(row=3,column=0,sticky=W)
    ToolTip(auto_colect_check,text="自动收集自然掉落的阳光和僵尸掉落的金币",bootstyle=(INFO,INVERSE))
    column_like_status=ttk.BooleanVar(quick_start_frame)
    column_like_check=ttk.Checkbutton(quick_start_frame,text="柱子模式",variable=column_like_status,bootstyle="success-round-toggle",command=lambda:pvz.column(column_like_status.get()))
    column_like_check.grid(row=4,column=0,sticky=W)
    ToolTip(column_like_check,text="种植一个植物后在同一列的其他行种植相同的植物(可与自由放置配合使用)",bootstyle=(INFO,INVERSE))
    shovel_pro_status=ttk.BooleanVar(quick_start_frame) 
    shovel_pro_check=ttk.Checkbutton(quick_start_frame,text="超级铲子",variable=shovel_pro_status,bootstyle="success-round-toggle",command=lambda:pvz.shovelpro(shovel_pro_status.get()))
    shovel_pro_check.grid(row=5,column=0,sticky=W)
    ToolTip(shovel_pro_check,text="铲掉植物返还其阳光消耗并触发亡语效果",bootstyle=(INFO,INVERSE))
    never_fail_status=ttk.BooleanVar(quick_start_frame)
    never_fail_check=ttk.Checkbutton(quick_start_frame,text="永不失败",variable=never_fail_status,bootstyle="success-round-toggle",command=lambda:pvz.ignoreZombies(never_fail_status.get()))
    never_fail_check.grid(row=6,column=0,sticky=W)
    ToolTip(never_fail_check,text="僵尸进家不判定游戏失败",bootstyle=(INFO,INVERSE))
    pause_pro_status=ttk.BooleanVar(quick_start_frame)
    pause_pro_check=ttk.Checkbutton(quick_start_frame,text="高级暂停",variable=pause_pro_status,bootstyle="success-round-toggle",command=lambda:pvz.pausePro(pause_pro_status.get()))
    pause_pro_check.grid(row=7,column=0,sticky=W)
    ToolTip(pause_pro_check,text="可以暂停种植植物",bootstyle=(INFO,INVERSE))
    win_button=ttk.Button(quick_start_frame,text="当前关卡胜利",padding=0,bootstyle=(SUCCESS,OUTLINE),command=lambda:pvz.win())
    win_button.grid(row=8,column=0,sticky=W,pady=(2,2))
    ToolTip(win_button,text="当前的游戏关卡直接进行胜利结算",bootstyle=(INFO,INVERSE))
    defeat_button=ttk.Button(quick_start_frame,text="当前关卡失败",padding=0,bootstyle=(SUCCESS,OUTLINE),command=lambda:pvz.defeat())
    defeat_button.grid(row=9,column=0,sticky=W,pady=(2,2))
    ToolTip(defeat_button,text="当前的游戏关卡直接进行失败结算",bootstyle=(INFO,INVERSE))
    kill_all_button=ttk.Button(quick_start_frame,text="秒杀所有僵尸",padding=0,bootstyle=(SUCCESS,OUTLINE),command=lambda:pvz.killAllZombies())
    kill_all_button.grid(row=10,column=0,sticky=W,pady=(2,2))
    ToolTip(kill_all_button,text="秒杀当前场上的所有僵尸",bootstyle=(INFO,INVERSE))
    unlock_button=ttk.Button(quick_start_frame,text="解锁全部植物",padding=0,bootstyle=(SUCCESS,OUTLINE),command=lambda:pvz.unlock())
    unlock_button.grid(row=11,column=0,sticky=W,pady=(2,2))
    ToolTip(unlock_button,text="在本次游戏中临时解锁图鉴中的所有植物(包括尚无法获得的隐藏植物)",bootstyle=(INFO,INVERSE))
    
    game_speed_frame=ttk.LabelFrame(common_page,text="游戏速度",bootstyle=PRIMARY)
    game_speed_frame.place(x=0,y=100,anchor=NW)
    game_speed_label=ttk.Label(game_speed_frame,text="1",bootstyle=PRIMARY)
    game_speed_label.grid(row=0,column=0)
    game_speed_frame.columnconfigure(0,minsize=30)
    game_speed_value=ttk.DoubleVar(game_speed_frame)
    game_speed_value.set(2)
    def changeSpeedValue(value):
        step=1
        adjusted_value = round(float(value) / step) * step
        game_speed_value.set(adjusted_value)
        if(game_speed_value.get()==0):
            game_speed_label.config(text="0.25")
        elif(game_speed_value.get()==1):
            game_speed_label.config(text="0.5")
        elif(game_speed_value.get()==2):
            game_speed_label.config(text="1")
        elif(game_speed_value.get()==3):
            game_speed_label.config(text="2")
        elif(game_speed_value.get()==4):
            game_speed_label.config(text="5")
        elif(game_speed_value.get()==5):
            game_speed_label.config(text="10")
        elif(game_speed_value.get()==6):
            game_speed_label.config(text="20")
        pvz.changeGameSpeed(game_speed_value.get())
    game_speed_scale=ttk.Scale(game_speed_frame,from_=0,to=6,orient=HORIZONTAL,variable=game_speed_value,command=changeSpeedValue)
    game_speed_scale.grid(row=0,column=1)
    def on_mousewheel(event):
        # 计算滚轮的滚动方向和距离
        increment = -1 if event.delta > 0 else 1
        # 获取当前Scale的值
        value = game_speed_value.get()+ increment
        # 设置新的Scale值
        step=1
        adjusted_value = round(float(value) / step) * step
        game_speed_value.set(adjusted_value)
        if(game_speed_value.get()==0):
            game_speed_label.config(text="0.25")
        elif(game_speed_value.get()==1):
            game_speed_label.config(text="0.5")
        elif(game_speed_value.get()==2):
            game_speed_label.config(text="1")
        elif(game_speed_value.get()==3):
            game_speed_label.config(text="2")
        elif(game_speed_value.get()==4):
            game_speed_label.config(text="5")
        elif(game_speed_value.get()==5):
            game_speed_label.config(text="10")
        elif(game_speed_value.get()==6):
            game_speed_label.config(text="20")
        pvz.changeGameSpeed(game_speed_value.get())
    game_speed_scale.bind("<MouseWheel>", on_mousewheel)
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
            keyboard.add_hotkey(shortcut_info['key'], lambda action=shortcut_info['action']: on_triggered(action))

    # 修改快捷键配置并重新加载监听
    def modify_shortcut(shortcut_id, new_key, new_action):
        try:
            keyboard.add_hotkey(new_key, lambda: on_triggered(new_action))
        except:
            Messagebox.show_error("请检查快捷键输入是否正确",title="快捷键非法")
            return
        config = load_config(config_file_path)
        # 保存旧的快捷键值
        old_key = config['shortcuts'].get(shortcut_id, {}).get('key')
        if 'shortcuts' not in config:
            config['shortcuts'] = {}
        config['shortcuts'][shortcut_id] = {'key': new_key, 'action': new_action}
        save_config(config, config_file_path)
        # 如果旧的快捷键存在，则移除旧的快捷键监听
        if old_key:
            keyboard.remove_hotkey(old_key)
        # 添加新的快捷键监听
        # 更新快捷键显示
        update_shortcut_display()

    def switch_status(status):
        if(status.get()==True):
            status.set(False)
        elif(status.get()==False):
            status.set(True)
        elif(status.get()==1):
            status.set(0)
        elif(status.get()==0):
            status.set(1)

    # 捕获快捷键并在控制台输出
    def on_triggered(action):
        if action==0:
            switch_status(pause_pro_status)
            pvz.pausePro(pause_pro_status.get())
        elif action==1:
            pvz.setSun(sun_value.get())
        elif action==2:
            pvz.addSun(sun_add_value.get())
        elif action==3:
            switch_status(over_plant_status)
            pvz.overPlant(over_plant_status.get())
        elif action==4:
            switch_status(free_plant_status)
            pvz.ignoreSun(free_plant_status.get())
        elif action==5:
            switch_status(cancel_cd_status)
            pvz.cancelCd(cancel_cd_status.get())
        elif action==6:
            switch_status(auto_colect_status)
            pvz.autoCollect(auto_colect_status.get())
        elif action==7:
            switch_status(column_like_status)
            pvz.column(column_like_status.get())
        elif action==8:
            switch_status(shovel_pro_status)
            pvz.shovelpro(shovel_pro_status.get())
        elif action==9:
            switch_status(never_fail_status)
            pvz.ignoreZombies(never_fail_status.get())
        elif action==10:
            pvz.win()
        elif action==11:
            pvz.killAllZombies()
        elif action==12:
            pvz.unlock()
        elif action==13:
            putPlants(plantPut_type_combobox.current())
        elif action==14:
            putLadders()
        elif action==15:
            clearPlants()


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
        change_shortcut_window.iconphoto(False,ttk.PhotoImage(file=resource_path(r"res\icon\change.png")))
        change_shortcut_window.tk.call('tk', 'scaling', 4/3)    
        main_window_x = main_window.winfo_x()
        main_window_y = main_window.winfo_y()  
        change_shortcut_window.geometry(f'+{main_window_x+200}+{main_window_y + 200}')

        label = ttk.Label(change_shortcut_window, text='请按下新的快捷键')
        label.pack()

        entry = ttk.Entry(change_shortcut_window)
        entry.pack()
        entry.focus_set()

        # 记录按键
        change_shortcut_window.bind('<Key>', record_key)

        confirm_button = ttk.Button(change_shortcut_window, text='确定',bootstyle=SUCCESS, command=set_new_shortcut)
        confirm_button.place(x=20,y=-10,relx=0,rely=1,anchor=SW)

        cancel_button = ttk.Button(change_shortcut_window, text='取消',bootstyle=DANGER, command=change_shortcut_window.destroy)
        cancel_button.place(x=-20,y=-10,relx=1,rely=1,anchor=SE)

    # 更新快捷键显示
    def update_shortcut_display():
        shortcuts = get_shortcuts()
        for i, (shortcut_id, shortcut_info) in enumerate(shortcuts.items()):
            shortcut_entries[i].delete(0, END)
            shortcut_entries[i].insert(0, shortcut_info['key'])
            shortcut_buttons[i].config(command=lambda i=i, id=shortcut_id, info=shortcut_info: open_change_window(id, info['key'], info['action']))

    shortcut_frame=ttk.LabelFrame(common_page,text="快捷按键")
    shortcut_frame.place(x=180,y=0)
    # 创建快捷键显示文本框和修改按钮
    shortcuts = get_shortcuts()
    for i, (shortcut_id, shortcut_info) in enumerate(shortcuts.items()):
        # 显示快捷键的文本框
        entry = ttk.Entry(shortcut_frame,width=18,font=("黑体",8))
        entry.insert(0, shortcut_info['key'])
        entry.grid(row=i, column=0, padx=2)
        shortcut_entries.append(entry)

        # 修改快捷键的按钮
        button = ttk.Button(shortcut_frame, text='修改',padding=0,bootstyle=(OUTLINE), command=lambda i=i, id=shortcut_id, info=shortcut_info: open_change_window(id, info['key'], info['action']))
        button.grid(row=i, column=1, padx=2)
        shortcut_buttons.append(button)

        
        combobox=ttk.Combobox(shortcut_frame,values=action_list,width=13,state=READONLY)
        combobox.grid(row=i, column=2, padx=2)
        combobox.current(shortcut_info['action'])
        shortcut_comboboxs.append(combobox)
        def modify_action(event,id=shortcut_id,i=i):
            config = load_config(config_file_path)
            modify_shortcut(id, config['shortcuts'][id]["key"], shortcut_comboboxs[i].current())
        combobox.bind("<<ComboboxSelected>>", modify_action)
    # 设置快捷键监听
    try:
        for shortcut_info in shortcuts.values():
            keyboard.add_hotkey(shortcut_info['key'], lambda action=shortcut_info['action']: on_triggered(action))
    except:
        delete_config()

    global zombie_select
    zombie_page=ttk.Frame(page_tab)
    zombie_page.pack()
    page_tab.add(zombie_page,text="僵尸修改")    
    zombie_list_frame=ttk.LabelFrame(zombie_page,text="僵尸列表",bootstyle=DANGER)
    zombie_list_frame.place(x=0,y=0,anchor=NW,height=260,width=275)
    zombie_list_box_scrollbar=ttk.Scrollbar(zombie_list_frame,bootstyle=DANGER)
    zombie_list_box=ttk.Treeview(zombie_list_frame,show=TREE,selectmode=BROWSE,padding=0,columns=("zombie_list"),yscrollcommand=zombie_list_box_scrollbar.set,bootstyle=DANGER)
    zombie_list_box_scrollbar.configure(command=zombie_list_box.yview)
    zombie_list_box.place(x=0,y=0,anchor=NW,height=240,width=50)
    zombie_list_box_scrollbar.place(x=45,y=0,height=240,anchor=NW)
    zombie_list=list()
    def refresh_zombie_list():
        zombie_list.clear()
        zombie_list_box.delete(*zombie_list_box.get_children())
        try:
            zombie_num=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xa0)
        except:
            return
        i=0
        j=0
        while i<zombie_num:
            zombie_addresss=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x90)+0x15c*j
            zombie_exist=data.PVZ_memory.read_bytes(zombie_addresss+0xec,1)
            if(zombie_exist==b'\x00'):
                zombie_list.append(data.zombie(zombie_addresss))
                i=i+1
            j=j+1
        n=0
        for k in range(zombie_num):
            zombie_list_box.insert("",END,iid=n,text=str(zombie_list[k].no))
            if(zombie_select!=None):
                if(zombie_select.exist==0):
                    if(zombie_select.no==zombie_list[k].no):
                        zombie_list_box.selection_set((str(n),))
            n=n+1

    refresh_zombie_list()
    zombie_attribute_frame=ttk.Frame(zombie_list_frame)
    zombie_attribute_frame.place(x=80,y=0,height=240,width=190)
    zombie_state_frame=ttk.Frame(zombie_attribute_frame)
    zombie_state_frame.grid(row=0,column=0,columnspan=12,sticky=W)
    ttk.Label(zombie_state_frame,text="僵尸类型:").grid(row=0,column=0,columnspan=2,sticky=W)
    zombie_type_value=ttk.IntVar(zombie_state_frame)
    zombie_type_entry=ttk.Entry(zombie_state_frame,textvariable=zombie_type_value,width=18,font=("黑体",8),state=READONLY,bootstyle=SECONDARY)
    zombie_type_entry.grid(row=0,column=2,columnspan=5,sticky=W)
    ttk.Label(zombie_state_frame,text="状态:").grid(row=1,column=0,sticky=W)
    zombie_state_value=ttk.IntVar(zombie_state_frame)
    zombie_state_entry=ttk.Entry(zombie_state_frame,textvariable=zombie_state_value,width=3,font=("黑体",8),bootstyle=SECONDARY)
    zombie_state_entry.grid(row=1,column=1,sticky=W)
    def setZombieState(event):
        zombie_select.setState(zombie_state_value.get())
        zombie_state_frame.focus_set()
    zombie_state_entry.bind("<Return>",setZombieState)
    ttk.Label(zombie_state_frame,text="大小:").grid(row=1,column=3,sticky=W)
    zombie_size_value=ttk.DoubleVar(zombie_state_frame)
    zombie_size_entry=ttk.Entry(zombie_state_frame,textvariable=zombie_size_value,width=6,font=("黑体",8),bootstyle=SECONDARY)
    zombie_size_entry.grid(row=1,column=4,sticky=W)
    def setZombieSize(event):
        zombie_select.setSize(zombie_size_value.get())
        zombie_state_frame.focus_set()
    zombie_size_entry.bind("<Return>",setZombieSize)
    zombie_position_frame=ttk.LabelFrame(zombie_attribute_frame,text="位置",bootstyle=DANGER)
    zombie_position_frame.grid(row=2,column=0,columnspan=4,sticky=W)
    ttk.Label(zombie_position_frame,text="x坐标:").grid(row=0,column=0,columnspan=3,sticky=W)
    zombie_x_value=ttk.DoubleVar(zombie_position_frame)
    zombie_x_entry=ttk.Entry(zombie_position_frame,textvariable=zombie_x_value,width=6,font=("黑体",8),bootstyle=SECONDARY)
    zombie_x_entry.grid(row=0,column=3,columnspan=3,sticky=W)
    def setZombieX(event):
        print(zombie_x_value.get())
        zombie_select.setX(zombie_x_value.get())
        zombie_position_frame.focus_set()
    zombie_x_entry.bind("<Return>",setZombieX)
    ttk.Label(zombie_position_frame,text="y坐标:").grid(row=1,column=0,columnspan=3,sticky=W)
    zombie_y_value=ttk.DoubleVar(zombie_position_frame)
    zombie_y_entry=ttk.Entry(zombie_position_frame,textvariable=zombie_y_value,width=6,font=("黑体",8),bootstyle=SECONDARY)
    zombie_y_entry.grid(row=1,column=3,columnspan=3,sticky=W)
    def setZombieY(event):
        zombie_select.setY(zombie_y_value.get())
        zombie_position_frame.focus_set()
    zombie_y_entry.bind("<Return>",setZombieY)
    ttk.Label(zombie_position_frame,text="第").grid(row=2,column=0,sticky=W)
    zombie_row_value=ttk.IntVar(zombie_position_frame)
    zombie_row_combobox=ttk.Combobox(zombie_position_frame,textvariable=zombie_row_value,width=2,values=[1,2,3,4,5,6],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    zombie_row_combobox.grid(row=2,column=1,columnspan=3,sticky=W)
    ttk.Label(zombie_position_frame,text="行").grid(row=2,column=4,sticky=W)
    def setZombieRow(event):
        zombie_select.setRow(zombie_row_value.get())
        zombie_position_frame.focus_set()
    zombie_row_combobox.bind("<<ComboboxSelected>>",setZombieRow)
    zombie_hp_frame=ttk.LabelFrame(zombie_attribute_frame,text="血量",bootstyle=DANGER)
    zombie_hp_frame.grid(row=2,column=4,columnspan=8,sticky=W)
    zombie_hp_frame.grid_columnconfigure(0,minsize=50)
    ttk.Label(zombie_hp_frame,text="本体:").grid(row=0,column=0)
    zombie_hp_value=ttk.IntVar(zombie_hp_frame)
    zombie_hp_entry=ttk.Entry(zombie_hp_frame,textvariable=zombie_hp_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    zombie_hp_entry.grid(row=0,column=1,ipady=0)
    def setZombieHP(event):
        zombie_select.setHP(zombie_hp_value.get())
        zombie_hp_frame.focus_set()
    zombie_hp_entry.bind("<Return>",setZombieHP)
    zombie_hatHP_label=ttk.Label(zombie_hp_frame,text="帽子:")
    zombie_hatHP_label.grid(row=1,column=0)
    zombie_hatHP_value=ttk.IntVar(zombie_hp_frame)
    zombie_hatHP_entry=ttk.Entry(zombie_hp_frame,textvariable=zombie_hatHP_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    zombie_hatHP_entry.grid(row=1,column=1,ipady=0)
    def setZombieHatHP(event):
        zombie_select.setHatHP(zombie_hatHP_value.get())
        zombie_hp_frame.focus_set()
    zombie_hatHP_entry.bind("<Return>",setZombieHatHP)
    ttk.Label(zombie_hp_frame,text="铁门:").grid(row=2,column=0,padx=(2,0))
    zombie_doorHP_value=ttk.IntVar(zombie_hp_frame)
    zombie_doorHP_entry=ttk.Entry(zombie_hp_frame,textvariable=zombie_doorHP_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    zombie_doorHP_entry.grid(row=2,column=1,ipady=0)
    def setZombieDoorHP(event):
        zombie_select.setDoorHP(zombie_doorHP_value.get())
        zombie_hp_frame.focus_set()
    zombie_doorHP_entry.bind("<Return>",setZombieDoorHP)
    zombie_control_frame=ttk.LabelFrame(zombie_attribute_frame,text="控制时间",bootstyle=DANGER)
    zombie_control_frame.grid(row=3,column=0,columnspan=3,sticky=W)
    ttk.Label(zombie_control_frame,text="减速:").grid(row=0,column=0)
    zombie_slow_value=ttk.IntVar(zombie_control_frame)
    zombie_slow_entry=ttk.Entry(zombie_control_frame,textvariable=zombie_slow_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    zombie_slow_entry.grid(row=0,column=1,ipady=0)
    def setZombieSlow(event):
        zombie_select.setSlow(zombie_slow_value.get())
        zombie_control_frame.focus_set()
    zombie_slow_entry.bind("<Return>",setZombieSlow)
    zombie_butter_label=ttk.Label(zombie_control_frame,text="黄油:")
    zombie_butter_label.grid(row=1,column=0)
    zombie_butter_value=ttk.IntVar(zombie_control_frame)
    zombie_butter_entry=ttk.Entry(zombie_control_frame,textvariable=zombie_butter_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    zombie_butter_entry.grid(row=1,column=1,ipady=0)
    def setZombieButter(event):
        zombie_select.setButter(zombie_butter_value.get())
        zombie_control_frame.focus_set()
    zombie_butter_entry.bind("<Return>",setZombieButter)
    ttk.Label(zombie_control_frame,text="冻结:").grid(row=2,column=0,padx=(2,0))
    zombie_frozen_value=ttk.IntVar(zombie_control_frame)
    zombie_frozen_entry=ttk.Entry(zombie_control_frame,textvariable=zombie_frozen_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    zombie_frozen_entry.grid(row=2,column=1,ipady=0)
    def setZombieFrozen(event):
        zombie_select.setFrozen(zombie_frozen_value.get())
        zombie_control_frame.focus_set()
    zombie_frozen_entry.bind("<Return>",setZombieFrozen)
    zombie_flag_frame=ttk.LabelFrame(zombie_attribute_frame,text="状态标志",bootstyle=DANGER)
    zombie_flag_frame.grid(row=3,column=3,columnspan=8,sticky=W)
    zombie_exist_flag=ttk.BooleanVar(zombie_flag_frame)
    def change_zombie_exist():
        if(zombie_exist_flag.get()==False):
            zombie_select.setExist(2)
    ttk.Checkbutton(zombie_flag_frame,text="存在",bootstyle="danger-round-toggle",variable=zombie_exist_flag,command=lambda:change_zombie_exist()).grid(row=0,column=0)
    zombie_isVisible_flag=ttk.BooleanVar(zombie_flag_frame)
    def change_zombie_isVisible():
        zombie_select.setIsVisible(not zombie_isVisible_flag.get())
    ttk.Checkbutton(zombie_flag_frame,text="隐形",bootstyle="danger-round-toggle",variable=zombie_isVisible_flag,command=lambda:change_zombie_isVisible()).grid(row=0,column=1)
    zombie_isEating_flag=ttk.BooleanVar(zombie_flag_frame)
    def change_zombie_isEating():
        zombie_select.setIsEating(zombie_isEating_flag.get())
    ttk.Checkbutton(zombie_flag_frame,text="啃咬",bootstyle="danger-round-toggle",variable=zombie_isEating_flag,command=lambda:change_zombie_isEating()).grid(row=1,column=0)
    zombie_isHpynotized_flag=ttk.BooleanVar(zombie_flag_frame)
    def change_zombie_isHpynotized():
        zombie_select.setIsHPynotized(zombie_isHpynotized_flag.get())
    ttk.Checkbutton(zombie_flag_frame,text="魅惑",bootstyle="danger-round-toggle",variable=zombie_isHpynotized_flag,command=lambda:change_zombie_isHpynotized()).grid(row=1,column=1)
    zombie_isBlow_flag=ttk.BooleanVar(zombie_flag_frame)
    def change_zombie_isBlow():
        zombie_select.setIsBlow(zombie_isBlow_flag.get())
    ttk.Checkbutton(zombie_flag_frame,text="吹飞",bootstyle="danger-round-toggle",variable=zombie_isBlow_flag,command=lambda:change_zombie_isBlow()).grid(row=2,column=0)
    zombie_isDying_flag=ttk.BooleanVar(zombie_flag_frame)
    def change_zombie_isDying():
        zombie_select.setIsDying(not zombie_isDying_flag.get())
    ttk.Checkbutton(zombie_flag_frame,text="濒死",bootstyle="danger-round-toggle",variable=zombie_isDying_flag,command=lambda:change_zombie_isDying()).grid(row=2,column=1)

    zombie_put_frame=ttk.LabelFrame(zombie_page,text="放置僵尸",bootstyle=DANGER)
    zombie_put_frame.place(x=280,y=0,anchor=NW,height=100,width=130)
    ttk.Label(zombie_put_frame,text="第").grid(row=0,column=0)
    zombiePut_start_row_value=ttk.IntVar(zombie_put_frame)
    zombiePut_start_row_combobox=ttk.Combobox(zombie_put_frame,textvariable=zombiePut_start_row_value,width=2,values=[1,2,3,4,5,6],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    zombiePut_start_row_combobox.grid(row=0,column=1)
    zombiePut_start_row_value.set(1)
    ttk.Label(zombie_put_frame,text="行").grid(row=0,column=2)
    zombiePut_start_col_value=ttk.IntVar(zombie_put_frame)
    zombiePut_start_col_combobox=ttk.Combobox(zombie_put_frame,textvariable=zombiePut_start_col_value,width=2,values=[1,2,3,4,5,6,7,8,9,10,11,12],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    zombiePut_start_col_combobox.grid(row=0,column=3)
    zombiePut_start_col_value.set(1)
    ttk.Label(zombie_put_frame,text="列").grid(row=0,column=4)
    ttk.Label(zombie_put_frame,text="至").grid(row=1,column=0)
    zombiePut_end_row_value=ttk.IntVar(zombie_put_frame)
    zombiePut_end_row_combobox=ttk.Combobox(zombie_put_frame,textvariable=zombiePut_end_row_value,width=2,values=[1,2,3,4,5,6],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    zombiePut_end_row_combobox.grid(row=1,column=1)
    zombiePut_end_row_value.set(1)
    ttk.Label(zombie_put_frame,text="行").grid(row=1,column=2)
    zombiePut_end_col_value=ttk.IntVar(zombie_put_frame)
    zombiePut_end_col_combobox=ttk.Combobox(zombie_put_frame,textvariable=zombiePut_end_col_value,width=2,values=[1,2,3,4,5,6,7,8,9,10,11,12],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    zombiePut_end_col_combobox.grid(row=1,column=3)
    zombiePut_end_col_value.set(1)
    ttk.Label(zombie_put_frame,text="列").grid(row=1,column=4)
    zombiePut_type_combobox=ttk.Combobox(zombie_put_frame,width=7,values=data.zombiesType,font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    zombiePut_type_combobox.grid(row=2,column=0,columnspan=4,sticky=W)
    zombiePut_type_combobox.current(0)
    def putZombies(type):
        startRow=zombiePut_start_row_value.get()-1
        startCol=zombiePut_start_col_value.get()-1
        endRow=zombiePut_end_row_value.get()-1
        endCol=zombiePut_end_col_value.get()-1
        if(type==25):
            pvz.putBoss
        print(startRow,startCol,endRow,endCol,type)
        if(pvz.getMap!=False):
            rows=pvz.getMap()-1
            if startRow>rows:
                startRow=rows
            if endRow>rows:
                endRow=rows
            if startRow>endRow or startCol>endCol:
                Messagebox.show_error("起始行列大于终止行列",title="输入错误")
            else:
                for i in range(startRow,endRow+1):
                    for j in range(startCol,endCol+1):
                        pvz.putZombie(i,j,type)
    ttk.Button(zombie_put_frame,text="放置僵尸",padding=0,bootstyle=(OUTLINE,DANGER),command=lambda:putZombies(zombiePut_type_combobox.current())).grid(row=2,column=0,columnspan=5,sticky=E)

    zombie_seed_frame=ttk.LabelFrame(zombie_page,text="修改出怪",bootstyle=DANGER)
    zombie_seed_frame.place(x=280,y=110,anchor=NW,height=100,width=130)
    pausee_spawn_status=ttk.BooleanVar(zombie_seed_frame)
    pausee_spawn_check=ttk.Checkbutton(zombie_seed_frame,text="暂停刷怪",variable=pausee_spawn_status,bootstyle="success-round-toggle",command=lambda:pvz.pauseSpawn(pausee_spawn_status.get()))
    pausee_spawn_check.grid(row=0,column=0,sticky=W)

    def get_zombie_select(event):
        global zombie_select
        try:
            index=int(zombie_list_box.selection()[0])
            zombie_select=zombie_list[index]
        except:
            return

    def get_zombie_attribute():
        global zombie_select
        if zombie_select!=None:
            try:
                zombie_type_value.set(str(zombie_select.type)+":"+data.zombiesType[zombie_select.type])
                if(zombie_attribute_frame.focus_get()!=zombie_state_entry):
                    zombie_state_value.set(zombie_select.state)
                if(zombie_attribute_frame.focus_get()!=zombie_size_entry):
                    zombie_size_value.set(zombie_select.size)
                if(zombie_attribute_frame.focus_get()!=zombie_x_entry):
                    zombie_x_value.set(round(zombie_select.x,2))
                if(zombie_attribute_frame.focus_get()!=zombie_y_entry):
                    zombie_y_value.set(round(zombie_select.y,2))
                zombie_row_value.set(zombie_select.row)
                if(zombie_attribute_frame.focus_get()!=zombie_hp_entry):
                    zombie_hp_value.set(zombie_select.hp)
                if(zombie_select.hatType==0):
                    zombie_hatHP_label["text"]="无:"
                elif(zombie_select.hatType==1):
                    zombie_hatHP_label["text"]="路障:"
                elif(zombie_select.hatType==2):
                    zombie_hatHP_label["text"]="铁桶:"
                elif(zombie_select.hatType==3):
                    zombie_hatHP_label["text"]="橄榄帽:"
                elif(zombie_select.hatType==4):
                    zombie_hatHP_label["text"]="矿工帽:"
                elif(zombie_select.hatType==7):
                    zombie_hatHP_label["text"]="雪橇车:"
                elif(zombie_select.hatType==8):
                    zombie_hatHP_label["text"]="坚果:"
                elif(zombie_select.hatType==9):
                    zombie_hatHP_label["text"]="高冰果:"
                elif(zombie_select.hatType==10):
                    zombie_hatHP_label["text"]="钢盔:"
                elif(zombie_select.hatType==11):
                    zombie_hatHP_label["text"]="绿帽:"
                else:
                    zombie_hatHP_label["text"]=str(zombie_select.hatType)+"未知:"
                if(zombie_attribute_frame.focus_get()!=zombie_hatHP_entry):
                    zombie_hatHP_value.set(zombie_select.hatHP)
                if(zombie_attribute_frame.focus_get()!=zombie_doorHP_entry):
                    zombie_doorHP_value.set(zombie_select.doorHP)
                if(zombie_attribute_frame.focus_get()!=zombie_slow_entry):
                    zombie_slow_value.set(zombie_select.slow)
                if(zombie_attribute_frame.focus_get()!=zombie_butter_entry):
                    zombie_butter_value.set(zombie_select.butter)
                if(zombie_attribute_frame.focus_get()!=zombie_frozen_entry):
                    zombie_frozen_value.set(zombie_select.frozen)
                if(zombie_select.exist==0):
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

    zombie_list_box.bind("<<TreeviewSelect>>",get_zombie_select)


    plant_page=ttk.Frame(page_tab)
    plant_page.pack()
    page_tab.add(plant_page,text="植物修改")    
    plant_list_frame=ttk.LabelFrame(plant_page,text="植物列表",bootstyle=SUCCESS)
    plant_list_frame.place(x=0,y=0,anchor=NW,height=390,width=235)
    plant_list_box_scrollbar=ttk.Scrollbar(plant_list_frame,bootstyle=SUCCESS)
    plant_list_box=ttk.Treeview(plant_list_frame,show=TREE,selectmode=BROWSE,padding=0,columns=("plant_list"),yscrollcommand=plant_list_box_scrollbar.set,bootstyle=SUCCESS)
    plant_list_box_scrollbar.configure(command=plant_list_box.yview)
    plant_list_box.place(x=0,y=0,anchor=NW,height=370,width=50)
    plant_list_box_scrollbar.place(x=45,y=0,height=370,anchor=NW)
    plant_list=list()
    def refresh_plant_list():
        plant_list.clear()
        plant_list_box.delete(*plant_list_box.get_children())
        try:
            plant_num=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xbc)
        except:
            return
        i=0
        j=0
        while i<plant_num:
            plant_addresss=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xac)+0x14c*j
            plant_exist=data.PVZ_memory.read_bytes(plant_addresss+0x141,1)
            if(plant_exist==b'\x00'):
                plant_list.append(data.plant(plant_addresss))
                i=i+1
            j=j+1
        n=0
        for k in range(plant_num):
            plant_list_box.insert("",END,iid=n,text=str(plant_list[k].no))
            if(plant_select!=None):
                if(plant_select.exist==0):
                    if(plant_select.no==plant_list[k].no):
                        plant_list_box.selection_set((str(n),))
            n=n+1

    refresh_plant_list()
    plant_attribute_frame=ttk.Frame(plant_list_frame)
    plant_attribute_frame.place(x=80,y=0,height=370,width=150)
    plant_state_frame=ttk.Frame(plant_attribute_frame)
    plant_state_frame.grid(row=0,column=0,columnspan=12,sticky=W)
    ttk.Label(plant_state_frame,text="植物类型:").grid(row=0,column=0,columnspan=2,sticky=W)
    plant_type_value=ttk.IntVar(plant_state_frame)
    plant_type_entry=ttk.Entry(plant_state_frame,textvariable=plant_type_value,width=12,font=("黑体",8),state=READONLY,bootstyle=SECONDARY)
    plant_type_entry.grid(row=0,column=2,columnspan=5,sticky=W)
    ttk.Label(plant_state_frame,text="状态:").grid(row=1,column=0,sticky=W)
    plant_state_value=ttk.IntVar(plant_state_frame)
    plant_state_entry=ttk.Entry(plant_state_frame,textvariable=plant_state_value,width=3,font=("黑体",8),bootstyle=SECONDARY)
    plant_state_entry.grid(row=1,column=1,sticky=W)
    def setPlantState(event):
        plant_select.setState(plant_state_value.get())
        plant_state_frame.focus_set()
    plant_state_entry.bind("<Return>",setPlantState)
    plant_position_frame=ttk.LabelFrame(plant_attribute_frame,text="位置",bootstyle=SUCCESS)
    plant_position_frame.grid(row=2,column=0,columnspan=4,sticky=W)
    ttk.Label(plant_position_frame,text="x坐标:").grid(row=0,column=0,columnspan=3,sticky=W)
    plant_x_value=ttk.IntVar(plant_position_frame)
    plant_x_entry=ttk.Entry(plant_position_frame,textvariable=plant_x_value,width=6,font=("黑体",8),bootstyle=SECONDARY)
    plant_x_entry.grid(row=0,column=3,columnspan=3,sticky=W)
    def setPlantX(event):
        print(plant_x_value.get())
        plant_select.setX(plant_x_value.get())
        plant_position_frame.focus_set()
    plant_x_entry.bind("<Return>",setPlantX)
    ttk.Label(plant_position_frame,text="y坐标:").grid(row=1,column=0,columnspan=3,sticky=W)
    plant_y_value=ttk.IntVar(plant_position_frame)
    plant_y_entry=ttk.Entry(plant_position_frame,textvariable=plant_y_value,width=6,font=("黑体",8),bootstyle=SECONDARY)
    plant_y_entry.grid(row=1,column=3,columnspan=3,sticky=W)
    def setPlantY(event):
        plant_select.setY(plant_y_value.get())
        plant_position_frame.focus_set()
    plant_y_entry.bind("<Return>",setPlantY)
    plant_row_value=ttk.IntVar(plant_position_frame)
    plant_row_combobox=ttk.Combobox(plant_position_frame,textvariable=plant_row_value,width=2,values=[1,2,3,4,5,6],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    plant_row_combobox.grid(row=2,column=1,columnspan=3,sticky=W)
    ttk.Label(plant_position_frame,text="行").grid(row=2,column=4,sticky=W)
    def setPlantRow(event):
        plant_select.setRow(plant_row_value.get())
        plant_position_frame.focus_set()
    plant_row_combobox.bind("<<ComboboxSelected>>",setPlantRow)
    plant_col_value=ttk.IntVar(plant_position_frame)
    plant_col_combobox=ttk.Combobox(plant_position_frame,textvariable=plant_col_value,width=2,values=[1,2,3,4,5,6,7,8,9],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    plant_col_combobox.grid(row=2,column=5,columnspan=3,sticky=W)
    ttk.Label(plant_position_frame,text="列").grid(row=2,column=8,sticky=W)
    def setPlantCol(event):
        plant_select.setCol(plant_col_value.get())
        plant_position_frame.focus_set()
    plant_col_combobox.bind("<<ComboboxSelected>>",setPlantCol)
    ttk.Label(plant_state_frame,text="血量:").grid(row=1,column=3)
    plant_hp_value=ttk.IntVar(plant_state_frame)
    plant_hp_entry=ttk.Entry(plant_state_frame,textvariable=plant_hp_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    plant_hp_entry.grid(row=1,column=4,ipady=0)
    def setPlantHP(event):
        plant_select.setHP(plant_hp_value.get())
        plant_state_frame.focus_set()
    plant_hp_entry.bind("<Return>",setPlantHP)
    plant_time_frame=ttk.LabelFrame(plant_attribute_frame,text="倒计时",bootstyle=SUCCESS)
    plant_time_frame.grid(row=3,column=0,columnspan=3,sticky=W)
    plant_dietime_label=ttk.Label(plant_time_frame,text="死亡:")
    plant_dietime_label.grid(row=0,column=0)
    ToolTip(plant_dietime_label,text="部分具有存在时间植物死亡倒计时",bootstyle=(INFO,INVERSE))
    plant_dietime_value=ttk.IntVar(plant_time_frame)
    plant_dietime_entry=ttk.Entry(plant_time_frame,textvariable=plant_dietime_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    plant_dietime_entry.grid(row=0,column=1,ipady=0)
    def setPlantDieTime(event):
        plant_select.setDieTime(plant_dietime_value.get())
        plant_time_frame.focus_set()
    plant_dietime_entry.bind("<Return>",setPlantDieTime)
    plant_cindertime_label=ttk.Label(plant_time_frame,text="灰烬:")
    plant_cindertime_label.grid(row=1,column=0)
    ToolTip(plant_cindertime_label,text="部分灰烬生效、女大消失倒计时",bootstyle=(INFO,INVERSE))
    plant_cindertime_value=ttk.IntVar(plant_time_frame)
    plant_cindertime_entry=ttk.Entry(plant_time_frame,textvariable=plant_cindertime_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    plant_cindertime_entry.grid(row=1,column=1,ipady=0)
    def setPlantCinderTime(event):
        plant_select.setCinderTime(plant_cindertime_value.get())
        plant_time_frame.focus_set()
    plant_cindertime_entry.bind("<Return>",setPlantCinderTime)
    plant_effecttime_label=ttk.Label(plant_time_frame,text="效果:")
    plant_effecttime_label.grid(row=2,column=0,padx=(2,0))
    ToolTip(plant_effecttime_label,text="部分植物变大、产生效果倒计时",bootstyle=(INFO,INVERSE))
    plant_effecttime_value=ttk.IntVar(plant_time_frame)
    plant_effecttime_entry=ttk.Entry(plant_time_frame,textvariable=plant_effecttime_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    plant_effecttime_entry.grid(row=2,column=1,ipady=0)
    def setPlantEffectTime(event):
        plant_select.setEffectTime(plant_effecttime_value.get())
        plant_time_frame.focus_set()
    plant_effecttime_entry.bind("<Return>",setPlantEffectTime)
    plant_producttime_label=ttk.Label(plant_time_frame,text="攻击:")
    plant_producttime_label.grid(row=3,column=0,padx=(2,0))
    ToolTip(plant_producttime_label,text="部分植物攻击倒计时",bootstyle=(INFO,INVERSE))
    plant_producttime_value=ttk.IntVar(plant_time_frame)
    plant_producttime_entry=ttk.Entry(plant_time_frame,textvariable=plant_producttime_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    plant_producttime_entry.grid(row=3,column=1,ipady=0)
    def setPlantProductTime(event):
        plant_select.setProductTime(plant_producttime_value.get())
        plant_time_frame.focus_set()
    plant_producttime_entry.bind("<Return>",setPlantProductTime)
    plant_productinterval_label=ttk.Label(plant_time_frame,text="间隔:")
    plant_productinterval_label.grid(row=4,column=0,padx=(2,0))
    ToolTip(plant_productinterval_label,text="上述植物攻击间隔",bootstyle=(INFO,INVERSE))
    plant_productinterval_value=ttk.IntVar(plant_time_frame)
    plant_productinterval_entry=ttk.Entry(plant_time_frame,textvariable=plant_productinterval_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    plant_productinterval_entry.grid(row=4,column=1,ipady=0)
    def setPlantProductInterval(event):
        plant_select.setProductInterval(plant_productinterval_value.get())
        plant_time_frame.focus_set()
    plant_productinterval_entry.bind("<Return>",setPlantProductInterval)
    plant_attacktime_label=ttk.Label(plant_time_frame,text="射击:")
    plant_attacktime_label.grid(row=5,column=0,padx=(2,0))
    ToolTip(plant_attacktime_label,text="部分植物攻击倒计时",bootstyle=(INFO,INVERSE))
    plant_attacktime_value=ttk.IntVar(plant_time_frame)
    plant_attacktime_entry=ttk.Entry(plant_time_frame,textvariable=plant_attacktime_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    plant_attacktime_entry.grid(row=5,column=1,ipady=0)
    def setPlantAttackTime(event):
        plant_select.setAttackTime(plant_attacktime_value.get())
        plant_time_frame.focus_set()
    plant_attacktime_entry.bind("<Return>",setPlantAttackTime)
    plant_suntime_label=ttk.Label(plant_time_frame,text="阳光:")
    plant_suntime_label.grid(row=6,column=0,padx=(2,0))
    ToolTip(plant_suntime_label,text="女王产生阳光倒计时",bootstyle=(INFO,INVERSE))
    plant_suntime_value=ttk.IntVar(plant_time_frame)
    plant_suntime_entry=ttk.Entry(plant_time_frame,textvariable=plant_suntime_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    plant_suntime_entry.grid(row=6,column=1,ipady=0)
    def setPlantSunTime(event):
        plant_select.setSunTime(plant_suntime_value.get())
        plant_time_frame.focus_set()
    plant_suntime_entry.bind("<Return>",setPlantSunTime)
    plant_humtime_label=ttk.Label(plant_time_frame,text="阳光:")
    plant_humtime_label.grid(row=7,column=0,padx=(2,0))
    ToolTip(plant_humtime_label,text="汉堡王产生阳光倒计时",bootstyle=(INFO,INVERSE))
    plant_humtime_value=ttk.IntVar(plant_time_frame)
    plant_humtime_entry=ttk.Entry(plant_time_frame,textvariable=plant_humtime_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    plant_humtime_entry.grid(row=7,column=1,ipady=0)
    def setPlantHumTime(event):
        plant_select.setHumTime(plant_humtime_value.get())
        plant_time_frame.focus_set()
    plant_humtime_entry.bind("<Return>",setPlantHumTime)
    plant_flag_frame=ttk.LabelFrame(plant_attribute_frame,text="状态标志",bootstyle=SUCCESS)
    plant_flag_frame.grid(row=3,column=3,columnspan=8,sticky=W)
    plant_exist_flag=ttk.BooleanVar(plant_flag_frame)
    def change_plant_exist():
        plant_select.setExist(not plant_exist_flag.get())
    ttk.Checkbutton(plant_flag_frame,text="存在",bootstyle="success-round-toggle",variable=plant_exist_flag,command=lambda:change_plant_exist()).grid(row=0,column=0)
    plant_isVisible_flag=ttk.BooleanVar(plant_flag_frame)
    def change_plant_isVisible():
        plant_select.setIsVisible(not plant_isVisible_flag.get())
    ttk.Checkbutton(plant_flag_frame,text="隐形",bootstyle="success-round-toggle",variable=plant_isVisible_flag,command=lambda:change_plant_isVisible()).grid(row=1,column=0)
    plant_isAttack_flag=ttk.BooleanVar(plant_flag_frame)
    def change_plant_isAttack():
        plant_select.setIsAttack(plant_isAttack_flag.get())
    ttk.Checkbutton(plant_flag_frame,text="攻击",bootstyle="success-round-toggle",variable=plant_isAttack_flag,command=lambda:change_plant_isAttack()).grid(row=2,column=0)
    plant_isSquash_flag=ttk.BooleanVar(plant_flag_frame)
    def change_plant_isSquash():
        plant_select.setIsSquash(plant_isSquash_flag.get())
    ttk.Checkbutton(plant_flag_frame,text="压扁",bootstyle="success-round-toggle",variable=plant_isSquash_flag,command=lambda:change_plant_isSquash()).grid(row=3,column=0)
    plant_isSleep_flag=ttk.BooleanVar(plant_flag_frame)
    def change_plant_isSleep():
        plant_select.setIsSleep(plant_isSleep_flag.get())
    ttk.Checkbutton(plant_flag_frame,text="睡眠",bootstyle="success-round-toggle",variable=plant_isSleep_flag,command=lambda:change_plant_isSleep()).grid(row=4,column=0)
    
    plant_put_frame=ttk.LabelFrame(plant_page,text="种植",bootstyle=SUCCESS)
    plant_put_frame.place(x=240,y=0,anchor=NW,height=120,width=130)
    ttk.Label(plant_put_frame,text="第").grid(row=0,column=0)
    plantPut_start_row_value=ttk.IntVar(plant_put_frame)
    plantPut_start_row_combobox=ttk.Combobox(plant_put_frame,textvariable=plantPut_start_row_value,width=2,values=[1,2,3,4,5,6],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    plantPut_start_row_combobox.grid(row=0,column=1)
    plantPut_start_row_value.set(1)
    ttk.Label(plant_put_frame,text="行").grid(row=0,column=2)
    plantPut_start_col_value=ttk.IntVar(plant_put_frame)
    plantPut_start_col_combobox=ttk.Combobox(plant_put_frame,textvariable=plantPut_start_col_value,width=2,values=[1,2,3,4,5,6,7,8,9],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    plantPut_start_col_combobox.grid(row=0,column=3)
    plantPut_start_col_value.set(1)
    ttk.Label(plant_put_frame,text="列").grid(row=0,column=4)
    ttk.Label(plant_put_frame,text="至").grid(row=1,column=0)
    plantPut_end_row_value=ttk.IntVar(plant_put_frame)
    plantPut_end_row_combobox=ttk.Combobox(plant_put_frame,textvariable=plantPut_end_row_value,width=2,values=[1,2,3,4,5,6],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    plantPut_end_row_combobox.grid(row=1,column=1)
    plantPut_end_row_value.set(1)
    ttk.Label(plant_put_frame,text="行").grid(row=1,column=2)
    plantPut_end_col_value=ttk.IntVar(plant_put_frame)
    plantPut_end_col_combobox=ttk.Combobox(plant_put_frame,textvariable=plantPut_end_col_value,width=2,values=[1,2,3,4,5,6,7,8,9],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    plantPut_end_col_combobox.grid(row=1,column=3)
    plantPut_end_col_value.set(1)
    ttk.Label(plant_put_frame,text="列").grid(row=1,column=4)
    plantPut_type_combobox=ttk.Combobox(plant_put_frame,width=10,values=data.plantPutType,font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    plantPut_type_combobox.grid(row=2,column=0,columnspan=4,sticky=W)
    plantPut_type_combobox.current(0)
    def putPlants(type):
        startRow=plantPut_start_row_value.get()-1
        startCol=plantPut_start_col_value.get()-1
        endRow=plantPut_end_row_value.get()-1
        endCol=plantPut_end_col_value.get()-1
        if(type>=52):
            type=type+23
        print(startRow,startCol,endRow,endCol,type)
        if(pvz.getMap!=False):
            rows=pvz.getMap()-1
            if startRow>rows:
                startRow=rows
            if endRow>rows:
                endRow=rows
            if startRow>endRow or startCol>endCol:
                Messagebox.show_error("起始行列大于终止行列",title="输入错误")
            else:
                for i in range(startRow,endRow+1):
                    for j in range(startCol,endCol+1):
                        pvz.putPlant(i,j,type)
    ttk.Button(plant_put_frame,text="种植",padding=0,bootstyle=(OUTLINE,SUCCESS),command=lambda:putPlants(plantPut_type_combobox.current())).grid(row=2,column=0,columnspan=5,sticky=E)
    def clearPlants():
        try:
            plant_num=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xbc)
        except:
            return
        i=0
        j=0
        while i<plant_num:
            plant_addresss=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0xac)+0x14c*j
            plant_exist=data.PVZ_memory.read_bytes(plant_addresss+0x141,1)
            if(plant_exist==b'\x00'):
                data.PVZ_memory.write_bytes(plant_addresss+0x141,b'\x01',1)
                i=i+1
            j=j+1
    ttk.Button(plant_put_frame,text="清空所有植物",padding=0,bootstyle=(OUTLINE,SUCCESS),command=lambda:clearPlants()).grid(row=3,column=0,columnspan=5,pady=(5,0),sticky=W)

    plant_characteristic_frame=ttk.Labelframe(plant_page,text="基础属性",bootstyle=SUCCESS)
    plant_characteristic_frame.place(x=240,y=130,anchor=NW,height=140,width=130)
    plant_type_combobox=ttk.Combobox(plant_characteristic_frame,width=10,values=data.plantsType,font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    plant_type_combobox.grid(row=0,column=0,columnspan=4,sticky=W)
    ttk.Label(plant_characteristic_frame,text="阳光:").grid(row=1,column=0)
    plant_characteristic_sun_value=ttk.IntVar(plant_characteristic_frame)
    plant_characteristic_sun_entry=ttk.Entry(plant_characteristic_frame,textvariable=plant_characteristic_sun_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    plant_characteristic_sun_entry.grid(row=1,column=1,ipady=0)
    def setPlantCharacteristicSun(event):
        plant_characteristic_type.setSun(plant_characteristic_sun_value.get())
        plant_characteristic_frame.focus_set()
    plant_characteristic_sun_entry.bind("<Return>",setPlantCharacteristicSun)
    plant_characteristic_cd_label=ttk.Label(plant_characteristic_frame,text="冷却:")
    plant_characteristic_cd_label.grid(row=2,column=0)
    plant_characteristic_cd_value=ttk.IntVar(plant_characteristic_frame)
    plant_characteristic_cd_entry=ttk.Entry(plant_characteristic_frame,textvariable=plant_characteristic_cd_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    plant_characteristic_cd_entry.grid(row=2,column=1,ipady=0)
    def setPlantCharacteristicCd(event):
        plant_characteristic_type.setCd(plant_characteristic_cd_value.get())
        plant_characteristic_frame.focus_set()
    plant_characteristic_cd_entry.bind("<Return>",setPlantCharacteristicCd)
    plant_characteristic_canAttack_flag=ttk.BooleanVar(plant_flag_frame)
    def change_plant_characteristic_canAttack():
        plant_characteristic_type.setCanAttack(plant_characteristic_canAttack_flag.get())
    ttk.Checkbutton(plant_characteristic_frame,text="可攻击",bootstyle="success-round-toggle",variable=plant_characteristic_canAttack_flag,command=lambda:change_plant_characteristic_canAttack()).grid(row=3,column=0,columnspan=4)
    ttk.Label(plant_characteristic_frame,text="攻击间隔:").grid(row=4,column=0)
    plant_characteristic_attackinterval_value=ttk.IntVar(plant_characteristic_frame)
    plant_characteristic_attackinterval_entry=ttk.Entry(plant_characteristic_frame,textvariable=plant_characteristic_attackinterval_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    plant_characteristic_attackinterval_entry.grid(row=4,column=1,ipady=0)
    def setPlantCharacteristicAttackInterval(event):
        plant_characteristic_type.setAttackInterval(zombie_frozen_value.get())
        zombie_control_frame.focus_set()
    zombie_frozen_entry.bind("<Return>",setPlantCharacteristicAttackInterval)

    def get_plant_type(event):
        global plant_characteristic_type
        plant_characteristic_type=data.plantCharacteristic(plant_type_combobox.current())
        plant_characteristic_sun_value.set(plant_characteristic_type.sun)
        plant_characteristic_cd_value.set(plant_characteristic_type.cd)
        plant_characteristic_attackinterval_value.set(plant_characteristic_type.attackInterval)
        plant_characteristic_canAttack_flag.set(plant_characteristic_type.canAttack)
        plant_characteristic_frame.focus_set()
    plant_type_combobox.bind("<<ComboboxSelected>>", get_plant_type)


    def get_plant_select(event):
        global plant_select
        try:
            index=int(plant_list_box.selection()[0])
            plant_select=plant_list[index]
        except:
            return

    def get_plant_attribute():
        global plant_select
        if plant_select!=None:
            try:
                plant_type_value.set(str(plant_select.type)+":"+data.plantsType[plant_select.type])
                if(plant_attribute_frame.focus_get()!=plant_state_entry):
                    plant_state_value.set(plant_select.state)
                if(plant_attribute_frame.focus_get()!=plant_x_entry):
                    plant_x_value.set(plant_select.x)
                if(plant_attribute_frame.focus_get()!=plant_y_entry):
                    plant_y_value.set(plant_select.y)
                plant_row_value.set(plant_select.row)
                plant_col_value.set(plant_select.col)
                if(plant_attribute_frame.focus_get()!=plant_hp_entry):
                    plant_hp_value.set(plant_select.hp)
                if(plant_attribute_frame.focus_get()!=plant_dietime_entry):
                    plant_dietime_value.set(plant_select.dieTime)
                if(plant_attribute_frame.focus_get()!=plant_cindertime_entry):
                    plant_cindertime_value.set(plant_select.cinderTime)
                if(plant_attribute_frame.focus_get()!=plant_effecttime_entry):
                    plant_effecttime_value.set(plant_select.effectTime)
                if(plant_attribute_frame.focus_get()!=plant_producttime_entry):
                    plant_producttime_value.set(plant_select.productTime)
                if(plant_attribute_frame.focus_get()!=plant_attacktime_entry):
                    plant_attacktime_value.set(plant_select.attackTime)
                if(plant_attribute_frame.focus_get()!=plant_productinterval_entry):
                    plant_productinterval_value.set(plant_select.productInterval)
                if(plant_attribute_frame.focus_get()!=plant_suntime_entry):
                    plant_suntime_value.set(plant_select.sunTime)
                if(plant_attribute_frame.focus_get()!=plant_humtime_entry):
                    plant_humtime_value.set(plant_select.humTime)
            except:
                pass
            plant_isVisible_flag.set(not plant_select.isVisible)
            plant_exist_flag.set(not plant_select.exist)
            plant_isAttack_flag.set(plant_select.isAttack)
            plant_isSquash_flag.set(plant_select.isSquash)
            plant_isSleep_flag.set(plant_select.isSleep)

    plant_list_box.bind("<<TreeviewSelect>>",get_plant_select)


    grid_page=ttk.Frame(page_tab)
    grid_page.pack()
    page_tab.add(grid_page,text="场地修改")    
    item_list_frame=ttk.LabelFrame(grid_page,text="物品列表",bootstyle=DARK)
    item_list_frame.place(x=0,y=0,anchor=NW,height=140,width=200)
    item_list_box_scrollbar=ttk.Scrollbar(item_list_frame,bootstyle=DARK)
    item_list_box=ttk.Treeview(item_list_frame,show=TREE,selectmode=BROWSE,padding=0,columns=("item_list"),yscrollcommand=item_list_box_scrollbar.set,bootstyle=DARK)
    item_list_box_scrollbar.configure(command=item_list_box.yview)
    item_list_box.place(x=0,y=0,anchor=NW,height=120,width=70)
    item_list_box_scrollbar.place(x=65,y=0,height=120,anchor=NW)
    item_list=list()
    def refresh_item_list():
        item_list.clear()
        item_list_box.delete(*item_list_box.get_children())
        try:
            item_num=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x12c)
        except:
            return
        i=0
        j=0
        while i<item_num:
            item_addresss=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x11c)+0xec*j
            item_exist=data.PVZ_memory.read_bytes(item_addresss+0x20,1)
            if(item_exist==b'\x00'):
                item_list.append(data.item(item_addresss))
                i=i+1
            j=j+1
        n=0
        for k in range(item_num):
            item_list_box.insert("",END,iid=n,text=str(item_list[k].no)+data.itemType[item_list[k].type])
            if(item_select!=None):
                if(item_select.exist==0):
                    if(item_select.no==item_list[k].no):
                        item_list_box.selection_set((str(n),))
            n=n+1
    refresh_item_list()
    item_attribute_frame=ttk.Frame(item_list_frame)
    item_attribute_frame.place(x=80,y=0,height=120,width=115)
    item_exist_flag=ttk.BooleanVar(item_attribute_frame)
    def change_item_exist():
            item_select.setExist(not item_exist_flag.get())
    ttk.Checkbutton(item_attribute_frame,text="存在",bootstyle="dark-round-toggle",variable=item_exist_flag,command=lambda:change_item_exist()).grid(row=0,column=0,columnspan=4,sticky=W)
    item_row_value=ttk.IntVar(item_attribute_frame)
    item_row_combobox=ttk.Combobox(item_attribute_frame,textvariable=item_row_value,width=2,values=[1,2,3,4,5,6],font=("黑体",8),bootstyle=SECONDARY)
    item_row_combobox.grid(row=1,column=0)
    ttk.Label(item_attribute_frame,text="行").grid(row=1,column=1)
    def setItemRow(event):
        item_select.setRow(item_row_value.get())
        item_attribute_frame.focus_set()
    item_row_combobox.bind("<<ComboboxSelected>>",setItemRow)
    item_col_value=ttk.IntVar(item_attribute_frame)
    item_col_combobox=ttk.Combobox(item_attribute_frame,textvariable=item_col_value,width=2,values=[1,2,3,4,5,6,7,8,9],font=("黑体",8),bootstyle=SECONDARY)
    item_col_combobox.grid(row=1,column=2)
    ttk.Label(item_attribute_frame,text="列").grid(row=1,column=3)
    def setItemCol(event):
        item_select.setCol(item_col_value.get())
        item_attribute_frame.focus_set()
    item_col_combobox.bind("<<ComboboxSelected>>",setItemCol)
    item_time_value=ttk.IntVar(item_attribute_frame)
    def setItemTime(event):
        item_select.setTime(item_time_meter.amountusedvar.get())
        item_attribute_frame.focus_set()
    item_time_meter=ttk.Meter(item_attribute_frame,metersize=80,bootstyle=DARK,amounttotal=18000,showtext=True,metertype="semi",interactive=True,textfont="-size 7",subtext="剩余时间",subtextfont="-size 7",subtextstyle="dark")
    def setItemTimeMeterFocus(event):
        item_time_meter.focus_set()
    item_time_meter.indicator.bind("<Button-1>", setItemTimeMeterFocus)
    item_time_meter.indicator.bind("<ButtonRelease-1>", setItemTime)
    ladder_put_frame=ttk.LabelFrame(grid_page,text="搭梯",bootstyle=DARK)
    ladder_put_frame.place(x=200,y=0,anchor=NW,height=90,width=130)
    ttk.Label(ladder_put_frame,text="第").grid(row=0,column=0)
    ladder_start_row_value=ttk.IntVar(ladder_put_frame)
    item_start_row_combobox=ttk.Combobox(ladder_put_frame,textvariable=ladder_start_row_value,width=2,values=[1,2,3,4,5,6],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    item_start_row_combobox.grid(row=0,column=1)
    ladder_start_row_value.set(1)
    ttk.Label(ladder_put_frame,text="行").grid(row=0,column=2)
    ladder_start_col_value=ttk.IntVar(ladder_put_frame)
    item_start_col_combobox=ttk.Combobox(ladder_put_frame,textvariable=ladder_start_col_value,width=2,values=[1,2,3,4,5,6,7,8,9],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    item_start_col_combobox.grid(row=0,column=3)
    ladder_start_col_value.set(1)
    ttk.Label(ladder_put_frame,text="列").grid(row=0,column=4)
    ttk.Label(ladder_put_frame,text="至").grid(row=1,column=0)
    ladder_end_row_value=ttk.IntVar(ladder_put_frame)
    item_end_row_combobox=ttk.Combobox(ladder_put_frame,textvariable=ladder_end_row_value,width=2,values=[1,2,3,4,5,6],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    item_end_row_combobox.grid(row=1,column=1)
    ladder_end_row_value.set(1)
    ttk.Label(ladder_put_frame,text="行").grid(row=1,column=2)
    ladder_end_col_value=ttk.IntVar(ladder_put_frame)
    item_end_col_combobox=ttk.Combobox(ladder_put_frame,textvariable=ladder_end_col_value,width=2,values=[1,2,3,4,5,6,7,8,9],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    item_end_col_combobox.grid(row=1,column=3)
    ladder_end_col_value.set(1)
    ttk.Label(ladder_put_frame,text="列").grid(row=1,column=4)
    def putLadders():
        startRow=ladder_start_row_value.get()-1
        startCol=ladder_start_col_value.get()-1
        endRow=ladder_end_row_value.get()-1
        endCol=ladder_end_col_value.get()-1
        print(startRow,startCol,endRow,endCol)
        if(pvz.getMap!=False):
            rows=pvz.getMap()-1
            if startRow>rows:
                startRow=rows
            if endRow>rows:
                endRow=rows
            if startRow>endRow or startCol>endCol:
                Messagebox.show_error("起始行列大于终止行列",title="输入错误")
            else:
                for i in range(startRow,endRow+1):
                    for j in range(startCol,endCol+1):
                        pvz.putLadder(i,j)
    ttk.Button(ladder_put_frame,text="搭梯",padding=0,bootstyle=(OUTLINE,DARK),command=lambda:putLadders()).grid(row=2,column=0,columnspan=5,sticky=E)

    def get_item_select(event):
        global item_select
        try:
            index=int(item_list_box.selection()[0])
            item_select=item_list[index]
        except:
            return
    def get_item_attribute():
        global item_select
        if item_select!=None:
            item_exist_flag.set(not item_select.exist)
            item_row_value.set(item_select.row)
            item_col_value.set(item_select.col)
            if(item_select.type==2):
                try:
                    if(item_attribute_frame.focus_get()!=item_time_meter):
                        item_time_value.set(item_select.time)
                        item_time_meter.grid(row=2,column=0,columnspan=4)
                        item_time_meter.configure(amountused=item_time_value.get())
                except:
                    pass
            else:
                item_time_meter.grid_forget()
                
    item_list_box.bind("<<TreeviewSelect>>",get_item_select)


    slot_page=ttk.Frame(page_tab)
    slot_page.pack()
    page_tab.add(slot_page,text="卡槽修改") 
    slots_configuration_mode=ttk.BooleanVar(slot_page)
    slots_configuration_mode.set(False)
    slots_frame=ttk.LabelFrame(slot_page,text="监视模式",bootstyle=SUCCESS)
    slots_frame.place(x=0,y=0)
    slot_list=list()
    def refresh_slot_list():
        slot_list.clear()
        try:
            slot_num=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x144)+0x24)
        except:
            return
        i=0
        while i<slot_num:
            slot_addresss=data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x144)+0x28+0x50*i
            slot_list.append(data.slot(slot_addresss))
            i=i+1
 
    slot_type_comboboxes = []
    slot_elapsed_values = []
    slot_elapsed_entrys = []
    slot_cooldown_values = []
    slot_cooldown_entrys = []
    slot_cd_progressBars = []
    slot_isVisible_flags = []
    # slot_canUse_flags = []
    def create_slot_ui(slot_number):
        ttk.Label(slots_frame, text=f"{slot_number}").grid(row=slot_number-1, column=0, sticky=W)
        ttk.Label(slots_frame, text="植物:").grid(row=slot_number-1, column=1, sticky=W)

        slot_type_combobox = ttk.Combobox(slots_frame, width=12, values=data.plantsType, state='readonly', bootstyle='secondary')
        slot_type_combobox.grid(row=slot_number-1, column=2, sticky=W)
        slot_type_comboboxes.append(slot_type_combobox)

        def set_slot_type(event, index=slot_number-1):
            if(slots_configuration_mode.get()==False):
                slot_list[index].setType(slot_type_combobox.current())
                slots_frame.focus_set()
        slot_type_combobox.bind("<<ComboboxSelected>>", set_slot_type)

        slot_elapsed_value = ttk.IntVar()
        slot_elapsed_values.append(slot_elapsed_value)
        slot_elapsed_entry = ttk.Entry(slots_frame, textvariable=slot_elapsed_value, width=5, font=("黑体", 8), bootstyle='secondary')
        slot_elapsed_entrys.append(slot_elapsed_entry)

        def set_slot_elapsed(event, index=slot_number-1):
            if(slots_configuration_mode.get()==False):
                slot_list[index].setElapsed(slot_elapsed_value.get())
                slots_frame.focus_set()
        slot_elapsed_entry.bind("<Return>", set_slot_elapsed)

        slot_cooldown_value = ttk.IntVar()
        slot_cooldown_values.append(slot_cooldown_value)
        slot_cooldown_entry = ttk.Entry(slots_frame, textvariable=slot_cooldown_value, width=5, font=("黑体", 8), bootstyle='secondary')
        slot_cooldown_entrys.append(slot_cooldown_entry)

        def set_slot_cooldown(event, index=slot_number-1):
            slot_list[index].setCooldown(slot_cooldown_value.get())
            slots_frame.focus_set()
        slot_cooldown_entry.bind("<Return>", set_slot_cooldown)


        slot_cooldown_label = ttk.Label(slots_frame, text="冷却进度")
        slot_cooldown_label.grid(row=slot_number-1, column=3, padx=(2,0))
        slot_cd_progressBar=ttk.Progressbar(slots_frame,length=80,mode=DETERMINATE,maximum=slot_cooldown_value.get(),variable=slot_elapsed_value,bootstyle="success-striped")
        slot_cd_progressBar.grid(row=slot_number-1, column=4, ipady=0)
        slot_cd_progressBars.append(slot_cd_progressBar)    
        def set_cd_progressBar_focus(event):
            if(slots_configuration_mode.get()==False):
                slot_cd_progressBar.focus_set()
        def set_cd_value(event,index=slot_number-1):
            if(slots_configuration_mode.get()==False):
                fraction = event.x / slot_cd_progressBar.winfo_width()
                new_value = int(fraction * slot_cd_progressBar['maximum'])
                slot_elapsed_value.set(new_value)
                slot_list[index].setElapsed(slot_elapsed_value.get())
        slot_cd_progressBar.bind("<Button-1>", set_cd_progressBar_focus)
        slot_cd_progressBar.bind("<ButtonRelease-1>", set_cd_value)
        
        slot_isVisible_flag=ttk.BooleanVar(slots_frame)
        slot_isVisible_flags.append(slot_isVisible_flag)
        def change_slot_isVisible(index=slot_number-1):
            if(slots_configuration_mode.get()==False):
                slot_list[index].setIsVisible(not slot_isVisible_flag.get())
        ttk.Checkbutton(slots_frame,text="隐形",bootstyle="danger-round-toggle",variable=slot_isVisible_flag,command=lambda:change_slot_isVisible()).grid(row=slot_number-1,column=5)
        # slot_canUse_flag=ttk.BooleanVar(slots_frame)
        # slot_canUse_flags.append(slot_canUse_flag)
        # def change_slot_canUse(index=slot_number-1):
        #     slot_list[index].setCanUse(slot_canUse_flag.get())
        # ttk.Checkbutton(slots_frame,text="可用",bootstyle="danger-round-toggle",variable=slot_canUse_flag,command=lambda:change_slot_canUse()).grid(row=slot_number-1,column=6)
    # 为slots 1至14创建UI组件
    for slot_number in range(1, 15):
        create_slot_ui(slot_number)

    slots_config_frame=ttk.LabelFrame(slot_page,text="卡槽设置",bootstyle=SUCCESS)
    slots_config_frame.place(x=0,y=0,relx=1,anchor=NE)
    slot_num_frame=ttk.Frame(slots_config_frame)
    slot_num_frame.pack()
    ttk.Label(slot_num_frame,text="卡槽格数：").pack(side=LEFT)
    slots_num_value=ttk.IntVar()
    slots_num_combobox=ttk.Combobox(slot_num_frame,textvariable=slots_num_value,width=2,values=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],font=("黑体",8),bootstyle=SECONDARY,state=READONLY)
    slots_num_combobox.pack(side=LEFT)
    def setSlotsNum(event):
        data.PVZ_memory.write_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x144)+0x24,slots_num_value.get())
        slot_num_frame.focus_set()
    slots_num_combobox.bind("<<ComboboxSelected>>",setSlotsNum)
    no_slot_status=ttk.BooleanVar(slots_config_frame)
    no_slot_check=ttk.Checkbutton(slots_config_frame,text="无需选卡",variable=no_slot_status,bootstyle="success-round-toggle",command=lambda:pvz.noSolt(no_slot_status.get()))
    no_slot_check.pack(pady=10,anchor=W)
    ToolTip(no_slot_check,text="可以不选卡片即开始游戏",bootstyle=(INFO,INVERSE))
    change_all_frame=ttk.Frame(slots_config_frame)
    change_all_frame.pack(pady=(0,10))
    ttk.Label(change_all_frame,text="修改所有卡槽：").pack(anchor=W)
    change_all_combobox = ttk.Combobox(change_all_frame, width=12, values=data.plantsType, state='readonly', bootstyle='secondary')
    change_all_combobox.pack()
    def change_all_slots(event):
        if(slots_configuration_mode.get()==False):
            for slot in slot_list:
                slot.setType(change_all_combobox.current())
    change_all_combobox.bind("<<ComboboxSelected>>", change_all_slots)

    card_select_frame=ttk.LabelFrame(slot_page,text="选卡配置",bootstyle=DARK)
    card_select_frame.place(x=0,y=150,relx=1,anchor=NE)
    def changeSlotsConfiguration():
        if(slots_configuration_mode.get()==True):
            slots_frame.configure(text="配置模式",bootstyle=DARK)
        else:
            slots_frame.configure(text="监视模式",bootstyle=SUCCESS)
    slots_configuration_change=ttk.Checkbutton(card_select_frame,text="配置模式",variable=slots_configuration_mode,bootstyle="dark-round-toggle",command=lambda:changeSlotsConfiguration())
    slots_configuration_change.pack()
    ToolTip(slots_configuration_change,text="开启后左侧卡槽进入配置模式，可以配置选卡方案",bootstyle=(INFO,INVERSE))
    # card_select_combobox = ttk.Combobox(card_select_frame, width=12, values=data.plantsType, state='readonly', bootstyle='secondary')
    # card_select_combobox.pack()
    # ttk.Button(card_select_frame,text="选卡",command=lambda:pvz.selectCard(card_select_combobox.current())).pack()
    # ttk.Button(card_select_frame,text="退卡",command=lambda:pvz.deselectCard(card_select_combobox.current())).pack()
    
    # 定义一个函数来更新slot的属性
    def get_slot_attribute():
        for index, slot in enumerate(slot_list):
            try:
                slot_type_comboboxes[index].current(slot.type)
                if (slot_page.focus_get() != slot_cooldown_entrys[index] and slot_page.focus_get() !=slot_cd_progressBars[index]):
                    slot_cooldown_values[index].set(slot.cooldown)
                    slot_cd_progressBars[index].configure(maximum=slot_cooldown_values[index].get())
                if (slot_page.focus_get() != slot_elapsed_entrys[index] and slot_page.focus_get() !=slot_cd_progressBars[index]):
                    slot_elapsed_values[index].set(slot.elapsed)
                slot_isVisible_flags[index].set(not slot.isViible)
                # slot_canUse_flags[index].set(slot.canUse)
            except:
                pass
        try:
            slots_num_value.set(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.PVZ_memory.read_int(data.baseAddress)+0x768)+0x144)+0x24))
        except:
            pass



    def refreshData():
        if(page_tab.index('current')==0):
            if(pvz.getMap()!=False):  
                try:      
                    if(main_window.focus_get()!=sun_value_entry):
                        sun_value.set(pvz.getSun())
                except:
                    pass
        if(page_tab.index('current')==1):
            if(pvz.getMap()!=False):       
                refresh_zombie_list()
                get_zombie_attribute()
        if(page_tab.index('current')==2):
            if(pvz.getMap()!=False):       
                refresh_plant_list()
                get_plant_attribute()
        if(page_tab.index('current')==3):
            if(pvz.getMap()!=False):       
                refresh_item_list()
                get_item_attribute()
        if(page_tab.index('current')==4):  
            if(slots_configuration_mode.get()==False):
                refresh_slot_list()
                get_slot_attribute()
        main_window.after(100,refreshData)
           



    
    support_button=ttk.Button(main_window,text="觉得好用？支持开发者",padding=0,bootstyle=(PRIMARY,LINK),cursor="hand2",command=lambda:support())
    support_button.place(x=0,y=0,relx=1,anchor=NE)
    main_window.after(100,refreshData)

    main_window.protocol("WM_DELETE_WINDOW", lambda: exit_editor(config_file_path, main_window))
    main_window.mainloop()

if __name__ == '__main__':
    mainWindow()