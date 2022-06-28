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

while True:
    userchoice = input("Mode: [E] Encryption\t[D] Decryption: ").capitalize()
    if userchoice in ["E", "D"]:
        break
    else:
        print("Invalid choice, try again.\n")

while True:
    filepath = input("\nFile path: ")
    if os.path.isfile(filepath):
        break
    else:
        print("Path does not exist, try again.\n")

if userchoice == "E":
    if filepath.endswith(".enc"):
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
    with open(filepath, "rb+") as file:
        print("\nEncrypting file...")
        content = file.read()
        file.seek(0)
        econtent = encrypttext(key, content)
        file.write(econtent)
        file.truncate()
        file.close()
        os.rename(filepath, filepath + ".enc")
        print("Encryption complete!\n")
        print("Key: " + key.decode())
else: # elif userchoice == "D"
    if not filepath.endswith(".enc"):
        print("File does not end with the .enc file extension.")
        quit()
    else:
        pass
    keyu = input("Key: ").encode()
    with open(filepath, "rb+") as file:
        print("\nDecrypting file...")
        content = file.read()
        file.seek(0)
        dcontent = decrypttext(keyu, content)
        file.write(dcontent)
        file.truncate()
        file.close()
        os.rename(filepath, filepath[:-4])
        print("Decryption complete!\n")