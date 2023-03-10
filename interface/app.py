import tkinter as tk
from .encrypt import Encrypt
from .decipher import Decipher
from utils import buttons

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry('300x300')
        self.title('Main')
        buttons.create_button(
            window=self,
            text='Создание стегосистемы',
            command=self.open_encrypt_window
        )

        buttons.create_button(
            window=self,
            text='Расшифровка стегосистемы',
            command=self.open_decipher_window
        )

        self.mainloop()

    @staticmethod
    def open_encrypt_window():
        Encrypt()


    @staticmethod
    def open_decipher_window():
        Decipher()


    