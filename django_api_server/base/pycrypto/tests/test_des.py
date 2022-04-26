import os
import random

from unittest import TestCase

from cryptography.hazmat.primitives.ciphers import algorithms

from ..pycrypto.des import TripleDES
from ..pycrypto.exceptions import PycryptoException

class TripleDESTestCase(TestCase):
    def test_tripleDES(self):
        for x in range(100):
            key = os.urandom(8)
            iv = os.urandom(int(algorithms.TripleDES.block_size / 8))
            message = os.urandom(random.randint(3000, 6000))
            print(message)
            aes = TripleDES(key)
            crypted_data = aes.encrypt(message, mode='ECB',  padding_mode='PKCS7')
            uncrypted_data = aes.decrypt(crypted_data, mode='ECB', padding_mode='PKCS7')
            if uncrypted_data != message:
                raise PycryptoException('err')
        print('success')
