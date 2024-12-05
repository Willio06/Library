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
n = int(re.findall('n = ([0-9]+)', r.text)[0])

def sqrt(x):
    r = req.post(url+'/sqrt', auth=auth, data={'value': x})
    if r.text.strip() == 'None': return None  # not a square
    return int(r.text)

def factorization(p, q):  # use this to submit your factorization
    assert type(p) == type(q) == int
    r = req.post(url+'/validate_factorization', auth=auth, data={'p': '{:d}'.format(p), 'q': '{:d}'.format(q)})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))
def validate(p):
    if(p is not None and n%p==0 and n!=p and p!=1):
        return True
    return False
################################################################

print('n: {}'.format(n))

# let's compute a few square roots for fun

test=1
while(not(validate(test))):
    k=random.randint(0,n-1)
    a= pow(k,2,n)
    x= sqrt(a)
    if(x is not None and x!=k):
        test = math.gcd(x+k,n)
        if(validate(test)):
            print("HEYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY ")
            p=test
            print(int(n/p)==n/p)
            print("P")
            print(p)
            print("Q")
            print(int(n/p))
            print(n==p*(n/p))
            break

    if(k%100==0): print(k)
