# --*coding:utf-8--*--

import tkinter as tk
from FileHandler import *
from tkinter import *
from tkinter import filedialog, scrolledtext
from retrieve import retrieve
import re


class UIframe():
    def __init__(self, root):
        self.root = root
        self.root.maxsize(580, 600)
        self.root.geometry("580x600")
        self.root.title("software engineering")

        # menu attributes
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="打开文件", command=self.__getfilepath)
        self.filemenu.add_command(label="打开目录", command=self.__getdirpath)
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.root.config(menu=self.menubar)

        # button attributes
        self.passwordbutton = Button(self.root, text='确定', bd=0, command=self.__getpassword)
        self.publickeypathbutton = Button(self.root, text='选择公钥文件路径', bd=0, command=self.__getpublickey)
        self.privatekeypathbutton = Button(self.root, text='选择私钥文件路径', bd=0, command=self.__getprivatekey)
        self.encryptbutton = Button(self.root, text='加密', bd=0, command=self.__encrypt)
        self.decrypbutton = Button(self.root, text='解密', bd=0, command=self.__decrypt)
        self.searchbutton = Button(self.root, text="开始搜索", bd=0, command=self.__search)

        # textbox attributes and initialize them with None
        self.pathtextbox = None
        self.publickeypathtextbox = None
        self.privatekeypathtextbox = None
        self.passwordtextbox = None
        self.searchtextbox = None

        # textbox variety
        self.pathvar = StringVar()
        self.publickeypathvar = StringVar()
        self.privatekeypathvar = StringVar()
        self.passwordvar = StringVar()
        self.keywordsvar = StringVar()
        self.scrolltextvar = StringVar

        # label string attributes
        self.pathlabel = "已选择的路径"
        self.privatekeypathlabel = "私钥证书路径"
        self.publickeypathlabel = "公钥证书路径"
        self.passwordlabel = "密码"
        self.searchlabel = "文件搜索"

        self.scr = scrolledtext.ScrolledText(self.root, width=78, height=30, wrap=tk.WORD)  # wrap=tk.WORD   这个值表示在行的末尾如果有一个单词跨行，会将该单词放到下一行显示,比如输入hello，he在第一行的行尾,llo在第二行的行首, 这时如果wrap=tk.WORD，则表示会将 hello 这个单词挪到下一行行首显示, wrap默认的值为tk.CHAR
        self.scr.grid(column=0, columnspan=3)
        self.scr.place(x=10, y=200)

        self.__pathtextbox(y=1)
        self.__publickeytextbox(y=23)
        self.__privatekeytextbox(y=45)
        self.__passwordtextbox(y=67)
        self.__searchtextbox(y=120)

        self.__publickeypathbutton(y=23)
        self.__privatekeypathbutton(y=45)
        self.__passwordbuttonposition(y=67)
        self.__encryptbutton(y=89)
        self.__decryptbutton(y=89)
        self.__searchbutton(y=120)

        self.root.mainloop()

    def initlabelstr(self, x, y, labelstr):
        var = StringVar()
        var.set(labelstr)
        pathlabel = Label(self.root, textvariable=var)
        pathlabel.pack(padx=10, pady=15, side="left")
        pathlabel.place(x=x, y=y)

    def __encrypt(self):
        path = self.pathvar.get()
        password = self.passwordvar.get()
        publickey = self.publickeypathvar.get()
        Encrypt(path, key=password, publickey=publickey)

    def __decrypt(self):
        path = self.pathvar.get()
        password = self.passwordvar.get()
        privatekey = self.privatekeypathvar.get()
        Decrypt(path, key=password, privatekey=privatekey)

    def __search(self):
        self.scr.delete(1.0, END)
        keywords = self.keywordsvar.get()
        dirpath = self.pathvar.get()
        if not os.path.isdir(dirpath):
            messagebox.showinfo("implicate", dirpath + " is not a directory, please choose a directory.")
            return
        result = retrieve(dirpath, keywords)
        if result:
            self.scr.insert("insert", result)
        else:
            messagebox.showinfo("result", "Nothing to be found.")

    def __dirpath(self):
        dirpath = filedialog.askdirectory()
        return dirpath

    def __filepath(self):
        filespath = filedialog.askopenfilename()
        return filespath

    def __getfilepath(self):
        self.pathvar.set(self.__filepath())

    def __getdirpath(self):
        self.pathvar.set(self.__dirpath())

    def __getpassword(self):
        self.passwordvar.set(self.__filepath())

    def __getpublickey(self):
        self.publickeypathvar.set(self.__filepath())


    def __getprivatekey(self):
        self.privatekeypathvar.set(self.__filepath())

    def __passwordbuttonposition(self, x=460, y=22):
        self.passwordbutton.pack()
        self.passwordbutton.place(x=x, y=y)

    def __publickeypathbutton(self, x=460, y=43):
        self.publickeypathbutton.pack()
        self.publickeypathbutton.place(x=x, y=y)

    def __privatekeypathbutton(self, x=460, y=64):
        self.privatekeypathbutton.pack()
        self.privatekeypathbutton.place(x=x, y=y)

    def __decryptbutton(self, x=460, y=79):
        self.decrypbutton.pack()
        self.decrypbutton.place(x=250, y=y)

    def __encryptbutton(self, x=460, y=79):
        self.encryptbutton.pack()
        self.encryptbutton.place(x=300, y=y)

    def __searchbutton(self, x=460, y=115):
        self.searchbutton.pack()
        self.searchbutton.place(x=x, y=y)

    def __pathtextbox(self, x=10, y=1):
        self.initlabelstr(x, y, self.pathlabel)
        self.pathtextbox = Entry(self.root, width=50, textvariable=self.pathvar)
        self.pathtextbox.pack(padx=100, pady=200, side="left")
        self.pathtextbox.place(x=100, y=y)

    def __publickeytextbox(self, x=10, y=22):
        self.publickeypathvar.set("C:/software/public_key.pem")
        self.initlabelstr(x, y, self.publickeypathlabel)
        self.publickeypathtextbox = Entry(self.root, width=50, textvariable=self.publickeypathvar)
        self.publickeypathtextbox.pack(padx=100, pady=200, side="left")
        self.publickeypathtextbox.place(x=100, y=y)

    def __privatekeytextbox(self, x=10, y=43):
        self.privatekeypathvar.set("C:/software/private_key.bin")
        self.initlabelstr(x, y, self.privatekeypathlabel)
        self.privatekeypathtextbox = Entry(self.root, width=50, textvariable=self.privatekeypathvar)
        self.privatekeypathtextbox.pack(padx=100, pady=200, side="left")
        self.privatekeypathtextbox.place(x=100, y=y)

    def __passwordtextbox(self, x=10, y=64):
        self.passwordvar.set("nooneknows")
        self.initlabelstr(x, y, self.passwordlabel)
        self.passwordtextbox = Entry(self.root, width=50, textvariable=self.passwordvar)
        self.passwordtextbox.pack(padx=100, pady=200, side="left")
        self.passwordtextbox.place(x=100, y=y)
        self.passwordtextbox["show"] = "*"

    def __searchtextbox(self, x=10, y=115):
        self.initlabelstr(x, y, self.searchlabel)
        self.searchtextbox = Entry(self.root, width=50, textvariable=self.keywordsvar)
        self.searchtextbox.pack(side="left")
        self.searchtextbox.place(x=100, y=y)






if __name__ == "__main__":
    root = Tk()
    instance = UIframe(root)



