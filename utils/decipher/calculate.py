from utils.decipher import settings
import math
import wave
import tkinter as tk

def get_left_channel_wav_data(wav_filename):
    with wave.open(wav_filename, 'rb') as wav_file:
        data = wav_file.readframes(wav_file.getnframes())
        data = b2a_bin(data)

        #ТЕСТТТТТ:

        print(f'\nкол-во бит wav файла: {len(data)}')

        # if wav_file.getnchannels() > 1:
        #     data = data[0::2]
        #     print(f'\nкол-во бит левого канала wav файла: {len(data)}')
        return data
    
def b2a_bin(data):
    return bin(int.from_bytes(data, 'big'))[2:].zfill(8*len(data)) if data else ''

def get_message(start_container_data, result_container_data, psp_list, attachment_depth):
    depth = attachment_depth
    result = ''

    for bit_index in range(0, len(result_container_data), depth*len(psp_list)):
        result_frame = result_container_data[bit_index:bit_index+depth]
        start_frame = start_container_data[bit_index:bit_index+depth]

        raznost = int(result_frame, 2) - int(start_frame, 2)
        print(raznost)

        if psp_list[0] == 1:
            if raznost == -1:
                result += '1'
                continue
            else:
                result += '0'
                continue
        else:
            if raznost == -1:
                result += '0'
                continue
            else:
                result += '1'
                continue
    
    print(result)
    return result



    

def call_message(text):
    window = tk.Tk()
    window.title('сообщение')
    window.geometry('300x300')
    message = tk.Label(window, text=text)
    message.pack(padx=20, pady=20)

def bin_to_b2a(data):
    result = bytearray()

    for byte_index in range(0, len(data) - 8, 8):
        moment_result = int(data[byte_index:byte_index+8], 2)
        result.append(moment_result)

    return (result)