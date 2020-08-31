import Crypto.Util.number
import Crypto
import random
import sys
import time

n=5

def getPrime(k):
    #should return k+1 bit prime
    p=Crypto.Util.number.getPrime(k+1, randfunc=None) #randfunc=Crypto.Random.get_random_bytes
    return p

def SelectG(p,n):
    #should select randomly g1,..,gn from 0,..,p and return that
    g=random.sample(range(2,p),n)
    return g

def HGen(k):
    #should return hash family p,g1,..,gn
    p=getPrime(k)
    g=SelectG(p,n)
    print(p," ",g," ")
    return p,g

def HEval(p,list_g,list_message):
    h=1
    for i in range(len(list_g)):
        h=h*(list_g[i]**(int(list_message[i],2)+1)) ### n exp
    return h

def IncH(p,g,M,h,j,m):
    print(M[j])
    print(int(M[j],2))
    x=h//(g[j]**(int(M[j],2)+1)) ### 1 exp
    y=x*(g[j]**(int(m,2)+1)) ### 1 exp
    return y

def main():
    M=[b'101',b'110',b'101',b'101',b'101']
    p,g = HGen(20)
    h=HEval(p,g,M)
    h1=IncH(p,g,M,h,2,b'111')
    M1=[b'101',b'110',b'111',b'101',b'101']
    h2=HEval(p,g,M1)
    print(h," ")
    print(h1)
    print(h2)

if __name__ == "__main__":
    start = time.process_time()
    main()
    print(time.process_time() - start)