from utils.encrypt import settings
import math

# def get_register_bit_depth(size_of_n_segment):
#     register_bit_depth = math.ceil(math.log(size_of_n_segment+1, 2))
#     settings.register_bit_depth = register_bit_depth
#     return register_bit_depth

#возвращает колличество n-сегментов
def get_size_of_n_segment(wav_file, message):
    number_of_counts = wav_file.getnframes()
    size_of_n_segment =  math.floor(number_of_counts/len(message))
    settings.size_of_n_segment = size_of_n_segment
    return size_of_n_segment