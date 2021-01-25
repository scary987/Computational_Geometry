from collections import namedtuple
import math
Vector = namedtuple('Vector','x y') 
Point = namedtuple('Point','x y')


def scalarprod(v1:Vector,v2:Vector):
    return sum([u*v for u,v in zip(v1,v2)])


def absol(v:Vector):
    return math.sqrt(scalarprod(v,v))

def scalarmult(v:Vector, k):
    return Vector._make([e*k for e in v])

def scalardiv(v:Vector, k):
    return scalarmult(v,1/k)

def vector_add(u:Vector, v:Vector):
    return Vector._make([u_i+v_i for u_i,v_i in zip(u,v)])

def vector_sub(u:Vector, v:Vector):
    return Vector._make([u_i-v_i for u_i,v_i in zip(u,v)])

def reduce(u:Vector,v:Vector):
    print(u,v)
    while(absol(u)>absol(v)):
        q = scalarprod(u, scalarmult(v,1/absol(v)**2)) 
        #print(q,scalarmult(v, round(q)))
        w = vector_sub(u,(scalarmult(v, round(q))))
        u = v 
        v = w
        print(u,v)
    return (u,v)


def Gcd(a,b):
    if a<0:
        a = -a
    if b<0:
        b = -b
    print(a,b)
    while(b!=0):
        c = a%b
        a = b
        b = c
        print(a,b)
    return (a,b)
if __name__ == "__main__":
    u =Vector(36,20)
    v = Vector(32,16)
    Gcd (39,12)
    reduce(u,v)