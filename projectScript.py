import os

privateKeys_256 = []
privateKeys_512 = []


# Formate le nom de la clé en fonction de son index et du nombre de bits
# et renvoie un string avec ce nom formaté :


def keyString(bits, index):
    if (bits == 512):
        return "key512_"+str(index)+".pem"
    if (bits == 256):
        return "key256_"+str(index)+".pem"


# Ouvre et renvoie la clé cible selon le nom formaté :


def openKey(keyString):
    with open(keyString, mode='r') as pem:
        return pem.read()


# Ajoute une clé (grâce aux fonctions keyString() et openKey())
# au tableau entré en paramètre :


def addToArray(keyString, privateKeysArray):
    privateKeysArray.append(openKey(keyString))


# Créé un nimbre de clés défini (keysNum), de la longueur de bits entrée en paramètre (bits)
# et ajoute cette clé dans le tableau entré en paramètre (privateKeysArray) :


def createKeys(keysNum, bits, privateKeysArray):
    for i in range(keysNum):
        key = keyString(bits, i)
        os.system("openssl genrsa -out "+key+" "+str(bits))
        addToArray(key, privateKeysArray)
        print("Key "+str(bits)+" n° " + str(i) + " created")


def loopKeys(nb, array):
    for i in range(nb):
        addToArray(keyString(512, i), array)
        print("Pem n°"+str(i))


# Cette fonction de comparaison est hautement inspirée de la source suivante :
# https://stackoverflow.com/questions/9835762/how-do-i-find-the-duplicates-in-a-list-and-create-another-list-with-them
# Ajoute les nouvelles clés dans un objet (Pourquoi un objet ? Pour la rapidité des loops sur un objet).
# Donc : si cette clé n'est pas dans l'objet, on l'ajoute dans l'objet et  dans le tableau, sinon, on l'ajoute pas.
# La fonction print le nombre de clé du départ puis le nombre de clé sans doublon, puis le nombre de doublons,
# et ajoute ces résultats dans un fichier result_256.txt ou result_512.txt :


def compareKeys(privateKeysArray, bits):
    print("Starting len keys_"+str(bits)+" :", len(privateKeysArray))
    resultFile = open("result_"+str(bits)+".txt", "a")
    seenKeys = set()
    uniqKeys = []
    for key in privateKeysArray:
        if key not in seenKeys:
            uniqKeys.append(key)
            seenKeys.add(key)
    resultFile.write("Finale len keys :")
    resultFile.write(str(len(seenKeys)))
    print("Finale len keys :", len(seenKeys))
    print("Number of duplicate keys : ", len(privateKeysArray) - len(uniqKeys))


# Lance la création des clés de 256 bits et les compare :
#createKeys(1000001, 256, privateKeys_256)
#compareKeys(privateKeys_256, 256)
#compareKeysWithArrays(256, privateKeys_256)
# Lance la création des clés de 512 bits et les compare :
#createKeys(1000001, 512, privateKeys_512)
#compareKeys(privateKeys_256, 256)
