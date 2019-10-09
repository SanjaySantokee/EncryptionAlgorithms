# Sanjay Santokee 81600051

from socket import *
from Cryptodome.Cipher import DES
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes


def clientSetup():
    s = socket(AF_INET, SOCK_STREAM)
    host = gethostbyname('127.0.0.1')
    port = 12345
    server_addr = (host, port)
    s.connect(server_addr)
    return s


def readFile(fileName):
    try:
        file = open(fileName, mode='rb')
    except IOError:
        print('File is not accessible')

    text = file.read()
    text = str(text, 'UTF-8')
    file.close()
    return text


def writeFile(fileName, data):
    out = open(fileName, "wb")
    out.write(data)


def main():
    s = clientSetup()

    # Gets Public Key from Bob
    # public_key = s.recv(4096).decode()
    public_key = RSA.import_key(open("public.pem").read())
    # Generates Session Key
    session_key = get_random_bytes(8)

    # Sends Encrypted Session Key to Bob
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    s.send(enc_session_key)
    confirmation = s.recv(4096).decode()
    print(confirmation)

    # Reads NoWar.dat file
    message = readFile("NoWar.dat").encode()

    # Using DES to transmit message to Bob
    cipher = DES.new(session_key, DES.MODE_EAX)
    cipherText = cipher.encrypt(message)

    s.send(cipher.nonce)
    confirmation = s.recv(4096).decode()
    print(confirmation)

    s.send(cipherText)
    confirmation = s.recv(4096).decode()
    print(confirmation)

    # Closing Socket
    s.close()


main()
