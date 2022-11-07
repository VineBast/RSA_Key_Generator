import os
import time

privateKeys_256 = []
privateKeys_512 = []


def keyString(bits, index):
    if (bits == 512):
        return "key512_"+str(index)+".pem"
    if (bits == 256):
        return "key256_"+str(index)+".pem"


def openKey(keyString):
    with open(keyString, mode='r') as pem:
        return pem.read()


def createKeys(keysNum, bits, privateKeys):
    for i in range(keysNum):
        key = keyString(bits, i)
        os.system("openssl genrsa -out "+key+" "+str(bits))
        addToArray(key, privateKeys)
        print("Key "+str(bits)+" n° " + str(i) + " created")


def addToArray(keyString, privateKeys):
    privateKeys.append(openKey(keyString))


def loopKeys():
    for i in range(1000000):
        addToArray(keyString(512, i))
        print("Pem n°"+str(i))


def compareKeysWithArrays(bits, privateKeys):
    st = time.perf_counter()
    resultFile = open("result_"+str(bits)+".txt", "a")
    sameKeysFile = open("sameKeys_"+str(bits)+".txt", "a")
    result = 0
    for i in range(len(privateKeys)):
        if (i == len(privateKeys)):
            break
        z = i + 1
        lenArray = range(z, len(privateKeys))
        for y in lenArray:
            if (privateKeys[i] == privateKeys[y]):
                result += 1
                resultFile.write("We are at key pair n°"+str(i)+" and we have " +
                                 str(result)+" equivalent RSA-"+str(bits)+" keys. \n")
                sameKeysFile.write(str(i)+"\n")
                sameKeysFile.write(str(y)+"\n")
            print("Key pairs 512 n° " + str(i) + " compared to n° " + str(y))
    if (result == 0):
        print("No equivalent among RSA-"+str(bits) + " key pairs")
    elif (result == 1):
        print("There is " + str(result) + " " + str(bits) +
              " equivalent RSA-"+str(bits) + " key pairs")
    elif (result > 0):
        print("There are " + str(result) +
              " equivalent RSA-"+str(bits) + " key pairs")
    resultFile.close()
    sameKeysFile.close()
    end = time.perf_counter()
    print("Time sec =", end - st)


def testCompareKeys():
    loopKeys()
    print("Starting len keys :", len(privateKeys))
    resultFile = open("result_512.txt", "a")
    seen = set()
    uniq = []
    for x in privateKeys:
        if x not in seen:
            uniq.append(x)
            seen.add(x)
    resultFile.write("Finale len keys :")
    resultFile.write(str(len(seen)))
    print("Finale len keys :", len(seen))


# Lance la création des clés de 256 bits et les compare :
#createKeys(1000001, 256, privateKeys_256)
#compareKeysWithArrays(256, privateKeys_256)
# Lance la création des clés de 512 bits et les compare :
#createKeys(1000001, 512, privateKeys_512)
#compareKeysWithArrays(512, privateKeys_512)
