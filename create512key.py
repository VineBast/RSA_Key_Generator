import os

for i in range(1000000):
    keyString = "key512_"+str(i)+".pem"
    os.system("openssl genrsa -out "+keyString+" 512")
