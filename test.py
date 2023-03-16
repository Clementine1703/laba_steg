import tkinter
from tkinter.filedialog import asksaveasfile

class Window(tkinter.Tk):
    def __init__(self):
        super().__init__()
        
        btn = tkinter.Button(self , text="выгрузить файл", command=self.command)
        btn.pack()

    @staticmethod
    def command():
        f = asksaveasfile(mode='w', defaultextension=".txt")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        text2save = str('aboba') # starts from `1.0`, not `0.0`
        f.write(text2save)
        f.close() # `()` was missing.


if __name__ == '__main__':
    app = Window()
    app.mainloop()