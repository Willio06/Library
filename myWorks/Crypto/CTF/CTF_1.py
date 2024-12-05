#!/usr/bin/env python3
import sys, requests, re, hashlib
import numpy as np
import random
import string
from functools import reduce
import math
from scipy.linalg import inv
import csv
from sympy import Matrix

hashlen = 5

url, auth = 'http://131.155.23.143:8803', ('tuurwillio', 'ilovecrypto')
sid, token = 20242009, 'cb903bf53b72447b6c7577a586fb30dfb2e04983'

sha = lambda m: int(hashlib.sha256((str(sid) + m).encode()).hexdigest()[:2*hashlen],16)

req = requests.Session()
req.cookies['token'] = token

r = req.get(url+'/', auth=auth)
n = int(re.search('n = ([0-9]+)', r.text).groups()[0])
e = int(re.search('e = ([0-9]+)', r.text).groups()[0])

def sign(m):
    r = req.post(url+'/sign', auth=auth, data={'msg': m})
    return int(r.text)

def validate(m, s):
    return pow(s, e, n) == sha(m)

def forgery(m, s):  # use this to submit your forgery once you've created it
    assert validate(m, s)
    r = req.post(url+'/validate_forgery', auth=auth, data={'msg': m, 'sig': str(s)})
    print('\x1b[32m{}\x1b[0m'.format(r.text.strip()))

def get_primes(a,b, oldprimes):
    primes = oldprimes
    for possiblePrime in range(a+1, b+1):
        # Assume number is prime until shown it is not. 
        isPrime = True
        for num in primes:
            if possiblePrime % num == 0:
                isPrime = False
                break
        
        if isPrime:
            primes.append(possiblePrime)
    return primes

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
def is_prime(x):
    if x < 2:
        return False
    for i in range(2, math.isqrt(x) + 1):
        if x % i == 0:
            return False
    return True
def factors(n):
    prime_factor_list = []
    # Handle factor 2 separately
    while n % 2 == 0:
        prime_factor_list.append(2)
        n //= 2
    # Now n is odd, we can skip even numbers (i.e., start from 3 and step by 2)
    for i in range(3, math.isqrt(n) + 1, 2):
        while n % i == 0:
            prime_factor_list.append(i)
            n //= i
    # If n is still greater than 2, then it must be prime
    if n > 2:
        prime_factor_list.append(n)
    return list(set(prime_factor_list))

def get_exponents(n, primes):
    exponents = []
    for p in primes:
        count = 0
        while n % p == 0:
            n //= p
            count += 1
        exponents.append(count%e)
    return exponents


def solve_modular_system(A, b, e):
    # Convert inputs to numpy arrays
    # Solve the system modulo eµ
    if( np.linalg.matrix_rank(A)!=len(get_primes(1,200,[]))):
        print(np.linalg.matrix_rank(A))
        raise ValueError("not invertible")

    M = Matrix(A)  # Use sympy Matrix for modular inverse
    A_inv_mod_e = M.inv_mod(e)  # Compute modular inverse of A mod e

    # Convert sympy Matrix back to numpy array
    A_inv_mod_e = np.array(A_inv_mod_e).astype(int)

    # Compute x mod e
    x_mod_e = np.mod((A_inv_mod_e @ b),e)
    x_mod_e = np.array(x_mod_e).flatten()

    # Compute residue vector r
    r = (b-np.dot(A, x_mod_e)) // e
    return x_mod_e,r
def check_linear_independence(A, v):
    if A.shape[0] != len(v):
        raise ValueError("The number of rows in A must match the length of v.")
    rank = np.linalg.matrix_rank(A % e)
    if rank != min(A.shape):
        raise ValueError("Matrix A is not full rank modulo e.")
    # Augmented matrix [A|v]
    augmented_matrix = np.column_stack((A, v))
    
    # Compute ranks
    rank_A = np.linalg.matrix_rank(A)
    rank_augmented = np.linalg.matrix_rank(augmented_matrix)
    
    # Compare ranks
    return bool(rank_A != rank_augmented)
def main():
    Messages ={}
    Primes = get_primes(1,200,[])
    k=99731
    # i=0
    # while len(Messages)<len(Primes):
    #     k+=1
    #     mess = str(k)
    #     hashedM = sha(mess)
    #     if(all(np.array(factors(hashedM))<200)):
    #         Messages[mess] = hashedM
    #         if(i==0):
    #             A = np.array(get_exponents(hashedM, Primes))
    #             A = A[:,None]
    #         else:
    #             v=np.array(get_exponents(hashedM, Primes))
    #             if(check_linear_independence(A,v)):
    #                 A = np.hstack((A,v[:,None]))
    #         i+=1
    #         print("#messages: "+str(len(Messages)) + "     vs #primes: "+str(len(Primes)))
    # print(Messages)

    Messages = {'3925': 793912605625, '8297': 669293644851, '8664': 6120202572, '9585': 539769369960, '14071': 103980097920, '14489': 757924721638, '15074': 297767330560, '16106': 11366918374, '19063': 32819356640, '19612': 612277191511, '20316': 85283580096, '22517': 327625566147, '24434': 297124186425, '24571': 307675322253, '25412': 142906173039, '29797': 1081959027534, '31948': 1001825231792, '33536': 621344352200, '35218': 700135030000, '44277': 87870433000, '44694': 211577708433, '44703': 497328435800, '44801': 109743858785, '49242': 347235471440, '49591': 1088905368320, '49626': 648677907025, '52842': 112806158256, '54146': 304067585124, '56503': 402166535680, '56713': 143077000430, '60582': 1103124475, '61814': 227705741050, '62298': 306847836900, '63171': 67301466700, '64842': 316961205141, '67237': 21366577950, '70459': 822036648048, '76317': 377604890460, '76908': 422394970525, '78025': 286511289241, '80281': 1606876370, '84771': 467427640383, '85939': 710742403917, '89207': 7987388800, '92206': 126850800510, '94544': 131190477275}
    A = np.zeros((len(Primes),len(Primes)))
    for i in range(len(Messages.keys())):
        key = list(Messages.keys())[i]
        A[:,i] = get_exponents(sha(key),Primes)
    
    MT = "99732"
    print("finding final message")
    while not all(np.isin(np.array(factors(sha(MT))),np.array(list(Primes)))):
        k+=1
        MT = str(k)
    print("message found: "+MT)
    b = np.array(get_exponents(sha(MT), Primes))
    x,r = solve_modular_system(A,b,e)
    print("b=Ax+eR   test: "+str(np.array_equal(b,np.mod(A@x+e*r,n))))
    assert np.array_equal(np.mod(A @ x, e), np.mod(b, e))
    assert np.array_equal(A @ x, b-e*r)

    prod1 = 1
    for prime, power in zip(Primes, r):
        prod1 = (prod1 * pow(prime, int(power), n)) % n
    
    signs = np.array([sign(mes) for mes in Messages.keys()])
    
    prod2=1
    for sn, power in zip(signs, x):
        prod2 = (prod2 * pow(sn, int(power), n)) % n
    
    KEY = (prod1*prod2)%n
    if(validate(MT,KEY)):
        forgery(MT,KEY)
    else:
        print("wrong key, whyyyyyyyyyyyyyyyyyyyy")

if __name__ == "__main__":
    main()
