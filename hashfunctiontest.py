import hashlib
from random import randint
import time
import matplotlib.pyplot as plt
import numpy as np

def blake2b(key):
    b = hashlib.blake2b()
    b.update(key.encode())
    return int(b.hexdigest(),16) % 2**128

def hashfunction(key):
    key = str(key)
    sum1 = 0
    for i in range(len(key)):
        sum1 += sum1 + ord(key[i]) * (32 * i + 1)
    return sum1*(2**127-1) % 2**128

def blakeDiffTest(n,key):
    binkey = bin(key)
    diffusion = list()
    # Diffusion test
    for i in range(n):
        # Flip one random bit from the hashkey.
        listkey = list(str(binkey))
        changedindex = randint(2,len(binkey)-1)
        if(listkey[changedindex] == '0'):
            listkey[changedindex] = '1'
        elif(listkey[changedindex] == '1'):
            listkey[changedindex] = '0'
        flipkey = str(int(''.join(listkey),2))

        # Creates hashes
        blakeflip = bin(blake2b(flipkey))
        blakenorm = bin(blake2b(str(key)))

        # Compares hashes
        flipcount = 0
        count = 0
        try:
            for i in range(2,len(str(blakenorm))):
                if(str(blakenorm)[i]!=str(blakeflip)[i]):
                    flipcount+=1
                count += 1
            diffusion.append(flipcount/count)
        except IndexError:
            pass

    return(sum(diffusion)/len(diffusion))

def hashfuncDiffTest(n,key):
    binkey = bin(key)
    diffusion = list()
    # Diffusion test
    for i in range(n):
        # Flip one random bit from the hashkey.
        listkey = list(str(binkey))
        changedindex = randint(2,len(binkey)-1)
        if(listkey[changedindex] == '0'):
            listkey[changedindex] = '1'
        elif(listkey[changedindex] == '1'):
            listkey[changedindex] = '0'
        flipkey = str(int(''.join(listkey),2))

        # Creates hashes
        hashflip = bin(hashfunction(flipkey))
        hashnorm = bin(hashfunction(str(key)))

        # Compares hashes
        flipcount = 0
        count = 0
        try:
            for i in range(2,len(str(hashnorm))):
                if(str(hashnorm)[i]!=str(hashflip)[i]):
                    flipcount+=1
                count += 1
            diffusion.append(flipcount/count)
        except IndexError:
            pass
    return(sum(diffusion)/len(diffusion))

def blakeSpreadTest(size):
    # Creates list with size amount of 0:s
    li = [0 for x in range(size)]
    
    # Spreads out size amount of hashes over li
    for i in range(size):
        rand = randint(0,2**64)
        index = blake2b(str(rand)) % size
        li[index] += 1
    
    # Checks how many collisions
    zerocount = 0
    for i in li:
        if(i == 0):
            zerocount += 1
    return zerocount
        
def hashfuncSpreadTest(size):
    li = [0 for x in range(size)]
    for i in range(size):
        rand = randint(0,2**64)
        index = hashfunction(str(rand)) % size
        li[index] += 1
    # Checks how many collisions
    zerocount = 0
    for i in li:
        if(i == 0):
            zerocount += 1
    return zerocount
    
def blakeSpeedTest(n):
    start = time.time()
    for i in range(n):
        b = blake2b(str(randint(0,2**127)))
    end = time.time()
    return end-start

def hashfuncSpeedTest(n):
    start = time.time()
    for i in range(n):
        h = hashfunction(str(randint(0,2**127)))
    end = time.time()
    return end-start

def main():
    ns = [10, 20, 40, 80, 160, 320, 640, 1000, 2000, 4000, 8000, 16000, 
          30000, 60000, 120000, 250000, 500000]
    keys = [int("1"*n) for n in range(5,15)]
    t_blake = []
    t_hashf = []
    for i in ns:
        t_blake.append(blakeSpeedTest(i))
        t_hashf.append(hashfuncSpeedTest(i))

    b_blake = []
    b_hashf = []
    for i in keys:
        b_blake.append(blakeDiffTest(100,i))
        b_hashf.append(hashfuncDiffTest(100,i))

    figure1, axis1 = plt.subplots(1, 2, figsize=(12, 5))

    axis1[0].plot(ns, t_blake)
    axis1[0].set_title("Blake2b")
    axis1[0].set_ylabel("Time in seconds")
    axis1[0].set_xlabel("Number of hashes")

    axis1[1].plot(ns, t_hashf)
    axis1[1].set_title("Hashfunction")
    axis1[1].set_ylabel("Time in seconds")
    axis1[1].set_xlabel("Number of hashes")

    plt.tight_layout()

    figure2, axis2 = plt.subplots(1, 2, figsize=(12, 5))
    axis2[0].plot([n for n in range(5,15)],b_blake)
    axis2[0].set_title("Blake2b")
    axis2[0].set_ylabel("Proportion of bitflips")
    axis2[0].set_xlabel("Number of ones in key")

    axis2[1].plot([n for n in range(5,15)],b_hashf)
    axis2[1].set_title("Hashfunction")
    axis2[1].set_ylabel("Proportion of bitflips")
    axis2[1].set_xlabel("Number of ones in key")

    plt.show()

if __name__ == '__main__':
    main()