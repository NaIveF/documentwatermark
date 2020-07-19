import hashlib
import time
import docx2txt


def string_to_md5(string):
    md5_val = hashlib.md5(string.encode('utf8')).hexdigest()

    return md5_val


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


my_text = docx2txt.process(r'test.docx')
print(my_text)
print(type(my_text))
list = my_text.split('\n')
print(list)
# fin = open('text.txt','r',encoding='utf-8')
# data = fin.readlines()
for line in list:
    start1 = time.time()
    md5 = string_to_md5(line)
    print(md5)
    print(type(md5))
    print(len(md5))
    crc = calc_crc(md5)
    print(crc)
