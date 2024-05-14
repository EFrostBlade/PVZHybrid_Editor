import tkinter as tk
from pynput import keyboard
from threading import Thread

class HotkeyApp:
    def __init__(self, root):
        self.root = root
        self.hotkeys = {
            'hotkey1': {keyboard.Key.ctrl, keyboard.KeyCode.from_char('f2')},
            'hotkey2': {keyboard.Key.alt, keyboard.KeyCode.from_char('f3')},
            'hotkey3': {keyboard.Key.ctrl, keyboard.Key.alt, keyboard.KeyCode.from_char('f4')}
        }
        self.listener = None
        self.create_ui()
        self.start_hotkey_listener()

    def create_ui(self):
        self.root.title('快捷键设置')
        for i, hotkey in enumerate(self.hotkeys, 1):
            setattr(self, f'hotkey_text{i}', tk.StringVar(value=self.format_hotkey(self.hotkeys[hotkey])))
            tk.Entry(self.root, textvariable=getattr(self, f'hotkey_text{i}'), state='readonly').grid(row=i, column=0)
            tk.Button(self.root, text=f'修改快捷键{i}', command=lambda hotkey=hotkey: self.change_hotkey(hotkey)).grid(row=i, column=1)

    def format_hotkey(self, hotkey_set):
        return '+'.join(str(key) for key in hotkey_set)

    def start_hotkey_listener(self):
        self.listener = keyboard.GlobalHotKeys({self.format_hotkey(self.hotkeys[hotkey]): self.on_activate for hotkey in self.hotkeys})
        self.listener.start()

    def on_activate(self):
        print(f'按下了快捷键')

    def change_hotkey(self, hotkey):
        new_hotkey_window = tk.Toplevel(self.root)
        new_hotkey_window.title('修改快捷键')

        prompt_label = tk.Label(new_hotkey_window, text='请按下新的快捷键')
        prompt_label.pack()

        new_hotkey_text = tk.StringVar(new_hotkey_window, value='...')
        tk.Entry(new_hotkey_window, textvariable=new_hotkey_text, state='readonly').pack()

        def on_key_release(key):
            if key == keyboard.Key.esc:
                new_hotkey_window.destroy()
                return False
            new_hotkey = {key}
            new_hotkey_text.set(self.format_hotkey(new_hotkey))
            prompt_label.config(text='')
            return False

        def update_hotkey():
            self.hotkeys[hotkey] = new_hotkey
            getattr(self, f'hotkey_text{list(self.hotkeys.keys()).index(hotkey)+1}').set(self.format_hotkey(new_hotkey))
            new_hotkey_window.destroy()
            self.listener.stop()
            self.start_hotkey_listener()

        tk.Button(new_hotkey_window, text='确定', command=update_hotkey).pack()
        tk.Button(new_hotkey_window, text='重新输入', command=lambda: prompt_label.config(text='请按下新的快捷键')).pack()
        tk.Button(new_hotkey_window, text='取消', command=new_hotkey_window.destroy).pack()

        with keyboard.Listener(on_release=on_key_release) as listener:
            listener.join()

if __name__ == '__main__':
    root = tk.Tk()
    app = HotkeyApp(root)
    root.mainloop()
