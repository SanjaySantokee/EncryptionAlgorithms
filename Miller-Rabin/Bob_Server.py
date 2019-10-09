# Sanjay Santokee 81600051

from random import randrange, getrandbits
from socket import *
from itertools import repeat

def serverSetup():
    c = socket(AF_INET, SOCK_STREAM)
    host = gethostbyname('127.0.0.1')
    port = 12346
    host_addr = (host, port)
    c.bind(host_addr)
    c.listen(10)
    print('Waiting on connection...')
    return c

def getPrime(n):
    """Get a n-bit pseudo-random prime"""

    def isProbablePrime(n, t=7):
        """Miller-Rabin primality test"""

        def isComposite(a):
            """Check if n is composite"""
            if pow(a, d, n) == 1:
                return False
            for i in range(s):
                if pow(a, 2 ** i * d, n) == n - 1:
                    return False
            return True

        assert n > 0
        if n < 3:
            return [False, False, True][n]
        elif not n & 1:
            return False
        else:
            s, d = 0, n - 1
            while not d & 1:
                s += 1
                d >>= 1
        for _ in repeat(None, t):
            if isComposite(randrange(2, n)):
                return False
        return True

    p = getrandbits(n)
    while not isProbablePrime(p):
        p = getrandbits(n)
    return p


p = 23
q = 5
b = getPrime(10)


def caeserAlgorithm(text, key):
    encryptedText = []
    for x in range(0, len(text)):
        letter = ord(text[x])  # letter -> ASCII
        encryptedLetter = (letter + key) % 128
        encryptedLetter = chr(encryptedLetter)  # ASCII -> letter
        encryptedText.append(encryptedLetter)

    return encryptedText


def caeserAlgorithmDecrypt(text, key):
    encryptedText = []
    for x in range(0, len(text)):
        letter = ord(text[x])  # letter -> ASCII
        encryptedLetter = (letter - key) % 128
        encryptedLetter = chr(encryptedLetter)  # ASCII -> letter
        encryptedText.append(encryptedLetter)

    encryptedString = ''.join(encryptedText)
    return encryptedString


def secretKey(b):
    return pow(q, b, p)


def sharedKey(A, b):
    return pow(A, b, p)


def main():
    c = serverSetup()
    c, addr = c.accept()
    print('Connection from: ' + str(addr))

    # Calculating B
    B = secretKey(b)  # calc using secret number

    # Sending B to Alice
    B = str(B)
    B = bytes(B, 'UTF-8')
    c.send(B)

    # Getting A from Alice
    A = c.recv(1024)
    A = str(A, "UTF-8")
    A = int(A)

    # Calculating Shared Key
    s1 = sharedKey(A, b)

    # Getting encrypted message
    encryptedMsg = c.recv(4096)
    encryptedMsg = str(encryptedMsg, "UTF-8")

    # Decrypting message
    message = caeserAlgorithmDecrypt(encryptedMsg, s1)

    print("The Message from Alice was: ")
    print(message)


main()
