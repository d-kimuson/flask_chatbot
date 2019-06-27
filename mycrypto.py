from Crypto.Cipher import AES
import random
import string

key = "ZpI6O2g7p8gbqLIf"
mode = AES.MODE_CBC
vector = "WXivShkV5U4TZZtL"
byte_len = 16


def encrypto(passwd):
    for i in range(byte_len-len(passwd)):
        passwd = passwd + " "
    return byte2str(AES.new(key, mode, vector).encrypt(passwd))


def decrypto(ciphertext):
    ciphertext = str2byte(ciphertext)
    passwd = AES.new(key, mode, vector).decrypt(ciphertext)
    return str(passwd)[2:-1].replace(" ", "")


def byte2str(byte):
    string = ""
    for token in byte:
        string = string + str(token) + " "
    return string


def str2byte(string):
    byte = b''
    for token in string.split(' ')[:-1]:
        byte = byte + int(token).to_bytes(1, "big")
    return byte

# def byte2str(byte):
#     return codecs.escape_encode(byte)[0]
#
#
# def str2byte(string):
#     return codecs.escape_decode(string)[0]


def rand_str():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=byte_len))
