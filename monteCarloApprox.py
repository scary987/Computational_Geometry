from collections import namedtuple
import random
import math
from fastFail import *
import tripy

def tplToPoint(l):
    return Point(l[0],l[1])
def Area(polygon):
    sum = 0
    for i in range(len(polygon)-1):
        sum = sum + (polygon[i].y+polygon[i+1].y)*(polygon[i].x-polygon[i+1].x)

    sum = sum + (polygon[-1].y+polygon[0].y)*(polygon[-1].x-polygon[0].x)
    return sum/2


def randomPointonTriangle( Triangle):
    r1 = random.random()
    r2 = random.random() 

    vX = (1- math.sqrt(r1)*Triangle[0].x+(math.sqrt(1)*(1 - r2)*Triangle[1].x) + (r2*math.sqrt(r1)*Triangle[2].x))
    vY = (1- math.sqrt(r1)*Triangle[0].y+(math.sqrt(1)*(1 - r2)*Triangle[1].y) + (r2*math.sqrt(r1)*Triangle[2].y))
    return Point(vX,vY)

def MCI (M, Function):
    areaM = Area(M)
    Triangulation = [[tplToPoint(tpl) for tpl in triangle]for triangle in tripy.earclip(M)]
    print(Triangulation)
    probs = []
    probs = [Area(triangle)/areaM for triangle in Triangulation]
    for i in range(1,len(probs)):
        probs[i]+=probs[i-1]
    
    print(probs)

    n = 1   #number of iterations
    sum = 0 
    integral = 0
    lastintegral =-1
    while lastintegral!=integral:
        randomNum = random.random()
        i = 0
        while probs[i]<randomNum:
            print(probs[i],randomNum)
            i+=1

        print(len(probs),i)
        randomPoint = randomPointonTriangle(Triangulation[i])
        sum += Function(randomPoint)
        lastintegral = integral
        integral = areaM/n *sum
        print(f"iteration: {n}: {integral}")
        n+=1


def EarCut(polygon):
    triangulation = [polygon]
    print("polygon",polygon)
    if (len(polygon)>3):
        previous = polygon[-1]
        polygon.pop(-1)
        ear = 0
        while(ear == 0):
            #line 6
            polygon.append(previous)
            current = polygon[0]
            #line 7
            polygon.pop(0)
            nextP = polygon[0]
            ear = 1

            while(polygon[0]!= previous):
                segStart = polygon[0]
                polygon.append(segStart)
                polygon.pop(0)
                segEnd = polygon[0]
                """
                a = something [[x,y][x1,y1]]
                """
                a = [Point(segEnd.x-segStart.x,segEnd.y-segStart.y),Point(previous.x-nextP.x,previous.y-nextP.y)]
                b =  Point( previous.x-segStart.x, previous.y-segStart.y )
                #does b lie on segement a = does bb intersect a ?
                """
                solve a*t = b -> t = 
                """
                if(doIntersect(b,b,a[0],a[1])):
                    print("isSegement")
                    ear = 0
                


            polygon.append(previous)
            polygon.pop(0)
            previous = current
            triangle = [polygon[-1], previous, polygon[0]]
            #line 19
            triangulation = [triangle]
            print(triangle)
            triangulation.extend(EarCut(polygon)) #recursive step
    return triangulation

def f1(P):
    return 1

def f2(P): # x^2 
    return P.x**2

if __name__ == "__main__":

    """
    Christians Test
    """

    polygon = [Point(0,0),Point(1,0),Point(1,1),Point(0,1)]
    MCI(polygon, lambda p:1)
    exit(0)

    """
    My Tests
    """

    listofPoints = random_points(1000,500,500,seed)
    convexHull = GrahamScan(listofPoints)