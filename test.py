import tkinter as tk
from tkinter import messagebox
import PVZ_data as data
from pymem import Pymem
import win32process
import win32gui
import json
import os

# 假设PVZ_memory是一个已经定义好的与游戏内存交互的类
# 这里只是一个示意，您需要替换为实际的内存读写操作

hwnd = win32gui.FindWindow("MainWindow", None)
pid = win32process.GetWindowThreadProcessId(hwnd)
data.update_PVZ_memory(Pymem(pid[1]))
data.update_PVZ_pid(pid[1])


# 创建Tkinter窗口
root = tk.Tk()
root.title("僵尸权重修改器")
# 存储复选框状态的字典
checkboxes = {}
# 存储与权重绑定的IntVar对象的字典
weight_vars = {}
# 存储僵尸类型对象的字典
zombies = {}


def update_weights():
    for zombie_name in data.zombiesType:
        if checkboxes[zombie_name].get():
            weight_var = weight_vars[zombie_name]
            weight = weight_var.get()
            try:
                weight = int(weight)
                zombies[zombie_name].setWeight(weight)
            except ValueError:
                messagebox.showerror("错误", f"无效的权重值: {weight}")
    messagebox.showinfo("成功", "权重更新成功")


def output_selected():
    save_to_json()  # 保存数据
    selected_ids = [str(idx) for idx, zombie_name in enumerate(
        data.zombiesType) if checkboxes[zombie_name].get()]
    messagebox.showinfo("选中的僵尸ID", ", ".join(selected_ids))


# 创建界面元素
for idx, zombie_name in enumerate(data.zombiesType):
    row = idx // 3
    col = idx % 3
    var = tk.IntVar()
    chk = tk.Checkbutton(root, text=zombie_name, variable=var)
    chk.grid(row=row, column=col*2, sticky='w')
    checkboxes[zombie_name] = var

    zombie = data.zombieType(idx)
    zombies[zombie_name] = zombie
    weight_var = tk.IntVar(value=zombie.weight)
    weight_vars[zombie_name] = weight_var
    entry = tk.Entry(root, textvariable=weight_var)
    entry.grid(row=row, column=col*2+1)

# 程序启动时读取JSON文件
if os.path.exists('zombies_data.json'):
    with open('zombies_data.json', 'r') as json_file:
        saved_data = json.load(json_file)
    for zombie_name in data.zombiesType:
        if zombie_name in saved_data:
            checkboxes[zombie_name].set(saved_data[zombie_name]['selected'])
            weight_vars[zombie_name].set(saved_data[zombie_name]['weight'])


def save_to_json():
    data_to_save = {}
    for zombie_name in data.zombiesType:
        data_to_save[zombie_name] = {
            'selected': checkboxes[zombie_name].get(),
            'weight': weight_vars[zombie_name].get()
        }
    with open('zombies_data.json', 'w') as json_file:
        json.dump(data_to_save, json_file, indent=4)


# 添加按钮
update_btn = tk.Button(root, text="修改权重", command=update_weights)
update_btn.grid(row=(len(data.zombiesType) - 1) //
                3 + 1, column=0, columnspan=3)

output_btn = tk.Button(root, text="输出选中ID", command=output_selected)
output_btn.grid(row=(len(data.zombiesType) - 1) //
                3 + 1, column=3, columnspan=3)

# 运行Tkinter事件循环
root.mainloop()
