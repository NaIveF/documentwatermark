import hashlib
import time
import docx2txt


def string_to_md5(string):
    md5_val = hashlib.md5(string.encode('utf8')).hexdigest()

    return md5_val


def binary_replace(binary_str):
    temp = []
    for i in range(0, len(binary_str), 2):
        if binary_str[i:i + 2] == '00':
            temp.append('\u202A\u202C')
        elif binary_str[i:i + 2] == '01':
            temp.append('\u202B\u202C')
        elif binary_str[i:i + 2] == '11':
            temp.append('\u202D\u202C')
        elif binary_str[i:i + 2] == '10':
            temp.append('\u202E\u202C')
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


if __name__ == "__main__":
    my_text = docx2txt.process(r'test.docx')  # read file
    list = my_text.split('\n')  # split data depend on '\n'
    for line in list:  # add watermark each line
        print('[*]The string after add watermark: ' + line)
        print('[*]The string size after add watermark: ' + str(len(line)))
        md5 = string_to_md5(line)  # generate md5 string
        crc = calc_crc(md5)  # generate crc string with md5 string
        binary = bin(int(crc, 16))[2:]  # get crc binary string
        for i in range(len(binary), 16):
            binary = '0' + binary
        binary_result = binary_replace(binary)  # replace crc string as invisible unicode
        line += binary_result
        print('[+]The string after add watermark: ' + line)
        print('[+]The string size after add watermark: ' + str(len(line)))
