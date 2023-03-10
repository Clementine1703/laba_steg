import tkinter as tk
from tkinter import filedialog
from utils.encrypt import files, calculate, settings
from utils import buttons
import wave

class Encrypt(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry('300x300')
        self.title('Создание стегосистемы')

        buttons.create_button(self, 'Загрузить водяной знак', self.upload_message_file)
        buttons.create_button(self, 'Загрузить контейнер', self.upload_wav_file)
        buttons.create_button(self, 'Расчитать колличество отсчетов', self.calculate_size_of_n_segment)
        buttons.create_button(self, 'Показать колличество отсчетов', self.show_size_of_n_segment)
        buttons.create_button(self, 'Сгенерировать ПСП', self.generate_psp)
        buttons.create_button(self, 'Сохранить ПСП', self.save_psp)
        buttons.create_button(self, 'Записать результат в файл', self.write_result)






        self.mainloop()

    @staticmethod
    def upload_wav_file():
        #окно выбора файлов
        filename_container = filedialog.askopenfilename()
        settings.wav_filename = filename_container

        #записываем экземпляр wave файла в настройки
        settings.wav_file = files.get_wave_file_object(filename_container)

        #записываем содержимое левого канала wave файла
        settings.left_channel_wav_data = files.get_left_channel_wav_data(filename_container)

        #записываем глубину вложения в настройки
        settings.attachment_depth = files.calculate_left_channel_attachment_depth(filename_container)


        # settings.wav_file = files.get_left_channel_data(b2a_bin(files.get_wave_file_object(filename_container).readframes(1)))


    @staticmethod
    def upload_message_file():
        #окно выбора файлов
        filename_message = filedialog.askopenfilename()
        settings.message_filename = filename_message
        
        #запись сообщения в бинарном виде в настройки
        settings.message = files.get_message_content(filename_message)

        print(f'\nтекстовое сообщение в двоичном формате: {settings.message}\nкол-во бит: {len(settings.message)}')


    @staticmethod
    def calculate_size_of_n_segment():
        if (settings.message != '' and settings.wav_file != ''):
            settings.size_of_n_segment = calculate.get_size_of_n_segment(settings.wav_file, settings.message)
        else:
            files.call_message('вы не загрузили все необходимые файлы!')

    @staticmethod
    def show_size_of_n_segment():
        if settings.size_of_n_segment:
            files.call_message(settings.size_of_n_segment)
        else:
            files.call_message('Колличество сегментов еще не расчитано!')

    @staticmethod
    def generate_psp():
        settings.psp_list = files.generate_psp(settings.size_of_n_segment)

        # settings.psp_list = [1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, -1, 1, 1, -1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1, 1, 1]

    @staticmethod
    def save_psp():
        filename_psp = filedialog.askopenfilename()
        with open(filename_psp, 'w') as file:
            file.write(str(settings.psp_list))

        
    @staticmethod
    def write_result():
        #открываем исхоный контейнер и записываем его параметры, для нового контейнера
        params = []
        with wave.open(settings.wav_filename, 'rb') as wave_read:
            print(wave_read.readframes(1))
            params = wave_read.getparams()
            params = list(params)


        filename_result = filedialog.askopenfilename()
        with wave.open(filename_result, 'wb') as wave_write:
            wave_write.setparams(params)
            result = files.calculate_result_file(
                settings.message,
                settings.left_channel_wav_data,
                settings.psp_list,
                settings.attachment_depth,
                settings.size_of_n_segment
            )
            
            wave_write.writeframes(result)


    


