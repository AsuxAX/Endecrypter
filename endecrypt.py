from Crypto.Cipher import AES
from secrets import choice
from string import ascii_letters
from Crypto import Random
import os

def pad(s):
    padding_size = AES.block_size - len(s) % AES.block_size
    return s + b"\0" * padding_size, padding_size

def decrypttext(key, ctext):
    nonce = ctext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt(ctext[AES.block_size:-1])
    padding_size = ctext[-1] * (-1)
    return plaintext[:padding_size]

def encrypttext(key, text):
    text, padding_size = pad(text)
    nonce = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    enc_bytes = nonce + cipher.encrypt(text) + bytes([padding_size])
    return enc_bytes

def generatekey():
    letters = ascii_letters, "0123456789", "!\"'#$%&()*+,-./;<>?@[\]^_`{|}~"
    key = ""
    for i in range(32):
        key += choice(letters[0]) + choice(letters[1]) + choice(letters[2])
    return key[:32]




# -------------------------------------------------------------------------------------------------------------------- #




filepathls = list()

while True:
    userchoice = input("Mode: [E] Encryption\t[D] Decryption: ").capitalize()
    if userchoice in ["E", "D"]:
        break
    else:
        print("Invalid choice, try again.\n")
while True:
    fileselchoice = input("File selection: [1] One file [2] Multiple files [3] Folder selection: ")
    if fileselchoice in ["1","2","3"]:
        break
    else:
        print("Invalid choice, try again.\n")

if fileselchoice == "1":
    while True:
        filepath = input("\nFile path: ")
        if os.path.isfile(filepath):
            filepathls.append(filepath)
            break
        else:
            print("Path does not exist, try again.\n")
elif fileselchoice == "2" or fileselchoice == "3":
    if userchoice == "D":
        keyu = input("Key: ").encode()
    else:
        pass
    if fileselchoice == "2":
        while True:
            filepath = input("\nFile path [type done when done]: ")
            if os.path.isfile(filepath):
                filepathls.append(filepath)
            elif filepath.lower() == "done":
                break
            else:
                print("Path does not exist, try again.\n")
    else:
        while True:
            folderpath = input("\nFolder path: ")
            if os.path.isdir(folderpath):
                for fif in os.listdir(folderpath):
                    if os.path.isfile(folderpath + "\\" + fif):
                        filepathls.append(folderpath + "\\" + fif)
                break
            else:
                print("Path does not exist, try again.\n")

if userchoice == "E":
    for f in filepathls:
        if f.endswith(".enc"):
            print("File has the .enc extension already, aborting process to avoid irreversible actions.")
            quit()
        else:
            pass
    while True:
        keychoice = input("Key: [R] Random\t[M] Manual: ").capitalize()
        if keychoice in ["R", "M"]:
            break
        else:
            print("Invalid choice, try again.\n")
    if keychoice == "R":
        key = generatekey().encode()
    else: # elif keychoice == "M"
        while True:
            key = input("Enter key [16, 24, 32]: ").encode()
            if len(key) in [16, 24, 32]:
                break
            else:
                print("Key too short or long, try again.")
    for f in filepathls:
        with open(f, "rb+") as file:
            print("\nEncrypting {}".format(f))
            content = file.read()
            file.seek(0)
            econtent = encrypttext(key, content)
            file.write(econtent)
            file.truncate()
            file.close()
            os.rename(f, f + ".enc")
            print("Encryption complete!")
            print("\nKey: " + key.decode())

else:
    for f in filepathls:
        if not f.endswith(".enc"):
            print("File does not end with the .enc file extension.")
            quit()
        else:
            pass
        if fileselchoice == "1":
            keyu = input("Key: ").encode()
        else:
            pass
        with open(f, "rb+") as file:
            print("\nDecrypting {}".format(f))
            content = file.read()
            file.seek(0)
            dcontent = decrypttext(keyu, content)
            file.write(dcontent)
            file.truncate()
            file.close()
            os.rename(f, f[:-4])
            print("Decryption complete!")
