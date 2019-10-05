
from Crypto.PublicKey import RSA


def generate_ssh_keys():
    key = RSA.generate(2048)
    private_key = key.exportKey('PEM')
    public_key = key.publickey().exportKey('OpenSSH')

    return (private_key, public_key)
