import os
import random

from unittest import TestCase

from cryptography.hazmat.primitives.ciphers import algorithms

from ..pycrypto.aes import Aes
from ..pycrypto.exceptions import PycryptoException


class AesTestCase(TestCase):
    def test_aes(self):
        key_length = [16, 24, 32]
        for key_len in key_length:
            key = os.urandom(key_len)
            iv = os.urandom(int(algorithms.AES.block_size/8))
            for x in range(2):
                message = os.urandom(random.randint(3000, 6000))
                aes = Aes(key)
                crypted_data = aes.encrypt(message, mode='CBC', iv=iv, padding_mode='PKCS7')
                uncrypted_data = aes.decrypt(crypted_data, mode='CBC', iv=iv, padding_mode='PKCS7')
                if uncrypted_data != message:
                    raise PycryptoException('err')
        print('success')
