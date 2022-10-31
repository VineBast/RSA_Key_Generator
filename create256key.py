import os

for i in range(1000000):
    keyString = "key256_"+str(i)+".pem"
    os.system("openssl genrsa -out "+keyString+" 256")
    print("Key 256 n° " + str(i))
