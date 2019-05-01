# --coding:utf-8--*--

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from hashlib import sha256
from retrieve import updateMap
from tkinter import messagebox
import os
import re
import time


defaultpath = r"C:/software"
defaultpassword = "nooneknows"
size = 1024000


def _RSAKeyGen(password=defaultpassword):
    key = RSA.generate(2048)
    private_key = key.exportKey(passphrase=password, pkcs=8)
    public_key = key.publickey().exportKey()
    if not os.path.exists(defaultpath):
        os.mkdir(defaultpath)
        os.chdir(defaultpath)
    else:
        os.chdir(defaultpath)
    public_key_path = os.path.join(defaultpath, "public_key.pem")
    private_key_path = os.path.join(defaultpath, "private_key.bin")
    if not os.path.exists(private_key_path):
        try:
            f = open("private_key.bin", "wb+")
            f.write(private_key)
            f.close()
            messagebox.showinfo("success", "generate private_key in " + defaultpath)
        except OSError as e:
            messagebox.showinfo("error", e)
    else:
        return
    if not os.path.exists(public_key_path):
        try:
            f = open("public_key.pem", "wb+")
            f.write(public_key)
            f.close()
            messagebox.showinfo("success", "generate public_key in " + defaultpath)
        except OSError as e:
            messagebox.showinfo("error", e)
    else:
        return


def Encrypt(path, key=defaultpassword, publickey=defaultpath + "/public_key.pem"):
    if os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename == "sha256data.json":
                    continue
                filepath = dirpath + "/" + filename
                FileEncrypt(filepath, password=key, public_key=publickey)
        messagebox.showinfo("success", "加密完成")
    else:
        filename = GetFileName(path)
        if filename == "sha256data.json":
            return
        FileEncrypt(path, password=key, public_key=publickey)
        messagebox.showinfo("success", "加密完成")


def Decrypt(path, key=defaultpassword, privatekey=defaultpath + "/private_key.bin"):
    
    if os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if len(filename) != 64:
                    continue
                elif filename == "sha256data.json":
                    continue
                filepath = dirpath + "/" + filename
                FileDecrypt(filepath, password=key, private_key=privatekey)
        messagebox.showinfo("success", "解密完成")
    else:
        filename = GetFileName(path)
        if filename == "sha256data.json":
            return
        FileDecrypt(path, password=key, private_key=privatekey)
        messagebox.showinfo("success", "解密完成")
	


def FileEncrypt(filepath, password=defaultpassword, public_key=defaultpath + "/public_key.pem"):
    """
    if os.path.getsize(filepath) >= (2<<20):
        return 1
    """
    _RSAKeyGen(password)
    start = time.clock()
    dir = GetFileDir(filepath)
    filename = GetFileName(filepath)
    updateMap(dir, filename, "E")
    filenamesha256 = sha256(filename.encode("utf-8")).hexdigest()
    try:
        mfp = open(filepath, "rb")
        cfp = open(os.path.join(dir + "/", filenamesha256), "wb")
    except OSError as e:
        messagebox.showinfo("error", e)
        return
    public_key_data = RSA.importKey(open(public_key).read())
    sessionstr = get_random_bytes(32)
    sessioncipher = PKCS1_OAEP.new(public_key_data)
    sessionkey = sessioncipher.encrypt(sessionstr)
    cfp.write(sessionkey)
    filenamekey = sessioncipher.encrypt(bytes(filename, encoding="utf-8"))
    cfp.write(filenamekey)
    datacipher = AES.new(sessionstr, AES.MODE_EAX)
    message = mfp.read(size)
    while message:
        nonce = datacipher.nonce
        ciphertext, tag = datacipher.encrypt_and_digest(message)
        cfp.write(nonce)
        cfp.write(tag)
        cfp.write(ciphertext)
        datacipher = AES.new(sessionstr, AES.MODE_EAX)
        message = mfp.read(size)
    mfp.close()
    cfp.close()
    os.remove(filepath)
    end = time.clock()#print("spent time is %f" % (start-end)


def FileDecrypt(filepath, password=defaultpassword, private_key=defaultpath + "/private_key.bin"):
    """
    return 1 : import private key error
    return 2 : AES verify tag error

    """
    dstfiledir = GetFileDir(filepath)
    filename = GetFileName(filepath)
    dir = GetFileDir(filepath)
    updateMap(dir, filename, "D")
    try:
        private_key_data = RSA.importKey(open(private_key).read(), passphrase=password)
        cfp = open(filepath, "rb")
        sessionkey = cfp.read(256)  #private_key_data.size_in_bytes())
        filenamekey = cfp.read(256)
        cipher = PKCS1_OAEP.new(private_key_data)
        sessionstr = cipher.decrypt(sessionkey)
        filename = cipher.decrypt(filenamekey)
        dstfilepath = dstfiledir + "/" + str(filename.decode("utf-8"))
        mfp = open(dstfilepath, "wb")
        # ciphertext = nonce + tag + cipher  ,  len(nonce) = len(tag) = 32
        ciphertext = cfp.read(size + 32)
        while ciphertext:
            nonce = ciphertext[0:16]
            tag = ciphertext[16:32]
            cipher = AES.new(sessionstr, AES.MODE_EAX, nonce=nonce)
            try:
                message = cipher.decrypt_and_verify(ciphertext[32:], tag)
            except ValueError as e:
                messagebox.showinfo("error", e)
                return 1
            #message = cipher.decrypt(ciphertext[32:])
            mfp.write(message)
            ciphertext = cfp.read(size + 32)
        cfp.close()
        mfp.close()
        os.remove(filepath)
    except (ValueError, IndexError, TypeError) as e:
        messagebox.showinfo("error", "invalid password or private key")
        return 1
    except OSError as e:
        messagebox.showinfo("error", e)
        return 1


def FileNameSha256(filepath):
    try:
        f = open(filepath, "rb")
        size = 10240
        data = f.read(size)
        m = sha256()
        while data:
            m.update(data)
            data = f.read(size)
        f.close()
    except OSError as e:
        messagebox("error", e)
    return m.hexdigest()


def GetFileName(filepath):
    return filepath.split('/')[-1]


def GetFileDir(filepath):
    pattern = filepath.split('/')[-1]
    dirlen = len(filepath) - len(pattern) - 1
    dir = filepath[:dirlen]
    return dir

if __name__ == "__main__":
    #_RSAKeyGen()
   # print(FileNameSha256("E:\\迅雷下载\\download"))
    dir1 = r"C:/Users/young/Desktop/a6ed0c785d4590bc95c216bcf514384eee6765b1c2b732d0b0a1ad7e14d3204a"
    dir2 = r"C:/users/young/desktop/teset/"+str(sha256("1.txt".encode("utf-8")).hexdigest())
    FileDecrypt(dir1)
