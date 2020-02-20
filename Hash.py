import sys
import hashlib


BUF_SIZE = 65536  

md5 = hashlib.md5()

def hashing(file):
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return ("MD5: {0}".format(md5.hexdigest()))



