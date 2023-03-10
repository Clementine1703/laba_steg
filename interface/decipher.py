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
        buttons.create_button(self, 'Загрузить ПСП', self.get_psp)
        buttons.create_button(self, 'Достать сообщение', self.get_message)




        self.mainloop()

    @staticmethod
    def upload_start_container():
        #окно выбора файлов
        settings.filename_start_container = filedialog.askopenfilename()
        settings.start_container_left_channel_data = calculate.get_left_channel_wav_data(settings.filename_start_container)

        with wave.open(settings.filename_start_container, 'rb') as wave_read:
            settings.start_container_attachment_depth = len(calculate.b2a_bin(wave_read.readframes(1)))

    @staticmethod
    def upload_result_container():
        #окно выбора файлов
        settings.filename_result_container = filedialog.askopenfilename()
        settings.result_container_left_channel_data = calculate.get_left_channel_wav_data(settings.filename_result_container)
        
        with wave.open(settings.filename_result_container, 'rb') as wave_read:
            settings.result_container_attachment_depth = len(calculate.b2a_bin(wave_read.readframes(1)))

    @staticmethod
    def get_psp():
        filename_psp = filedialog.askopenfilename()
        with open(filename_psp, 'r') as file:
            psp_str = file.read()
            settings.psp_list = [int(i) for i in psp_str[1:-1].split(',') ]
            print(settings.psp_list)

    @staticmethod
    def get_message():
        result = calculate.get_message(settings.start_container_left_channel_data, settings.result_container_left_channel_data, settings.psp_list, settings.result_container_attachment_depth)
        calculate.call_message(result)
        name = settings.filename_start_container = filedialog.askopenfilename()
        with open(name, 'wb') as file:
            file.write(calculate.bin_to_b2a(result))





    

