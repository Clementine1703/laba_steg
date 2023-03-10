import wave
import tkinter
from utils.encrypt import settings
import random

#перевод в двоичный формат из b2a
def b2a_bin(data):
    return bin(int.from_bytes(data, 'big'))[2:].zfill(8*len(data)) if data else ''

#возвращает содержимое файла с сообщением
def get_message_content(filename):
    with open(filename, 'rb') as file:
        content = file.read()
        content = b2a_bin(content)
        return content

#возвращает объект wave файла
def get_wave_file_object(filename):
    with wave.open(filename, 'rb') as file:
        return file


#возвращает данные левого канала wave-файла
def get_left_channel_wav_data(wav_filename):
    with wave.open(wav_filename, 'rb') as wav_file:
        data = wav_file.readframes(wav_file.getnframes())
        data = b2a_bin(data)

        #ТЕСТТТТТ:

        print(f'\nкол-во бит wav файла: {len(data)}')

        if wav_file.getnchannels() > 1:
            data = data[0::2]
            print(f'\nкол-во бит левого канала wav файла: {len(data)}')
        return data


#вычисляет глубину вложения (кол-во битов в 1 кадре)
def calculate_left_channel_attachment_depth(wav_filename):
    with wave.open(wav_filename, 'rb') as wav_file:
        frame = wav_file.readframes(1)
        frame = b2a_bin(frame)

        print(f'1 кадр сообщения: {wav_file.readframes(50)}')
        attachment_depth = len(frame)
        print(f'Глубина вложения: {attachment_depth/2}\n')
        if wav_file.getnchannels() > 1:
            return attachment_depth/2
        return attachment_depth


#отображает сообщение с содержимым text
def call_message(text):
    window = tkinter.Tk()
    window.title('сообщение')
    window.geometry('300x300')
    message = tkinter.Label(window, text=text)
    message.pack(padx=20, pady=20)

#генерация списка с n псевдослучайных 1 и -1
def generate_psp(size_of_n_segment):
    psp_list = []
    for i in range(size_of_n_segment):
        if (random.getrandbits(1)):
            psp_list.append(1)
        else:
            psp_list.append(-1)
    print(psp_list)
    print(type(settings.left_channel_wav_data))
    return psp_list

def calculate_result_file():
    result = ''
    bytesdata = bytearray()
    # for bit_index in range(len(settings.message)):
    for bit_index in range(len(settings.message)):
        #начало отсчета под номером bit_index
        from_m = int(bit_index * settings.attachment_depth * settings.size_of_n_segment)
        #конец отсчета под номером bit_index
        to_m = int((bit_index+1) * settings.attachment_depth * settings.size_of_n_segment)
        #кусок n сегмента под номером bit_index
        part_of_left_channel_data = settings.left_channel_wav_data[from_m:to_m]


        for psp_index in range(len(settings.psp_list)):
            #начало кадра под номером psp_index
            from_m = int(psp_index*settings.attachment_depth)
            #конец кадра под номером psp_index
            to_m = int((psp_index+1)*settings.attachment_depth)
            #psp_index-тый кадр
            frame = part_of_left_channel_data[from_m:to_m]
            # print(f'НЕизмененный {psp_index} кадр: {frame}\n')
            int_frame = int(frame, 2)

            if(settings.message[bit_index] == 1):
                #обработка опасных граничных случаeв
                if (int(frame, 2) - settings.psp_list[psp_index] < 0) or (int(frame, 2) - settings.psp_list[psp_index] > 65535):
                    data = frame
                else:
                    data = bin(int_frame - settings.psp_list[psp_index])[2:].zfill(int(settings.attachment_depth))
                result += data
                # print(f'измененный {psp_index} кадр: {data}\n')
                bytesdata.append(int(data[:8], 2))
                bytesdata.append(int(data[8:], 2))
            else:
                #обработка опасных граничных случаeв
                if (int(frame, 2) + settings.psp_list[psp_index] < 0) or (int(frame, 2) + settings.psp_list[psp_index] > 65535):
                    data = frame
                else:
                    data = bin(int_frame + settings.psp_list[psp_index])[2:].zfill(int(settings.attachment_depth))
                result += data  
                # print(f'измененный {psp_index} кадр: {data}\n')
                bytesdata.append(int(data[:8], 2))
                bytesdata.append(int(data[8:], 2))
                
    
    #данные левого канала в 16-ричном формате
    settings.bytesresult = bytesdata
    #возвращаем данные левого канала с вложенныи сообщением
    return result+settings.left_channel_wav_data[len(result):]













