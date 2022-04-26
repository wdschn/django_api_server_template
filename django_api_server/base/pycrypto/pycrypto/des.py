from cryptography.hazmat.primitives.ciphers import algorithms

from .symmetric import SymmetricCipher


class TripleDES(SymmetricCipher):
    algorithm = algorithms.TripleDES
