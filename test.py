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
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.tooltip import ToolTip
import PVZ_data as data
import PVZ_Hybrid as pvz
import PVZ_asm  


hwnd=win32gui.FindWindow("MainWindow",None)
pid=win32process.GetWindowThreadProcessId(hwnd)
data.update_PVZ_memory( Pymem(pid[1]))
data.update_PVZ_pid(pid[1])
def window():
    main_window=ttk.Window()
    main_window.title("杂交版多功能修改器")
    main_window.geometry("500x500")
    page_tab=ttk.Notebook(main_window)
    page_tab.pack(padx=10, pady=(5,30), fill=BOTH,expand=True)
    slot_page=ttk.Frame(page_tab)
    slot_page.pack()
    page_tab.add(slot_page,text="卡槽修改")         
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

    refresh_slot_list()
    # ttk.Label(slot_page,text="卡槽1").grid(row=0,column=0,sticky=W)
    # ttk.Label(slot_page,text="植物:").grid(row=0,column=1,sticky=W)
    # slot1_type_combobox=ttk.Combobox(slot_page,width=12,values=data.plantsType,state=READONLY,bootstyle=SECONDARY)
    # slot1_type_combobox.grid(row=0,column=2,sticky=W)
    # def setSlot1Type(event):
    #     slot_list[0].setType(slot1_type_combobox.current())
    #     slot_page.focus_set()
    # slot1_type_combobox.bind("<<ComboboxSelected>>",setSlot1Type)
    # slot1_elapsed_label=ttk.Label(slot_page,text="已冷却:")
    # slot1_elapsed_label.grid(row=0,column=3)
    # slot1_elapsed_value=ttk.IntVar(slot_page)
    # slot1_elapsed_entry=ttk.Entry(slot_page,textvariable=slot1_elapsed_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    # slot1_elapsed_entry.grid(row=0,column=4,ipady=0)
    # def setSlot1Elapsed(event):
    #     slot_list[0].setElapsed(slot1_elapsed_value.get())
    #     slot_page.focus_set()
    # slot1_elapsed_entry.bind("<Return>",setSlot1Elapsed)
    # slot1_cooldowne_label=ttk.Label(slot_page,text="总冷却:")
    # slot1_cooldowne_label.grid(row=0,column=5,padx=(2,0))
    # slot1_cooldowne_value=ttk.IntVar(slot_page)
    # slot1_cooldowne_entry=ttk.Entry(slot_page,textvariable=slot1_cooldowne_value,width=5,font=("黑体",8),bootstyle=SECONDARY)
    # slot1_cooldowne_entry.grid(row=0,column=6,ipady=0)
    # def setSlot1Cooldowne(event):
    #     slot_list[0].setCooldowne(slot1_cooldowne_value.get())
    #     slot_page.focus_set()
    # slot1_cooldowne_entry.bind("<Return>",setSlot1Cooldowne)

    # # 定义一个函数来创建slot的UI组件
    # def create_slot_ui(slot_number, slot_page, slot_list, data):
    #     ttk.Label(slot_page, text=f"卡槽{slot_number}").grid(row=slot_number-1, column=0, sticky='W')
    #     ttk.Label(slot_page, text="植物:").grid(row=slot_number-1, column=1, sticky='W')

    #     slot_type_combobox = ttk.Combobox(slot_page, width=12, values=data.plantsType, state='readonly', bootstyle='secondary')
    #     slot_type_combobox.grid(row=slot_number-1, column=2, sticky='W')

    #     def setSlotType(event, slot_number=slot_number):
    #         slot_list[slot_number-1].setType(slot_type_combobox.current())
    #         slot_page.focus_set()
    #     slot_type_combobox.bind("<<ComboboxSelected>>", setSlotType)

    #     slot_elapsed_label = ttk.Label(slot_page, text="已冷却:")
    #     slot_elapsed_label.grid(row=slot_number-1, column=3)

    #     slot_elapsed_value = ttk.IntVar(slot_page)
    #     slot_elapsed_entry = ttk.Entry(slot_page, textvariable=slot_elapsed_value, width=5, font=("黑体", 8), bootstyle='secondary')
    #     slot_elapsed_entry.grid(row=slot_number-1, column=4, ipady=0)

    #     def setSlotElapsed(event, slot_number=slot_number):
    #         slot_list[slot_number-1].setElapsed(slot_elapsed_value.get())
    #         slot_page.focus_set()
    #     slot_elapsed_entry.bind("<Return>", setSlotElapsed)

    #     slot_cooldown_label = ttk.Label(slot_page, text="总冷却:")
    #     slot_cooldown_label.grid(row=slot_number-1, column=5, padx=(2,0))

    #     slot_cooldown_value = ttk.IntVar(slot_page)
    #     slot_cooldown_entry = ttk.Entry(slot_page, textvariable=slot_cooldown_value, width=5, font=("黑体", 8), bootstyle='secondary')
    #     slot_cooldown_entry.grid(row=slot_number-1, column=6, ipady=0)

    #     def setSlotCooldown(event, slot_number=slot_number):
    #         slot_list[slot_number-1].setCooldown(slot_cooldown_value.get())
    #         slot_page.focus_set()
    #     slot_cooldown_entry.bind("<Return>", setSlotCooldown)

    # # 为slot2至slot14创建UI组件
    # for slot_number in range(2, 15):
    #     create_slot_ui(slot_number, slot_page, slot_list, data)



    # def get_slot_attribute():
    #     try:
    #         slot1_type_combobox.current(slot_list[0].type)
    #         if(slot_page.focus_get()!=slot1_cooldowne_entry):
    #             slot1_cooldowne_value.set(slot_list[0].cooldown)
    #         if(slot_page.focus_get()!=slot1_elapsed_entry):
    #             slot1_elapsed_value.set(slot_list[0].elapsed)
            
    #     except:
    #         pass
           
    def create_slot_ui(slot_number, slot_page, slot_list, data, slot_progressbars, slot_elapsed_values):
        ttk.Label(slot_page, text=f"卡槽{slot_number}").grid(row=slot_number-1, column=0, sticky=W)
        ttk.Label(slot_page, text="植物:").grid(row=slot_number-1, column=1, sticky=W)

        slot_type_combobox = ttk.Combobox(slot_page, width=12, values=data.plantsType, state='readonly', bootstyle='secondary')
        slot_type_combobox.grid(row=slot_number-1, column=2, sticky=W)

        def set_slot_type(event, slot_number=slot_number):
            slot_list[slot_number-1].setType(slot_type_combobox.current())
            slot_page.focus_set()
        slot_type_combobox.bind("<<ComboboxSelected>>", set_slot_type)

        slot_elapsed_progress = ttk.Progressbar(slot_page, length=100, mode='determinate', maximum=slot_list[slot_number-1].cooldown)
        slot_elapsed_progress.grid(row=slot_number-1, column=3, columnspan=2, sticky=W+E)
        slot_elapsed_progress['value'] = slot_list[slot_number-1].elapsed
        slot_progressbars.append(slot_elapsed_progress)

        slot_elapsed_value = ttk.IntVar(value=slot_list[slot_number-1].elapsed)
        slot_elapsed_values.append(slot_elapsed_value)

        def update_elapsed(event, slot_number=slot_number):
            slot_elapsed_value.set(slot_elapsed_progress.get())
            slot_list[slot_number-1].setElapsed(slot_elapsed_value.get())
            slot_page.focus_set()
        slot_elapsed_progress.bind("<B1-Motion>", update_elapsed)

    # 创建一个函数来更新slot的属性
    def get_slot_attribute(slot_page, slot_list, slot_progressbars, slot_elapsed_values):
        for slot_number in range(1, len(slot_list)+1):
            try:
                slot_progressbars[slot_number-1]['value'] = slot_list[slot_number-1].elapsed
                slot_elapsed_values[slot_number-1].set(slot_list[slot_number-1].elapsed)
            except Exception as e:
                print(f"An error occurred while updating slot {slot_number}: {e}")

    # 假设slot_list是一个对象列表，拥有属性'plantsType', 'setType', 'cooldown', 和 'elapsed'
    # 假设slot_page是slot UI组件的父框架

    # 创建列表来存储每个slot的进度条和elapsed值
    slot_progressbars = []
    slot_elapsed_values = []

    # 为每个slot创建UI组件，并将进度条添加到列表中
    for slot_number in range(1, 15):
        create_slot_ui(slot_number, slot_page, slot_list, data, slot_progressbars, slot_elapsed_values)

        def refreshData():
            if(pvz.getMap()!=False):   
                refresh_slot_list()
                get_slot_attribute()
      
        main_window.after(100,refreshData)

    main_window.after(100,refreshData)
    main_window.mainloop()

window()