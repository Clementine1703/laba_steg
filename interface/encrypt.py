import tkinter as tk
from tkinter import filedialog
from utils.encrypt import files, calculate, settings
from utils import buttons
import wave
from scipy.io.wavfile import read
import matplotlib.pyplot as plt

class Encrypt(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry('500x300')
        self.title('Создание стегосистемы')

        buttons.create_button(self, 'Загрузить сообщение', self.upload_message_file)
        buttons.create_button(self, 'Загрузить покрывающий объект', self.upload_wav_file)
        buttons.create_button(self, 'Расчитать размер N', self.calculate_size_of_n_segment)
        buttons.create_button(self, 'Показать размер N', self.show_size_of_n_segment)
        buttons.create_button(self, 'Сгенерировать ПСП', self.generate_psp)
        buttons.create_button(self, 'Сохранить ПСП (ключ)', self.save_psp)
        buttons.create_button(self, 'Записать результат в файл', self.write_result)
        buttons.create_button(self, 'Визуальное сравнение', self.show_stenogram)





        self.mainloop()

    @staticmethod
    def upload_wav_file():
        #окно выбора файлов
        filename_container = filedialog.askopenfilename()
        settings.wav_filename = filename_container

        #записываем экземпляр wave файла в настройки
        try:
            settings.wav_file = files.get_wave_file_object(filename_container)
        except wave.Error:
            files.show_info('Необходим файл с расширением .WAV')
            return 0

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
        try:
            settings.message = files.get_message_content(filename_message)
        except TypeError:
            files.show_info('Необходим файл с расширением .TXT')
            return 0

        print(f'\nтекстовое сообщение в двоичном формате: {settings.message}\nкол-во бит: {len(settings.message)}')


    @staticmethod
    def calculate_size_of_n_segment():
        if (settings.message != '' and settings.wav_file != ''):
            settings.size_of_n_segment = calculate.get_size_of_n_segment(settings.wav_file, settings.message)
            if settings.size_of_n_segment < 1:
                settings.size_of_n_segment = ''
                files.show_error('Колличество кадров в wav-файле меньше кол-ва бит в текстовом файле, вложение невозможно.')
        else:
            files.show_info('Вы не загрузили все необходимые файлы')

    @staticmethod
    def show_size_of_n_segment():
        if settings.size_of_n_segment:
            files.show_info(f'{settings.size_of_n_segment} кадров (в 1 кадре {settings.attachment_depth} бит)')
        else:
            files.show_info('Размер N еще не расчитан')
            

    @staticmethod
    def generate_psp():
        try:
            settings.psp_list = files.generate_psp(settings.size_of_n_segment)
        except Exception:
            files.show_info('Рассчитайте размер N')


        # settings.psp_list = [1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, -1, 1, 1, -1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1, 1, 1]

    @staticmethod
    def save_psp():
        filename_psp = tk.filedialog.asksaveasfilename(
                                        filetypes=[("txt file", ".txt")],
                                        defaultextension=".txt", initialfile='key')
        with open(filename_psp, 'w') as file:
            file.write(str(settings.psp_list))

    @staticmethod
    def show_stenogram():
        audios = []

        try:
            audio = read(settings.wav_filename)[1]
            audios.append(audio)
        except FileNotFoundError:
            files.show_info('Вы не загрузили покрывающий объект')
            return 0
        except Exception:
            files.show_info('Что-то пошло не так')
            return 0
        
        try:
            audio = read(settings.result_wav_filename)[1]
            audios.append(audio)
        except FileNotFoundError:
            files.show_info('Вы не выгрузили покрывающий объект с вложенным сообщением')
            return 0
        except Exception:
            files.show_info('Что-то пошло не так')
            return 0


        if not settings.message:
            files.show_info('Вы не загрузили вкладываемое сообщение или оно пустое')

        fig = plt.figure()
        fig.subplots_adjust(top=0.8)
        fig.canvas.manager.set_window_title('Визуальное сравнение')
        axes = fig.subplots(3)

        # plot the first 1024 samples
        axes[0].plot(audios[0][0:][:, 0])
        axes[0].set_title("Покрывающий объект")
        axes[0].get_xaxis().set_visible(False)
        axes[0].get_yaxis().set_visible(True)

        message_data = [int(settings.message[i]) for i in range(len(settings.message))]
        message_visualization_size = 500
        if(message_visualization_size > len(message_data)):
            message_visualization_size = len(message_data)
        
        axes[1].plot(message_data[0:500])
        axes[1].set_title(f"Вкладываемое сообщение (первые {message_visualization_size} бит)")
        axes[1].get_xaxis().set_visible(False)
        axes[1].set_ylim(-6,6)

        axes[2].plot(audios[1][0:][:, 0])
        axes[2].set_title("Покрывающий объект с вложенным сообщением")
        axes[2].get_xaxis().set_visible(False)
        axes[2].get_yaxis().set_visible(True)
        

        plt.tight_layout()
        plt.show()


        
    @staticmethod
    def write_result():
        if not settings.size_of_n_segment:
            files.show_info('Вы не расчитали размер N')
            return 0
        if not settings.psp_list:
            files.show_info('Вы не сгенерировали ПСП')
            return 0


        #открываем исхоный контейнер и записываем его параметры, для нового контейнера
        params = []
        try:
            with wave.open(settings.wav_filename, 'rb') as wave_read:
                print(wave_read.readframes(1))
                params = wave_read.getparams()
                params = list(params)
        except FileNotFoundError as e:
            files.show_info('Вы не выбрали покрывающий объект')
            return e


        

        filename_result = tk.filedialog.asksaveasfilename(
                            filetypes=[("wave file", ".wav")],
                            defaultextension=".wav", initialfile='covering_object_with_message')
        settings.result_wav_filename = filename_result
        with wave.open(filename_result, 'wb') as wave_write:
            wave_write.setparams(params)
            result = files.calculate_result_file(
                settings.message,
                settings.left_channel_wav_data,
                settings.psp_list,
                settings.attachment_depth,
                settings.size_of_n_segment
            )

            print(params)
            
            wave_write.writeframes(result)

            


    


