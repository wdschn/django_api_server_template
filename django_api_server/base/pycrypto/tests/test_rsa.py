import os
import random
import string
from unittest import TestCase

from ..pycrypto.rsa import Rsa
from ..pycrypto.exceptions import PycryptoException

PASSWORD = 'mypassword'


def get_random_bytes(length):
    return os.urandom(length)
    # source_str = string.digits + string.ascii_letters
    # return ''.join([source_str[random.randint(0, len(source_str) - 1)] for x in range(length)])


class TestRsa(TestCase):

    def setUp(self):
        self.private_key = Rsa.generate_private_key()
        self.public_key = Rsa.get_public_key_from_private_key(self.private_key)

    def test_sign(self):
        for x in range(50):
            message = get_random_bytes(x)
            for padding_mode in ('PKCS1v15', 'PSS'):
                sign = Rsa.sign(private_key=self.private_key, data=message, padding_mode=padding_mode)
                if not Rsa.verify_sign(public_key=self.public_key, signature=sign, data=message, padding_mode=padding_mode):
                    raise PycryptoException('verify sign error')

    def test_crypto(self):
        for x in range(50):
            message = get_random_bytes(x)
            for padding_mode in ('PKCS1v15', 'OAEP'):
                ciphertext = Rsa.encrypt(public_key=self.public_key, data=message, padding_mode=padding_mode)
                plaintext = Rsa.decrypt(private_key=self.private_key, ciphertext=ciphertext, padding_mode=padding_mode)
                if plaintext != message:
                    raise PycryptoException('crypto error')
