import base64
import getpass
import socket
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class Security(object):

    def __init__(self):
        pass

    @staticmethod
    def _generateKey():
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update("{0}{1}".format(socket.gethostname(), getpass.getuser()))
        return base64.urlsafe_b64encode(digest.finalize())

    @staticmethod
    def encrypt(value):
        f = Fernet(Security._generateKey())
        return f.encrypt(bytes(value))

    @staticmethod
    def decrypt(value):
        f = Fernet(Security._generateKey())
        return f.decrypt(bytes(value))


if __name__ == '__main__':
    pass
