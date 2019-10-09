# Sanjay Santokee 81600051

from socket import *
from Cryptodome.PublicKey import RSA
from Crypto.Hash import SHA256
from Cryptodome.Signature import pss


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

    # Creates Private & Public Keys
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    writeFile("private.pem", private_key)
    writeFile("public.pem", public_key)

    print("Keys Generated")

    public_key = RSA.import_key(open("public.pem").read())
    private_key = RSA.import_key(open("private.pem").read())

    # Reads NoWar.dat file
    message = readFile("NoWar.dat").encode()

    print("Hashing Message")
    hash_obj = SHA256.new(message)
    signature = pss.new(private_key).sign(hash_obj)

    s.send(signature)
    confirmation = s.recv(4096).decode()
    print(confirmation)

    s.send(message)
    confirmation = s.recv(4096).decode()
    print(confirmation)

    # Closing Socket
    s.close()


main()
