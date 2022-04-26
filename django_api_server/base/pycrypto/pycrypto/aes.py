from cryptography.hazmat.primitives.ciphers import algorithms

from .symmetric import SymmetricCipher


class Aes(SymmetricCipher):
    algorithm = algorithms.AES
