import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb


def create_app():
    root = tk.Tk()
    style = tb.Style(theme="darkly")

    # 创建一个醒目的按钮
    button = tb.Button(root, text="重要操作", bootstyle="danger", width=20)
    button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_app()
