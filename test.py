import tkinter as tk
from threading import Thread
import queue


class ThreadSafeIntVar:
    def __init__(self, master):
        self.master = master
        self.queue = queue.Queue()
        self.intvar = tk.IntVar(master)

    def get(self):
        self.master.after(0, self._get_from_queue)
        return self.queue.get()

    def set(self, value):
        self.master.after(0, self._set_from_queue, value)

    def _get_from_queue(self):
        self.queue.put(self.intvar.get())

    def _set_from_queue(self, value):
        self.intvar.set(value)


# 使用示例
def worker(ts_intvar):
    # 获取IntVar的值
    current_value = ts_intvar.get()
    print("Current value:", current_value)
    # 更新IntVar的值
    ts_intvar.set(current_value + 10)
    print("Current value:", current_value)


if __name__ == "__main__":
    root = tk.Tk()
    ts_intvar = ThreadSafeIntVar(root)
    ts_intvar.set(100)  # 初始设置一个值

    t = Thread(target=worker, args=(ts_intvar,))
    t.start()

    root.mainloop()
