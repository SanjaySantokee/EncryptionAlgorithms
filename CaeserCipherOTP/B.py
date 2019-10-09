from socket import *

s = socket(AF_INET, SOCK_STREAM)
host = gethostbyname('127.0.0.1')
port = 12345
host_addr = (host, port)
s.bind(host_addr)
s.listen(10)
print('Waiting on connection...')

#1
def caeserAlgorithmDecrypt(text, key):
    encryptedText = []
    for x in range(0, len(text)):
        letter = ord(text[x])  # letter -> ASCII
        encryptedLetter = (letter - key) % 128
        encryptedLetter = chr(encryptedLetter)  # ASCII -> letter
        encryptedText.append(encryptedLetter)
        
    encryptedString = ''.join(encryptedText)
    return encryptedString
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

def writeFile(message):
    outputFile = open('Trump.dat', 'wb')

    outputFile.write(bytes(message, 'UTF-8'))
    outputFile.close()


c, addr = s.accept()
print('Connection from: ' + str(addr))
print('Receiving... ')
encryptedKey = c.recv(4096)
encryptedKey = str(encryptedKey, 'UTF-8')

key = caeserAlgorithmDecrypt(encryptedKey, 4)

keyStr = convertToBinary(key)

encryptedMsg = c.recv(4096)
encryptedMsg = str(encryptedMsg, 'UTF-8')

writeFile(encryptedMsg)

#Opening file 
try:
    file = open("Trump.dat", mode='rb')
except IOError:
    print('File is not accessible')
print('File is accessible')

encryptedMsg = file.read(4096)
encryptedMsg = str(encryptedMsg, 'UTF-8')

binaryText = findXOR(encryptedMsg, keyStr)

decryptedMsg = convertToString(binaryText)


print(decryptedMsg)


print('Done Receiving...')
print('Receiver Ended')

file.close()
