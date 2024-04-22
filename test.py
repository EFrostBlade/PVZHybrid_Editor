import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def window2():
    window2 = ttk.Window(themename='superhero')  # 应用主题
    b1 = ttk.Button(window2, text="Button 1", bootstyle=SUCCESS)
    b1.pack(side=LEFT, padx=5, pady=10)
    window2.mainloop()

def window():
    root = ttk.Window(themename='superhero')  # 应用主题

    b1 = ttk.Button(root, text="Button 1", bootstyle=SUCCESS)
    b1.pack(side=LEFT, padx=5, pady=10)

    root.mainloop()

window()
window2()
