# Sanjay Santokee 81600051

import time
from socket import *
from Cryptodome.Cipher import DES
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes


def serverSetup():
    c = socket(AF_INET, SOCK_STREAM)
    host = gethostbyname('127.0.0.1')
    port = 12345
    host_addr = (host, port)
    c.bind(host_addr)
    c.listen(1)
    print('Waiting on connection...')
    return c


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
    # Creates Private & Public Keys
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    writeFile("private.pem", private_key)
    writeFile("public.pem", public_key)

    print("Keys Generated")

    c = serverSetup()
    c, addr = c.accept()
    print('Connection from: ' + str(addr))

    # Sends Public Key to Alice
    # c.send(public_key)

    # Receives Encrypted Session Key from Alice
    enc_session_key = c.recv(1024)
    confirmation = "enc_session_key recieved at bob"
    c.send(confirmation.encode())

    # Bob Decrypts the Encrypted Session Key
    private = RSA.import_key(open("private.pem").read())
    cipher_rsa = PKCS1_OAEP.new(private)
    session_key = cipher_rsa.decrypt(enc_session_key)

    nonce = c.recv(4096)
    confirmation = "nonce received at bob"
    c.send(confirmation.encode())

    cipherText = c.recv(4096)
    confirmation = "cipherText received at bob"
    c.send(confirmation.encode())

    newCipher = DES.new(session_key, DES.MODE_EAX, nonce)
    message = newCipher.decrypt(cipherText)

    print(message)


main()
