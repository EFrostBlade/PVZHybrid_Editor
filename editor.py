from pymem import Pymem
import win32gui
import win32process
import psutil
import re
import time
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import *
import PVZ_data as data
import PVZ_Hybrid as pvz

data.update_PVZ_memory(1)


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
    choose_process_window.iconphoto(False,ttk.PhotoImage(file=r"src\icon\choose.png"))
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
    main_window.iconphoto(False,ttk.PhotoImage(file=r"src\icon\editor.png"))
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
    over_plant_check=ttk.Checkbutton(quick_start_frame,text="自由放置(重叠种植)",variable=over_plant_status,bootstyle="success-round-toggle",command=lambda:pvz.overPlant(over_plant_status.get()))
    over_plant_check.grid(row=0,column=0,sticky=W)
    free_plant_status=ttk.IntVar(quick_start_frame)
    free_plant_check=ttk.Checkbutton(quick_start_frame,text="无视阳光(免费种植)",variable=free_plant_status,bootstyle="success-round-toggle",command=lambda:pvz.ignoreSun(free_plant_status.get()))
    free_plant_check.grid(row=1,column=0,sticky=W)
    cancel_cd_status=ttk.IntVar(quick_start_frame)
    cancel_cd_check=ttk.Checkbutton(quick_start_frame,text="取消种植冷却",variable=cancel_cd_status,bootstyle="success-round-toggle",command=lambda:pvz.cancelCd(cancel_cd_status.get()))
    cancel_cd_check.grid(row=2,column=0,sticky=W)
    auto_colect_status=ttk.IntVar(quick_start_frame)
    auto_colect_check=ttk.Checkbutton(quick_start_frame,text="自动收集",variable=auto_colect_status,bootstyle="success-round-toggle",command=lambda:pvz.autoCollect(auto_colect_status.get()))
    auto_colect_check.grid(row=3,column=0,sticky=W)
    column_like_status=ttk.IntVar(quick_start_frame)
    column_like_check=ttk.Checkbutton(quick_start_frame,text="柱子模式(种一个送一排)",variable=column_like_status,bootstyle="success-round-toggle",command=lambda:pvz.column(column_like_status.get()))
    column_like_check.grid(row=4,column=0,sticky=W)
    ttk.Button(quick_start_frame,text="当前关卡直接胜利",padding=0,bootstyle=(SUCCESS,OUTLINE),command=lambda:pvz.win()).grid(row=5,column=0,sticky=W,pady=(5,0))
    ttk.Button(quick_start_frame,text="秒杀所有僵尸 ",padding=0,bootstyle=(SUCCESS,OUTLINE),command=lambda:pvz.killAllZombies()).grid(row=6,column=0,sticky=W,pady=(5,0))
    ttk.Button(quick_start_frame,text="解锁所有植物",padding=0,bootstyle=(SUCCESS,OUTLINE),command=lambda:pvz.unlock()).grid(row=7,column=0,sticky=W,pady=(5,0))
    
    
    
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