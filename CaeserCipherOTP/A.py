import random
from socket import *

s = socket(AF_INET, SOCK_STREAM)
host = gethostbyname('127.0.0.1')
port = 12345
server_addr = (host, port)
s.connect(server_addr)

#1
def caeserAlgorithm(text, key):
    encryptedText = []
    for x in range(0, len(text)):
        letter = ord(text[x])  # letter -> ASCII
        encryptedLetter = (letter + key) % 128
        encryptedLetter = chr(encryptedLetter)  # ASCII -> letter
        encryptedText.append(encryptedLetter)

    return encryptedText
#2
def convertToBinary(encryptedText):
    encryptedStr = []
    for letter in range(0, len(encryptedText)):
        encryptedStr.append(bin(ord(encryptedText[letter]))[2:].zfill(7))    # text -> Binary
    encryptedString = ''.join(encryptedStr)
    return encryptedString


# 3
def convertToString(bitstring):
    bitString = []
    string = []
    start = 0
    end = 7
    for i in range(0, (int(len(bitstring)/7))):
        bitString.append(bitstring[start:end])
        start += 7
        end += 7
    for x in bitString:
        string.append(chr(int(x, 2)))
    return ''.join(string)

# 4
def generateRandomBitString(k):
    randomBits = []
    for x in range(k):
        randomBits.append(str(random.randint(0, 1)))

    randomBitString = ''.join(randomBits)

    return randomBitString

# 5
def findXOR(bitString1, bitString2):
    xor = []
    length = min(len(bitString1), len(bitString2))

    for x in range(0, length):
        value = int(bitString1[x]) ^ int(bitString2[x])
        xor.append(str(value))

    xorString = ''.join(xor)

    return xorString


#main
try:
    file = open("NoWar.dat", mode='rb')
except IOError:
    print('File is not accessible')
print('File is accessible')

text = file.read(4096)
text = str(text, 'UTF-8')


binaryText = convertToBinary(text)

length = len(binaryText)

key = generateRandomBitString(length)

keyStr = convertToString(key)

encryptedKey = caeserAlgorithm(keyStr, 4)
encryptedKeyString = ''.join(encryptedKey)

print ('Sending Key')
encryptedKeyString = bytes(encryptedKeyString, 'UTF-8')
s.send(encryptedKeyString)
print ('Done Sending Key')

# OTP Encryption
xorString = findXOR(binaryText, key)

#Sending Trump.dat
print("Sending Trump.dat")
xorString = bytes(xorString, 'UTF-8')
s.send(xorString)
print ('Done Sending Trump.dat')

file.close()
s.close()
print ('Sender Ended')

