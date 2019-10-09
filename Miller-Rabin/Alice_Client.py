# Sanjay Santokee 81600051
from random import randrange, getrandbits
from socket import *
from itertools import repeat


def clientSetup():
    s = socket(AF_INET, SOCK_STREAM)
    host = gethostbyname('127.0.0.1')
    port = 12346
    server_addr = (host, port)
    s.connect(server_addr)
    return s


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
a = getPrime(10)



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


def secretKey(a):
    return pow(q, a, p)


def sharedKey(B, a):
    return pow(B, a, p)


def readFile():
    try:
        file = open("NoWar.dat", mode='rb')
    except IOError:
        print('File is not accessible')

    text = file.read(4096)
    text = str(text, 'UTF-8')
    return text


def main():
    s = clientSetup()

    # Getting B from Bob
    B = s.recv(1024)
    B = str(B, 'UTF-8')
    B = int(B)

    # Calculating A
    A = secretKey(a)

    # Sending A to Bob
    A = str(A)
    A = bytes(A, 'UTF-8')
    s.send(A)

    # Calculating Shared Key
    s2 = sharedKey(B, a)

    # Encrypting Message
    message = readFile()
    encryptedArr = caeserAlgorithm(message, s2)
    encryptedMsg = ''.join(encryptedArr)

    # Sending Message
    encryptedMsg = bytes(encryptedMsg, 'UTF-8')
    s.send(encryptedMsg)

    # Closing Socket
    s.close()


main()

