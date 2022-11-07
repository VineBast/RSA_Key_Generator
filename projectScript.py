import os
from batch_gcd import batch_gcd
from base64 import b64decode


privateKeys_256 = []
privateKeys_512 = []


# Formate le nom de la clé en fonction de son index et du nombre de bits
# et renvoie un string avec ce nom formaté :

def keyString(bits, index):
    if (bits == 512):
        return "key512_"+str(index)+".rsa"
    if (bits == 256):
        return "key256_"+str(index)+".rsa"



# Ouvre et renvoie la clé cible selon le nom formaté :

def openKey(keyString):
    with open(keyString, mode='r') as rsa:
        return rsa.read()


# Ajoute une clé (grâce aux fonctions keyString() et openKey())
# au tableau entré en paramètre (et supprime les sauts de ligne + le début et la fin de la clé RSA) :

def addToArray(keyString, privateKeysArray):
    key = openKey(keyString)
    key = key.replace('-----BEGIN RSA PRIVATE KEY-----', '')
    key = key.replace('-----END RSA PRIVATE KEY-----', '')
    key = key.replace('\n', '')
    privateKeysArray.append(int.from_bytes(b64decode(key), 'big'))


# Créé un nimbre de clés défini (keysNum), de la longueur de bits entrée en paramètre (bits)
# et ajoute cette clé dans le tableau entré en paramètre (privateKeysArray) :

def createKeys(keysNum, bits, privateKeysArray):
    for i in range(keysNum):
        key = keyString(bits, i)
        os.system("openssl genrsa -out "+key+" "+str(bits))
        addToArray(key, privateKeysArray)
        print("Key "+str(bits)+" n° " + str(i) + " created")


# Permet de relancer l'ajout des clés, n'est pas utilisé dans le script ici,
# mais est utile en cas de crash de VM pour relancer la comparaison en faisant un loop
# sur les clés créées et les ajouter à un tableau :

def loopKeys(nb, privateKeysArray, bits):
    for i in range(nb):
        addToArray(keyString(bits, i), privateKeysArray)
        print("Rsa n°"+str(i))


# Cette fonction de comparaison est hautement inspirée de la source suivante :
# https://stackoverflow.com/questions/9835762/how-do-i-find-the-duplicates-in-a-list-and-create-another-list-with-them
# Ajoute les nouvelles clés dans un objet (Pourquoi un objet ? Pour la rapidité des loops sur un objet).
# Donc : si cette clé n'est pas dans l'objet, on l'ajoute dans l'objet et  dans le tableau, sinon, on l'ajoute pas.
# La fonction écrit dans un fichier .txt (result_256.txt et result_512.txt) le nombre de clés au départ puis le nombre de clé sans doublon,
# puis le nombre de doublons.
# Puis print les fichiers txt (les résultat sont donc aussi consultable avec un "cat result_256.txt" ou "result_512.txt") 
# En dernier lieu, la fonction batch_gcd() est appelée sur le tableau de clés uniques et son résultat est ajouté 
#  sous forme de tableau dans un fichier .txt (gcd_256.txt et gcd_512.txt) :

def compareKeys(privateKeysArray, bits):
    resultFile = (open("result_"+str(bits)+".txt", "a"))
    startingNbKeys = "Starting number of keys_" + \
        str(bits)+" : " + str(len(privateKeysArray))
    resultFile.write(startingNbKeys)
    resultFile.write("\n")
    seenKeys = set()
    uniqKeys = []

    for key in privateKeysArray:
        if key not in seenKeys:
            uniqKeys.append(key)
            seenKeys.add(key)

    resultUniqKeys = "Finale number of unique keys_" + \
        str(bits)+" : "+str(len(uniqKeys))
    resultFile.write(resultUniqKeys)
    resultFile.write("\n")
    resultDupKeys = "Number of duplicate keys_" + \
        str(bits)+" : " + str(len(privateKeysArray) - len(uniqKeys))
    resultFile.write(resultDupKeys)
    resultFile.write("\n")
    resultFile.close()

    fileToRead = (open("result_"+str(bits)+".txt", "r"))
    print(fileToRead.read())
    fileToRead.close()

    gcdArray = batch_gcd(*uniqKeys)
    gcdFile = (open("gcd_"+str(bits)+".txt", "a"))
    gcdFile.write(str(gcdArray))
    gcdFile.close()


# Lance la création des clés de 256 bits et les compare :
createKeys(1000001, 256, privateKeys_256)
compareKeys(privateKeys_256, 256)
# Lance la création des clés de 512 bits et les compare :
createKeys(1000001, 512, privateKeys_512)
compareKeys(privateKeys_512, 512)
