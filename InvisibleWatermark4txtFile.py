import hashlib


def string_to_md5(string):
    md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
    return md5_val


def binary_replace(binary_str):
    temp = []
    for i in range(0, len(binary_str), 2):
        if binary_str[i:i + 2] == '00':
            temp.append('\u202A')
        elif binary_str[i:i + 2] == '01':
            temp.append('\u202B')
        elif binary_str[i:i + 2] == '11':
            temp.append('\u202C')
        elif binary_str[i:i + 2] == '10':
            temp.append('\u202D')
    return ''.join(temp)


def calc_crc(string):
    data = bytearray.fromhex(string)
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return hex(((crc & 0xff) << 8) + (crc >> 8))


def add_watermark(filename_origin, filename_target):
    fin = open(filename_origin, 'r', encoding='utf-8')  # read file
    fout = open(filename_target, 'w', encoding='utf-8')
    my_text = fin.readlines()
    fin.close()
    result = []
    for paragraph in my_text:
        list = paragraph.split('。')  # split data depend on '。'
        temp = []
        for sentence in list:  # add watermark each line
            print('[*]The string before add watermark: ' + sentence)
            print('[*]The string size before add watermark: ' + str(len(sentence)))
            md5 = string_to_md5(sentence)  # generate md5 string
            crc = calc_crc(md5)  # generate crc string with md5 string
            binary = bin(int(crc, 16))[2:]  # get crc binary string
            for i in range(len(binary), 16):
                binary = '0' + binary
            binary_result = binary_replace(binary)  # replace crc string as invisible unicode
            sentence += binary_result
            print('[+]The string after add watermark: ' + sentence)
            print('[+]The string size after add watermark: ' + str(len(sentence)))
            temp.append(sentence)
        result.append('。'.join(temp))
    fout.write(''.join(result))
    fout.close()


def judge_different(file_target):
    ft = open(file_target, 'r', encoding='utf-8')
    alllines_ft = ft.readlines()
    for paragraph in alllines_ft:
        list = paragraph.split('。')  # split data depend on '。'
        for sentence in list:  # add watermark each line
            if len(sentence) == 1:
                continue
            str_origin = sentence[:-8]
            str_watermark = sentence[-8:]
            md5 = string_to_md5(str_origin)  # generate md5 string
            crc = calc_crc(md5)  # generate crc string with md5 string
            binary = bin(int(crc, 16))[2:]  # get crc binary string
            for i in range(len(binary), 16):
                binary = '0' + binary
            binary_result = binary_replace(binary)  # replace crc string as invisible unicode
            if binary_result != str_watermark:
                print(
                    f'[-]The target file is different from  origin file in: paragraph {alllines_ft.index(paragraph) + 1} sentence {list.index(sentence) + 1}. ' + sentence + '。')
    ft.close()


def delete_invisible_chars(origin_string):
    invisible_chars = ['\u202A', '\u202B', '\u202C', '\u202D']
    for i in invisible_chars:
        origin_string = origin_string.replace(i, '')
    return origin_string


def document_recovery(filename_watermark, filename_recovery):
    fin = open(filename_watermark, 'r', encoding='utf-8')  # read file
    fout = open(filename_recovery, 'w', encoding='utf-8')
    text = fin.readlines()
    fin.close()
    for paragraph in text:
        paragraph = delete_invisible_chars(paragraph)
        fout.write(paragraph)
    fout.close()
    print('[*]Recovery Successfully.')


if __name__ == "__main__":
    print('***************************\nAdd watermark to txt file.\n***************************')
    add_watermark('text.txt', 'result.txt')
    print('***************************\nCheck any change in txt file.\n***************************')
    judge_different('result1.txt')  # some difference from generated file
    print('***************************\nRecovery file with watermark.\n***************************')
    document_recovery('result.txt', 'recovery.txt')
