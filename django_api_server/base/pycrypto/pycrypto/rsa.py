from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature
from .exceptions import PycryptoException


# cryptography.hazmat.primitives.asymmetric.padding.OAEP 推荐的 rsa 加密填充
# cryptography.hazmat.primitives.asymmetric.padding.PSS 推荐的 rsa 签名填充
# cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15 可以作为 rsa 加密和签名填充，但是不建议在新的应用程序中使用它

class Rsa(object):
    ALGORITHMES = {
        'sha1': hashes.SHA1(),
        'sha224': hashes.SHA224(),
        'sha256': hashes.SHA256(),
        'sha384': hashes.SHA384(),
        'sha512': hashes.SHA512(),
    }

    @classmethod
    def get_algorithme(cls, mode='sha256'):
        if mode not in cls.ALGORITHMES.keys():
            raise PycryptoException('The {algorithm} algorithm is not supported' % mode)
        return cls.ALGORITHMES[mode]

    @classmethod
    def generate_private_key(cls):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        return private_key

    @classmethod
    def get_public_key_from_private_key(cls, private_key):
        return private_key.public_key()

    @classmethod
    def load_pem_private_key(cls, pem_private_key_text, password=None):
        password = password if password is None else password.encode()
        private_key = serialization.load_pem_private_key(
            pem_private_key_text,
            password=password,
            backend=default_backend()
        )
        return private_key

    @classmethod
    def load_pem_public_key(cls, pem_public_key_text):
        private_key = serialization.load_pem_public_key(
            pem_public_key_text,
            backend=default_backend()
        )
        return private_key

    @classmethod
    def dump_pem_private_key(cls, pem_private_key, password=None):
        pwd = serialization.NoEncryption() if password is None else serialization.BestAvailableEncryption(password.encode())
        pem_private_text = pem_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=pwd
        )
        return pem_private_text

    @classmethod
    def dump_pem_public_key(cls, pem_public_key):
        pem_public_key_text = pem_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem_public_key_text

    @classmethod
    def pss_padding(cls, algorithm_sha):
        return padding.PSS(
            mgf=padding.MGF1(algorithm_sha),
            salt_length=padding.PSS.MAX_LENGTH
        )

    @classmethod
    def oaep_padding(cls, algorithm_sha):
        return padding.OAEP(
            mgf=padding.MGF1(algorithm=algorithm_sha),
            algorithm=algorithm_sha,
            label=None
        )

    @classmethod
    def pkcs1v15(cls):
        return padding.PKCS1v15()

    @classmethod
    def get_padding(cls, padding_mode, algorithm=None):
        if padding_mode in ('OAEP', 'PSS') and algorithm is None:
            raise PycryptoException('')
        if padding_mode == 'OAEP':
            return cls.oaep_padding(algorithm)
        if padding_mode == 'PSS':
            return cls.pss_padding(algorithm)
        if padding_mode == 'PKCS1v15':
            return cls.pkcs1v15()
        raise PycryptoException('%s is not supported' % padding_mode)

    @classmethod
    def sign(cls, private_key, data, padding_mode='PSS', algorithm='sha256'):
        if padding_mode not in ('PKCS1v15', 'PSS'):
            raise PycryptoException('sign padding only supports PKCS1v15 or PSS')

        if not isinstance(data, bytes):
            data = data.encode()
        algorithm = cls.get_algorithme(algorithm)
        return private_key.sign(
            data,
            cls.get_padding(padding_mode=padding_mode, algorithm=algorithm),
            algorithm
        )

    @classmethod
    def verify_sign(cls, public_key, signature, data, padding_mode='PSS', algorithm='sha256'):
        if padding_mode not in ('PKCS1v15', 'PSS'):
            raise PycryptoException('sign padding only supports PKCS1v15 or PSS')

        if not isinstance(data, bytes):
            data = data.encode()
        algorithm = cls.get_algorithme(algorithm)

        try:
            public_key.verify(
                signature,
                data,
                cls.get_padding(padding_mode=padding_mode, algorithm=algorithm),
                algorithm
            )
        except InvalidSignature:
            return False
        return True

    @classmethod
    def encrypt(cls, public_key, data, padding_mode='OAEP', algorithm='sha256'):
        if padding_mode not in ('PKCS1v15', 'OAEP'):
            raise PycryptoException('Rsa encrypt padding only supports PKCS1v15 or OAEP')

        algorithm = cls.get_algorithme(algorithm)
        ciphertext = public_key.encrypt(
            data,
            cls.get_padding(padding_mode=padding_mode, algorithm=algorithm)
        )
        return ciphertext

    @classmethod
    def decrypt(cls, private_key, ciphertext, padding_mode='OAEP', algorithm='sha256'):
        if padding_mode not in ('PKCS1v15', 'OAEP'):
            raise PycryptoException('Rsa decrypt padding only supports PKCS1v15 or OAEP')

        algorithm = cls.get_algorithme(algorithm)
        plaintext = private_key.decrypt(
            ciphertext,
            cls.get_padding(padding_mode=padding_mode, algorithm=algorithm)
        )
        return plaintext
