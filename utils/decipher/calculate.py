from utils.decipher import settings
import math
import wave
import tkinter as tk
import tkinter.messagebox as mb

def get_left_channel_wav_data(wav_filename):
    try:
        with wave.open(wav_filename, 'rb') as wav_file:
            data = wav_file.readframes(wav_file.getnframes())
            data = b2a_bin(data)

            print(f'\nкол-во бит wav файла: {len(data)}')

            return data
    except wave.Error:
        raise wave.Error
    
def b2a_bin(data):
    return bin(int.from_bytes(data, 'big'))[2:].zfill(8*len(data)) if data else ''

def get_message(start_container_data, result_container_data, psp_list, attachment_depth):
    depth = attachment_depth
    result = ''

    print(len(result_container_data))
    for bit_index in range(0, len(result_container_data), depth*len(psp_list)):


        # result_frame = result_container_data[bit_index:bit_index+depth]
        # start_frame = start_container_data[bit_index:bit_index+depth]

        # raznost = int(result_frame, 2) - int(start_frame, 2)





        result_n_segment_data = result_container_data[bit_index:bit_index+depth*len(psp_list)]
        start_n_segment_data = start_container_data[bit_index:bit_index+depth*len(psp_list)]

        result_plus_1_counter = 0
        result_plus_0_counter = 0


        for n_segment_bit_index in range(len(psp_list)):
            n_segment_res_frame = result_n_segment_data[n_segment_bit_index*depth:n_segment_bit_index*depth+depth]
            n_segment_start_frame = start_n_segment_data[n_segment_bit_index*depth:n_segment_bit_index*depth+depth]

            if (n_segment_res_frame == '' or n_segment_start_frame == ''):
                if (result_plus_1_counter >= result_plus_0_counter):
                    result += '1'
                else:
                    result += '0'
                break
            

            raznost = int(n_segment_res_frame, 2) - int(n_segment_start_frame, 2)
            if psp_list[n_segment_bit_index] == 1:
                if raznost == -1:
                    result_plus_1_counter += 1
                    continue
                elif raznost == 1:
                    result_plus_0_counter += 1
                    continue
            else:
                if raznost == -1:
                    result_plus_0_counter += 1
                    continue
                elif raznost == 1:
                    result_plus_1_counter += 1
                    continue

        
        if (result_plus_1_counter >= result_plus_0_counter):
            result += '1'
        else:
            result += '0'
        


        # if psp_list[bit_index] == 1:
        #     if raznost == -1:
        #         result += '1'
        #         continue
        #     elif raznost == 1:
        #         result += '0'
        #         continue
        # else:
        #     if raznost == -1:
        #         result += '0'
        #         continue
        #     elif raznost == 1:
        #         result += '1'
        #         continue

    return result



    

def call_message(text):
    window = tk.Tk()
    window.title('сообщение')
    window.geometry('300x300')
    message = tk.Label(window, text=text)
    message.pack(padx=20, pady=20)

def show_info(message):
    mb.showinfo('Информация', message)

def bin_to_b2a(data):
    result = bytearray()

    for byte_index in range(0, len(data) - 8, 8):
        moment_result = int(data[byte_index:byte_index+8], 2)
        result.append(moment_result)

    return (result)