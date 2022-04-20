from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# cryptography.hazmat.primitives.asymmetric.padding.OAEP 推荐的 rsa 加密填充
# cryptography.hazmat.primitives.asymmetric.padding.PSS 推荐的 rsa 签名填充
# cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15 可以作为 rsa 加密和签名填充，但是不建议在新的应用程序中使用它

ALGORITHMES = {
    'sha1': hashes.SHA1(),
    'sha224': hashes.SHA224(),
    'sha256': hashes.SHA256(),
    'sha384': hashes.SHA384(),
    'sha512': hashes.SHA512(),
}


class PycryptoException(Exception):
    pass


class Rsa(object):
    def __init__(self, public_key=None, private_key=None, padding_mode='OAEP', algorithme=None):

        if algorithme and algorithme not in ALGORITHMES.keys():
            raise PycryptoException('The {algorithm} algorithm is not supported' % algorithme)

        self.public_key = public_key
        self.private_key = private_key
        self.padding_mode = padding_mode
        self.algorithme = algorithme

    def get_algorithme(self, algorithme='sha256'):
        return ALGORITHMES[algorithme]

    def oaep_padding(self, algorithm_sha):
        return padding.OAEP(
            mgf=padding.MGF1(algorithm=algorithm_sha),
            algorithm=algorithm_sha,
            label=None
        )

    def pss_padding(self, algorithm_sha):
        return padding.PSS(
            mgf=padding.MGF1(algorithm_sha),
            salt_length=padding.PSS.MAX_LENGTH
        )

    def pkcs1v15(self):
        return padding.PKCS1v15()

    def get_padding(self, padding_mode, algorithm=None):
        if padding_mode in ('OAEP', 'PSS') and algorithm is None:
            raise PycryptoException("algorithm isn't None when padding_mode is OAEP or PSS")
        if padding_mode == 'OAEP':
            return self.oaep_padding(algorithm)
        if padding_mode == 'PSS':
            return self.pss_padding(algorithm)
        if padding_mode == 'PKCS1v15':
            return self.pkcs1v15()
        raise PycryptoException('%s is not supported' % padding_mode)

    def decrypt(self, private_key, ciphertext, padding_mode='OAEP', algorithm=None):
        if padding_mode not in ('PKCS1v15', 'OAEP'):
            raise PycryptoException('Rsa decrypt padding only supports PKCS1v15 or OAEP')
        if padding_mode == 'OAEP' and algorithm is None:
            raise PycryptoException("algorithm isn't None when padding_mode is OAEP")
        if padding_mode == 'OAEP':
            algorithm = self.get_algorithme(algorithm)

        plaintext = private_key.decrypt(
            ciphertext,
            self.get_padding(padding_mode=padding_mode, algorithm=algorithm)
        )
        return plaintext
