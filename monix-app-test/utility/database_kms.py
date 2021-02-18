# -*- coding: utf-8 -*-
import base64
import attr
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.backends import default_backend

@attr.s
class DatabaseKms(object):
    config = attr.ib(default=None)

    @staticmethod
    def pkcs7_pad(content):
        if not isinstance(content, bytes):
            content = content.encode()
        pad = PKCS7(algorithms.AES.block_size).padder()
        pad_content = pad.update(content) + pad.finalize()
        return pad_content

    @staticmethod
    def pkcs7_un_pad(content):
        pad = PKCS7(algorithms.AES.block_size).unpadder()
        pad_content = pad.update(content) + pad.finalize()
        return pad_content

    def aes_encrypt(self, content, key, iv=b'0000000000000000'):
        if not content:
            return None
        if not isinstance(content, bytes):
            content = content.encode()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        cryptors = cipher.encryptor()
        data = cryptors.update(self.pkcs7_pad(content))
        return base64.b64encode(data).decode()

    def aes_decrypt(self, content, key, iv=b'0000000000000000'):
        content = base64.b64decode(content)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        cryptors = cipher.decryptor()
        data = cryptors.update(content)
        data = self.pkcs7_un_pad(data)
        return data

if __name__=="__main__":
    res=DatabaseKms().aes_decrypt()
    print(res)


