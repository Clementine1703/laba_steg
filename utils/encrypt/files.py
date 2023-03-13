import wave
import tkinter
import tkinter.messagebox as mb
from utils.encrypt import settings
import math
import random

# перевод в двоичный формат из b2a


def b2a_bin(data):
    return bin(int.from_bytes(data, 'big'))[2:].zfill(8*len(data)) if data else ''

# возвращает содержимое файла с сообщением


def get_message_content(filename):
    if filename.endswith('.txt'):
        with open(filename, 'rb') as file:
            content = file.read() + b'\x8a' #добавляем любой символ в конец, т.к. при передаче последний символ теряется
            content = b2a_bin(content)
            return content
    else:
        raise TypeError
        return 0

# возвращает объект wave файла


def get_wave_file_object(filename):
    try:
        with wave.open(filename, 'rb') as file:
            return file
    except wave.Error as e:
        raise e
    return 0


# возвращает данные левого канала wave-файла
def get_left_channel_wav_data(wav_filename):
    with wave.open(wav_filename, 'rb') as wav_file:
        data = wav_file.readframes(wav_file.getnframes())
        data = b2a_bin(data)

        # ТЕСТТТТТ:

        print(f'\nкол-во бит wav файла: {len(data)}')

        # if wav_file.getnchannels() > 1:
        #     data = data[0::2]
        #     print(f'\nкол-во бит левого канала wav файла: {len(data)}')
        return data


# вычисляет глубину вложения (кол-во битов в 1 кадре)
def calculate_left_channel_attachment_depth(wav_filename):
    with wave.open(wav_filename, 'rb') as wav_file:
        frame = wav_file.readframes(1)
        frame = b2a_bin(frame)

        print(f'1 кадр сообщения: {wav_file.readframes(1)}')
        attachment_depth = len(frame)
        print(f'Глубина вложения: {attachment_depth}\n')
        # if wav_file.getnchannels() > 1:
        #     return attachment_depth/2
        return attachment_depth


# отображает сообщение с содержимым text
def call_message(text):
    window = tkinter.Tk()
    window.title('сообщение')
    window.geometry('300x300')
    message = tkinter.Label(window, text=text)
    message.pack(padx=20, pady=20)


def show_info(message):
    mb.showinfo('Информация', message)

def show_error(message):
    mb.showerror('Ошибка', message)





# генерация списка с n псевдослучайных 1 и -1
def generate_psp(size_of_n_segment):
    if size_of_n_segment:
        psp_list = []
        for i in range(size_of_n_segment):
            if (random.getrandbits(1)):
                psp_list.append(1)
            else:
                psp_list.append(-1)
        print(f'первые 10 элементов псевдослучайной последовательности: {psp_list}')
        print(f'длина сгенерированной ПСП: {len(psp_list)}')
        return psp_list
    else:
        raise Exception
        return 0


def calculate_result_file(message, left_channel_wav_data, psp_list, attachment_depth, size_of_n_segment):
    result = ''
    # for bit_index in range(len(message)):
    for bit_index in range(len(message)):
        # начало отсчета под номером bit_index
        from_m = int(bit_index * attachment_depth *
                     size_of_n_segment)
        # конец отсчета под номером bit_index
        to_m = int((bit_index+1) * attachment_depth *
                   size_of_n_segment)
        # кусок n сегмента под номером bit_index
        part_of_left_channel_data = left_channel_wav_data[from_m:to_m]

        for psp_index in range(len(psp_list)):
            # начало кадра под номером psp_index
            from_m = int(psp_index*attachment_depth)
            # конец кадра под номером psp_index
            to_m = int((psp_index+1)*attachment_depth)
            # psp_index-тый кадр
            frame = part_of_left_channel_data[from_m:to_m]
            # print(f'НЕизмененный {psp_index} кадр: {frame}\n')
            int_frame = int(frame, 2)

            # print(message[psp_index])
            if (message[bit_index] == '1'):
                # обработка опасных граничных случаeв
                if (int(frame, 2) - psp_list[psp_index] < 0) or (int(frame, 2) - psp_list[psp_index] > (2**attachment_depth)-1):
                    data = frame
                else:
                    data = bin(
                        int_frame - psp_list[psp_index])[2:].zfill(int(attachment_depth))
                result += data
                # print(f'измененный {psp_index} кадр: {data}\n')
            else:
                # обработка опасных граничных случаeв
                if (int(frame, 2) + psp_list[psp_index] < 0) or (int(frame, 2) + psp_list[psp_index] > (2**attachment_depth)-1):
                    data = frame
                else:
                    data = bin(
                        int_frame + psp_list[psp_index])[2:].zfill(int(attachment_depth))
                result += data
                # print(f'измененный {psp_index} кадр: {data}\n')

    # данные левого канала в 16-ричном формате + остаточные биты, в которые мы ничего не записывали
    bytesresult = bin_to_b2a(result) + bin_to_b2a(data[len(result):])

    # возвращаем данные левого канала с вложенныи сообщением
    return bytesresult


def bin_to_b2a(data):
    result = bytearray()

    for byte_index in range(0, len(data) - 8, 8):
        moment_result = int(data[byte_index:byte_index+8], 2)
        result.append(moment_result)

    return (result)
