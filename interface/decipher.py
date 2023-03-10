import tkinter as tk
from tkinter import filedialog
from utils import buttons
from utils.decipher import calculate, settings
import wave
from utils.encrypt.settings import psp_list

class Decipher(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry('300x300')
        self.title('Расшифровка стегосистемы')
        
        buttons.create_button(self, 'Загрузить исходный контейнер', self.upload_start_container)
        buttons.create_button(self, 'Загрузить результирующий контейнер', self.upload_result_container)
        buttons.create_button(self, 'Достать сообщение', self.get_message)




        self.mainloop()

    @staticmethod
    def upload_start_container():
        #окно выбора файлов
        settings.filename_start_container = filedialog.askopenfilename()
        settings.start_container_left_channel_data = calculate.get_left_channel_wav_data(settings.filename_start_container)

    @staticmethod
    def upload_result_container():
        #окно выбора файлов
        settings.filename_result_container = filedialog.askopenfilename()
        settings.result_container_left_channel_data = calculate.get_left_channel_wav_data(settings.filename_result_container)

    @staticmethod
    def get_message():
        result = calculate.get_message(settings.start_container_left_channel_data, settings.result_container_left_channel_data, [-1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, 1, 1, -1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, -1, -1, 1, -1])
        calculate.call_message(result)
        name = settings.filename_start_container = filedialog.askopenfilename()
        with open(name, 'wb') as file:
            file.write(calculate.bin_to_b2a(result))





    

