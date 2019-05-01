# --*--coding:utf-8--*--
import json
import pprint
import demjson
import os
from hashlib import sha256
from FileHandler import *    #  GetFileDir, GetFileName, defaultpath
from tkinter import messagebox

global map
map = {}

def updateMap(dirpath, filename, mode):
    map = {}
    jsonpath = dirpath + "/sha256data.json"
    if mode == "E":
        map = getMap(filename)
        if not os.path.exists(jsonpath):
            try:
                f = open(jsonpath, "w")
                json.dump(map, f)
                f.close()
            except IOError:
                pass
        else:
            try:
                f = open(jsonpath, "r")
                originalmap = json.load(f)
                originalmap.update(map)
                f.close()
                f = open(jsonpath, "w")
                json.dump(originalmap, f)
                f.close()
            except IOError:
                pass
    elif mode == "D":
        try:
            f = open(jsonpath, "r")
            map = json.load(f)
            try:
                map.pop(filename)
            except KeyError:
                pass
            f.close()
            f = open(jsonpath, "w")
            json.dump(map, f)
            f.close()
        except IOError:
            pass
    else:
        messagebox.showinfo("implicate", "please specific mode!")
        return



def getMap(filename):
    """
    dir act as a key
    sha256 of string act as a key
    sha256 of each byte and following its in the string act as a value set

    """
    map = {}
    values = []
    key = sha256(filename.encode("utf-8")).hexdigest()
    for i in range(len(filename)-1):
        digest = sha256(filename[i:i+2].encode("utf-8")).hexdigest()
        values.append(digest)
    map[str(key)] = list(set(values))
    return map


def retrieve(dirpath, string):
    if string == "":
        return ""
    keys = []
    values = []
    jsonpath = dirpath + "/sha256data.json"
    f = open(jsonpath)
    map = json.load(f)
    string = string.split()   # split keys here
    for i in string:
        for j in range(len(i)-1):
            digest = sha256(i[j:j + 2].encode("utf-8")).hexdigest()
            values.append(digest)

    flag = 0
    for key in map:
        temp = len(set(map[key]) & set(values))  # 求交集的长度
        if flag < temp:
            flag = temp
            keys.clear()
            keys.append(key)
        elif flag == temp:
            keys.append(key)
    return keys

if __name__ == "__main__":
    _getMap("西安电子科技大学python")
    _getMap("成都电子科技大学php")
    _getMap("网络与信息安全电子专业")
    _dumpMap()
    print(retrieve("电子"))