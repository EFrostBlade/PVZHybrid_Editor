from pymem import Pymem
import win32gui
import win32process
import psutil
import re
import time
import os
import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.tooltip import ToolTip
import PVZ_data as data
import PVZ_Hybrid as pvz

data.update_PVZ_memory(1)

def resource_path(relative_path):
    """ 获取资源的绝对路径，适用于开发环境和PyInstaller环境 """
    try:
        # PyInstaller创建的临时文件夹的路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def chooseGame():
    def openPVZ_memory(process1):
        try:
            data.update_PVZ_memory(Pymem(int(re.search(r'(\d+)',process1).group(1))))
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
    choose_process_window.iconphoto(False,ttk.PhotoImage(file=resource_path(r"src\icon\choose.png")))
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

def mainWindow():
    main_window=ttk.Window()
    main_window.title("杂交版多功能修改器")
    main_window.geometry("500x500")
    main_window.iconphoto(False,ttk.PhotoImage(file=resource_path(r"src\icon\editor.png")))
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
            process_label["text"]="找到进程："+str(data.PVZ_memory.process_id)+str(psutil.Process(data.PVZ_memory.process_id).name())
            process_label.config(bootstyle=DANGER)
        except:
            updateGame()
    tryFindGame()
    choose_process_button=ttk.Button(process_frame,text="选择游戏",padding=0,bootstyle=(PRIMARY,LINK),command=lambda:updateGame())
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
    ttk.Label(resource_modify_frame,text="阳光：",bootstyle=WARNING,font=("宋体",14)).grid(row=0,column=0,sticky=E)
    sun=ttk.IntVar(main_window)
    sun_value=ttk.Entry(resource_modify_frame,width=8,bootstyle=WARNING,textvariable=sun)
    sun_value.grid(row=0,column=1)
    ttk.Button(resource_modify_frame,text="修改",bootstyle=(WARNING,OUTLINE),command=lambda:pvz.setSun(sun.get())).grid(row=0,column=2,padx=(5,0))
    ttk.Label(resource_modify_frame,text="增加阳光：",bootstyle=WARNING,font=("宋体",14)).grid(row=1,column=0,sticky=E)
    add_sun_value=ttk.Entry(resource_modify_frame,width=8,bootstyle=WARNING)
    add_sun_value.grid(row=1,column=1)
    ttk.Button(resource_modify_frame,text="增加",bootstyle=(WARNING,OUTLINE),command=lambda:pvz.addSun(int(add_sun_value.get()))).grid(row=1,column=2,padx=(5,0))
    
    quick_start_frame=ttk.LabelFrame(common_page,text="快速使用",bootstyle=SUCCESS)
    quick_start_frame.place(x=0,y=0,relx=1,rely=0,anchor=NE)
    over_plant_status=ttk.IntVar(quick_start_frame)
    over_plant_check=ttk.Checkbutton(quick_start_frame,text="自由放置",variable=over_plant_status,bootstyle="success-round-toggle",command=lambda:pvz.overPlant(over_plant_status.get()))
    over_plant_check.grid(row=0,column=0,sticky=W)
    ToolTip(over_plant_check,text="植物可以重叠放置并无视地形",bootstyle=(INFO,INVERSE))
    free_plant_status=ttk.IntVar(quick_start_frame)
    free_plant_check=ttk.Checkbutton(quick_start_frame,text="免费种植",variable=free_plant_status,bootstyle="success-round-toggle",command=lambda:pvz.ignoreSun(free_plant_status.get()))
    free_plant_check.grid(row=1,column=0,sticky=W)
    ToolTip(free_plant_check,text="植物可以不消耗阳光种植",bootstyle=(INFO,INVERSE))
    cancel_cd_status=ttk.IntVar(quick_start_frame)
    cancel_cd_check=ttk.Checkbutton(quick_start_frame,text="取消冷却",variable=cancel_cd_status,bootstyle="success-round-toggle",command=lambda:pvz.cancelCd(cancel_cd_status.get()))
    cancel_cd_check.grid(row=2,column=0,sticky=W)
    ToolTip(cancel_cd_check,text="植物种植后不进入冷却时间",bootstyle=(INFO,INVERSE))
    auto_colect_status=ttk.IntVar(quick_start_frame)
    auto_colect_check=ttk.Checkbutton(quick_start_frame,text="自动收集",variable=auto_colect_status,bootstyle="success-round-toggle",command=lambda:pvz.autoCollect(auto_colect_status.get()))
    auto_colect_check.grid(row=3,column=0,sticky=W)
    ToolTip(auto_colect_check,text="自动收集自然掉落的阳光和僵尸掉落的金币",bootstyle=(INFO,INVERSE))
    column_like_status=ttk.IntVar(quick_start_frame)
    column_like_check=ttk.Checkbutton(quick_start_frame,text="柱子模式",variable=column_like_status,bootstyle="success-round-toggle",command=lambda:pvz.column(column_like_status.get()))
    column_like_check.grid(row=4,column=0,sticky=W)
    ToolTip(column_like_check,text="种植一个植物后在同一列的其他行种植相同的植物(可与自由放置配合使用)",bootstyle=(INFO,INVERSE))
    shovel_pro_status=ttk.IntVar(quick_start_frame)
    shovel_pro_check=ttk.Checkbutton(quick_start_frame,text="超级铲子",variable=shovel_pro_status,bootstyle="success-round-toggle",command=lambda:pvz.shovelpro(shovel_pro_status.get()))
    shovel_pro_check.grid(row=5,column=0,sticky=W)
    ToolTip(shovel_pro_check,text="铲掉植物返还其阳光消耗并触发亡语效果",bootstyle=(INFO,INVERSE))
    never_fail_status=ttk.IntVar(quick_start_frame)
    never_fail_check=ttk.Checkbutton(quick_start_frame,text="永不失败",variable=never_fail_status,bootstyle="success-round-toggle",command=lambda:pvz.ignoreZombies(never_fail_status.get()))
    never_fail_check.grid(row=6,column=0,sticky=W)
    ToolTip(never_fail_check,text="僵尸进家不判定游戏失败",bootstyle=(INFO,INVERSE))
    win_button=ttk.Button(quick_start_frame,text="当前关卡胜利",padding=0,bootstyle=(SUCCESS,OUTLINE),command=lambda:pvz.win())
    win_button.grid(row=7,column=0,sticky=W,pady=(2,2))
    ToolTip(win_button,text="当前的游戏关卡直接进行胜利结算",bootstyle=(INFO,INVERSE))
    kill_all_button=ttk.Button(quick_start_frame,text="秒杀所有僵尸",padding=0,bootstyle=(SUCCESS,OUTLINE),command=lambda:pvz.killAllZombies())
    kill_all_button.grid(row=8,column=0,sticky=W,pady=(2,2))
    ToolTip(kill_all_button,text="秒杀当前场上的所有僵尸",bootstyle=(INFO,INVERSE))
    unlock_button=ttk.Button(quick_start_frame,text="解锁全部植物",padding=0,bootstyle=(SUCCESS,OUTLINE),command=lambda:pvz.unlock())
    unlock_button.grid(row=9,column=0,sticky=W,pady=(2,2))
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
    
    
    def refreshData():
        if(page_tab.index('current')==0):
            if(pvz.getMap()!=False):        
                if(main_window.focus_get()!=sun_value):
                    sun.set(pvz.getSun())

        main_window.after(500,refreshData)
        
    main_window.after(500,refreshData)
    main_window.mainloop()

if __name__ == '__main__':
    mainWindow()