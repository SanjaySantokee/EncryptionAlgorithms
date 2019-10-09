# Sanjay Santokee 81600051

import time
from socket import *
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pss


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
    c = serverSetup()
    c, addr = c.accept()
    print('Connection from: ' + str(addr))

    signature = c.recv(4096)
    confirmation = "Signature received at bob"
    c.send(confirmation.encode())

    message = c.recv(4096)
    confirmation = "Message received at bob"
    c.send(confirmation.encode())

    public_key = RSA.import_key(open('public.pem').read())
    hash_obj = SHA256.new(message)
    verifier = pss.new(public_key)
    try:
        verifier.verify(hash_obj, signature)
        print("The signature is authentic.")
        print(message)
    except (ValueError, TypeError):
        print("The signature is not authentic.")



main()
