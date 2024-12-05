#!/usr/bin/env python3
import sys, requests, re, random, os
import numpy as np
import random
import string
from functools import reduce
import math
from scipy.linalg import inv
import csv
from sympy import Matrix

url, auth = 'http://example', ('user', 'pw')
sid, token = 'ID', 'token'

req = requests.Session()
req.cookies['token'] = token

r = req.get(url+'/', auth=auth)
target = bytes.fromhex(re.search('target_hash = ([0-9a-f]+)', r.text).groups()[0])

def hash(x):
    r = req.post(url+'/hash', auth=auth, data={'data': x.hex()})
    return bytes.fromhex(r.text) #in byte strings

def multi_unhash(xs):
    r = req.post(url+'/multi_unhash', auth=auth, data={'hashes': [x.hex() for x in xs]})
    r = r.text.strip().split()
    if r[1] == 'None': return int(r[0]), None  # bad query
    try: 
        return int(r[0]), bytes.fromhex(r[1]) #returns id of preimage and preimg in byte strings
    except:
        print(r)
        return None,None

def preimage(x):  # use this to submit your preimage
    r = req.post(url+'/validate_preimage', auth=auth, data={'data': x.hex()})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

def validate(x):
    if(format(hash(x).hex())==format(target.hex()) and x is not None):
        return True
    return False
################################################################

print('target hash value: {}'.format(target.hex()))
print(target)

# let's compute a few hash values for fun
preimage(b'Hello, 20242009. This is your preimage. Some randomness: 39c8c60036c119edbc31272013cd6fa6')
# Generate random byte string
test = os.urandom(len(target))
k=0
while(not(validate(test))):
    k+=1
    xs = []
    for _ in range(25):

        x = os.urandom(len(target)).hex() #in byte strings
        # print(x)
        # print('string: {}'.format(x.hex()), end = ' ~> ')
        # print('hash: {}'.format(hash(x).hex()))
        xs.append(hash(bytes.fromhex(x)))
    xs[random.randint(0,24)] = target

    inte ,test = multi_unhash(xs)
    if(hash(test)!=target):
        print("NO, found: ",end="")
        print(test,end=" with hash: " )
        print(hash(test))
    if(inte==xs.index(target)):
        print("we got it: ",end="")
        print(test)
        print("ourcheck says: "+str(validate(test)))
    if(k%10==0):
        print("@ loop "+str(k))

