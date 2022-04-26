from enum import Enum

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from .exceptions import PycryptoException

PADDING_MODES = {
    'PADDINGCONTEXT': padding.PaddingContext,
    'ANSIX923': padding.ANSIX923,
    'PKCS7': padding.PKCS7,
}


class Modes(Enum):
    ECB = (modes.ECB, False)
    CBC = (modes.CBC, True)

    # CTR = (modes.CTR, True)
    # OFB = (modes.OFB, True)
    # CFB = (modes.CFB, True)
    # CFB8 = (modes.CFB8, True)
    # GCM = (modes.GCM, True)
    # XTS = (modes.XTS, False)

    def __init__(self, cls, need_iv):
        self.cls = cls
        self.need_iv = need_iv


class SymmetricCipher(object):
    algorithm = None

    def __init__(self, key):
        if isinstance(key, str):
            key = key.encode()
        self.key = key

    def padding(self, data, padding_mode='PKCS7'):
        padding_mode = padding_mode.upper()
        if padding_mode not in PADDING_MODES.keys():
            raise PycryptoException('不支持的填充')
        padder = PADDING_MODES[padding_mode](self.algorithm.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data

    def unpadding(self, data, padding_mode='PKCS7'):
        padding_mode = padding_mode.upper()
        if padding_mode not in PADDING_MODES.keys():
            raise PycryptoException('不支持的填充')
        unpadder = PADDING_MODES[padding_mode](self.algorithm.block_size).unpadder()
        unpadded_data = unpadder.update(data) + unpadder.finalize()
        return unpadded_data

    def get_mode(self, mode, iv=None):
        mode = mode.upper()
        if mode not in Modes.__members__:
            raise PycryptoException('不支持的分组模式')
        if Modes[mode].need_iv:
            return Modes[mode].cls(iv)
        return Modes[mode].cls()

    def encrypt(self, data, mode='CBC', iv=None, padding_mode='PKCS7'):
        cipher = Cipher(self.algorithm(self.key), self.get_mode(mode, iv))
        padded_data = self.padding(data=data, padding_mode=padding_mode)
        return cipher.encryptor().update(padded_data)

    def decrypt(self, data, mode='CBC', iv=None, padding_mode='PKCS7'):
        cipher = Cipher(self.algorithm(self.key), self.get_mode(mode, iv))
        decryption_data = cipher.decryptor().update(data)
        return self.unpadding(data=decryption_data, padding_mode=padding_mode)
