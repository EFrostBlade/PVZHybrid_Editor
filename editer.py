from pymem import Pymem
import win32gui
import win32process
import psutil
import re
import time
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import *

PVZ_memory=1

def chooseGame():
    global PVZ_memory
    def openPVZ_memory(process1):
        global PVZ_memory
        try:
            PVZ_memory=Pymem(int(re.search(r'(\d+)',process1).group(1)))
        except:
            Messagebox.show_error("没有足够的权限，请确保游戏未以管理员身份运行",title="注入进程失败",parent=choose_process_window)
            choose_process_window.quit()
            choose_process_window.destroy()
        else:   
            choose_process_window.quit()
            choose_process_window.destroy()   

    def tryFindGame():
        global PVZ_memory
        try:
            hwnd=win32gui.FindWindow("MainWindow",None)
            pid=win32process.GetWindowThreadProcessId(hwnd)
            PVZ_memory= Pymem(pid[1])
            choose_process_window.quit()
            choose_process_window.destroy()
        except:
            Messagebox.show_error("请确保游戏已开启且未以管理员身份运行\n如果仍无法注入游戏可以尝试使用管理员身份开启本修改器",title="未找到游戏",parent=choose_process_window)
            return

    # def retry():
    #     global PVZ_memory
    #     choose_process_window.quit()
    #     choose_process_window.destroy()
    #     PVZ_memory=1
    #     # choosegame()
    #     return PVZ_memory

    def close():
        global PVZ_memory
        choose_process_window.quit()
        choose_process_window.destroy()
        PVZ_memory=0
        return PVZ_memory
     
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
    main_window.iconphoto(False,ttk.PhotoImage(file=r"src\icon\editer.png"))
    process_frame=ttk.Frame(main_window)
    process_frame.place(x=0,y=0,relx=1,rely=1,anchor=SE)
    process_label=ttk.Label(process_frame,text="", font=("黑体", 12))
    process_label.pack(side=LEFT)
    def updateGame():
        chooseGame()
        if(type(PVZ_memory)!= Pymem):
            process_label["text"]="未找到游戏"
            process_label.config(bootstyle=DANGER)
        else:
            process_label["text"]="找到进程："+str(PVZ_memory.process_id)+str(psutil.Process(PVZ_memory.process_id).name())
            process_label.config(bootstyle=DANGER)
    def tryFindGame():
        global PVZ_memory
        try:
            hwnd=win32gui.FindWindow("MainWindow",None)
            pid=win32process.GetWindowThreadProcessId(hwnd)
            PVZ_memory= Pymem(pid[1])
            process_label["text"]="找到进程："+str(PVZ_memory.process_id)+str(psutil.Process(PVZ_memory.process_id).name())
            process_label.config(bootstyle=DANGER)
        except:
            updateGame()
    tryFindGame()
    choose_process_button=ttk.Button(process_frame,text="选择游戏",bootstyle=PRIMARY,command=lambda:updateGame())
    choose_process_button.pack(side=LEFT)
    main_window.mainloop()

if __name__ == '__main__':
    mainWindow()