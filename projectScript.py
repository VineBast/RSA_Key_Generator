import os
import time

privateKeys = []

def keyString(bits, index):
    if(bits == 512):
        return "key512_"+str(index)+".pem"
    if(bits == 256):
        return "key256_"+str(index)+".pem"


def keyStringPub(bits, index):
    if(bits == 512):
        return "key512_"+str(index)+"_pub.pem"
    if(bits == 256):
        return "key256_"+str(index)+"_pub.pem"


def openKey(keyString):
    with open(keyString, mode='r') as pem:
        return pem.read()


def create512Key(keysNum):
    for i in range(keysNum):
        key = keyString(512, i)
        os.system("openssl genrsa -out "+key+" 512")
        addToArray(key)
        print("Key 512 n° " + str(i) + " created")


def addToArray(keyString):
    privateKeys.append(openKey(keyString))


def loopKeys():
    for i in range(1000000):
        addToArray(keyString(512, i))
        print("Pem n°"+str(i))


def compareKeysWithArrays(bits):
    st = time.perf_counter()
    resultFile = open("result.txt", "x")
    result = 0
    for i in range(len(privateKeys)):
        if(i == len(privateKeys)):
            break
        z = i + 1
        lenArray = range(z, len(privateKeys))
        for y in lenArray:
            if(privateKeys[i] == privateKeys[y]):
                result += 1
                resultFile.write("We are at key pair n°"+str(i)+" and we have " +
                                 str(result)+" equivalent RSA-"+str(bits))
            print("Key pairs 512 n° " + str(i) + " compared to n° " + str(y))
    if(result == 0):
        print("No equivalent among RSA-"+str(bits) + " key pairs")
    elif(result == 1):
        print("There is " + str(result) + " " + str(bits) +
              " equivalent RSA-"+str(bits) + " key pairs")
    elif(result > 0):
        print("There are " + str(result) +
              " equivalent RSA-"+str(bits) + " key pairs")
    resultFile.close()
    end = time.perf_counter()
    print("Time sec =", end - st)


def compareKeys(bits, keysNum):
    result = 0
    for i in range(keysNum):
        key = keyString(bits, i)
        pemToCompare = openKey(key)
        keyPub = keyStringPub(bits, i)
        pemPubToCompare = openKey(keyPub)
        y = i + 1
        for y in range(keysNum):
            if(i == y):
                break
            key = keyString(bits, y)
            keyPub = keyStringPub(bits, y)
            tempPem = openKey(key)
            tempPemPub = open(keyPub)
            if((pemToCompare == tempPem) and (pemPubToCompare == tempPemPub)):
                result += 2
            print("Key pairs 512 n° " + str(i) + " compared to n° " + str(y))

    if(result == 0):
        print("No equivalent among RSA-"+str(bits) + " key pairs")
    elif(result == 1):
        print("There is " + str(result) + " " + str(bits) +
              " equivalent RSA-"+str(bits) + " key pairs")
    elif(result > 0):
        print("There are " + str(result) +
              " equivalent RSA-"+str(bits) + " key pairs")


create512Key(1000001)
compareKeysWithArrays(512)
