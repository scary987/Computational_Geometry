from collections import namedtuple
import random
import math
Point = namedtuple('Point','x y')

"""
points as  named tuple
"""

def random_points(k, xMax, yMax,seed= 0):
    if seed:
        random.seed(seed)
    l = []
    for _ in range(k):
        x= random.random()*xMax
        if random.randint(0,1)==1:
            x*=-1
        y = random.random()*yMax
        if random.randint(0,1)==1:
            y*=-1
        l.append(Point(x,y))
    return l

def getAngle(p1,p2):
    return math.atan2( (p2.y-p1.y),(p2.x-p1.x) )

def isLeft(A,B, C):
    return ( (B.x-A.x)*(C.y-A.y)-(C.x-A.x)*(B.y-A.y) > 0) #Helperfunction T(A,B,C) https://de.wikipedia.org/wiki/Graham_Scan#Vorbereitung


def GrahamScan(listofPoints):
    #listofPoints.sort(key=lambda p: p.y) #sort by y value (Height)
    print(listofPoints,"before sorting")
    key_min = 0
    for i in range(len(listofPoints)):
        if listofPoints[i].x < listofPoints[key_min].x:
            key_min = i
    listofPoints[0],listofPoints[key_min] = listofPoints[key_min],listofPoints[0] #this actually works(), was looking for a built in python, wow thanks https://www.geeksforgeeks.org/python-program-to-swap-two-elements-in-a-list/
    
    listofPoints[1:].sort(key=lambda p: getAngle(listofPoints[0],p)) #sort rest by angle compared to first value
    print(listofPoints,"after sorting")

    stack = []
    stack.extend(listofPoints[:2])
    i = len(stack)
    print(i,stack)

    while i < len(listofPoints):
        if( isLeft(stack[-2],stack[-1],listofPoints[i])):
            print("IsLeft")
            stack.append(listofPoints[i])
            i+=1
            continue
        elif len(stack)==2:
            print("stack smol")
            stack.append(listofPoints[i])
            i+=1
            continue
        else:
            print("bad point")
            stack.pop(-1)
    
    #print("="*20,"\nDone\n",stack,"\n","="*20)
    print(len(listofPoints),len(stack))
    return stack

#https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
"""
if q lies on segment between p and r
"""

#note: only works if give segments are already colinear, because this just checks the square
def onSegment(p,q,r):
    if (q.x<=max(p.x,r.x) and q.x >= min(p.x, r.x) and q.y <= max(p.y,r.y) and q.y>=min(p.y,r.y)):
        return True
    return False

def orientation(p,q,r):
    val = (q.y-p.y) *(r.x-q.x) - (q.x-p.x) * (r.y - q.y)
    if (val == 0): #is colinear  
        return 0 
    elif val>0: #positive 
        return 1
    else:       #negative
        return 2

"""
The main function that returns true if line segment 'p1q1'  and 'p2q2' intersect. 
"""

def doIntersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2 , q1)

    #general case
    if (o1 != o2 ) and (o3 != o4):
        return True
    if(o1 == 0 and onSegment(p1, p2, q1)):
        return True
    if(o2 == 0 and onSegment(p1, q2, q1)):
        return True
    if(o3 == 0 and onSegment(p2, q1, q2)):
        return True
    if(o4 == 0 and onSegment(p2, q1, q2)):
        return True
    return False

def fastFail(segment,listofPoints):

    convexHull = GrahamScan(listofPoints)
    s1,s2 = segment
    i = 0
    if doIntersect(convexHull[0],convexHull[-1],s1,s2):
        print("Failed very fast:",-1)
        return False
    while i< len(convexHull)-1:
        print(i)
        if doIntersect(convexHull[i],convexHull[i+1],s1,s2):
            print("Failed fast:",i)
            return False
        i+=1
    print("Didn't Fail lmao")
    return True

    




if __name__ == '__main__':
    seed = random.randint(1,10000000000000000000)
    listofPoints = random_points(1000,500,500,seed)
    fastFail((Point(-1,-1),Point(-2,-2)),listofPoints)
    s1,s2 = tuple (random_points(2,500,500))
    fastFail((s1,s2),listofPoints )
    #convexHull =GrahamScan(listofPoints)
    #sprint(len(listofPoints),len(convexHull))

    