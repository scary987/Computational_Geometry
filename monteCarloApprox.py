from collections import namedtuple
import random
import math
from fastFail import *
import tripy
import matplotlib.pyplot as plt

#plt.scatter(3, 9, s=1000)

    # Set chart title.
plt.title("RandomNumbers", fontsize=19)

    # Set x axis label.
plt.xlabel("X", fontsize=10)

    # Set y axis label.
plt.ylabel("Y", fontsize=10)

    # Set size of tick labels.
plt.tick_params(axis='both', which='major', labelsize=9)

    # Display the plot in the matplotlib's viewer.


def tplToPoint(l):
    return Point(l[0],l[1])


def Area(polygon):
    sum = 0
    for i in range(len(polygon)-1):
        sum = sum + (polygon[i].y+polygon[i+1].y)*(polygon[i].x-polygon[i+1].x)

    sum = sum + (polygon[-1].y+polygon[0].y)*(polygon[-1].x-polygon[0].x)
    return sum/2

#generates a uniform random point in a Triangle 
def randomPointonTriangle( Triangle):
    r1 = random.random()
    r2 = random.random()
    while r1+r2 >1:
        r1 = random.random()
        r2 = random.random()
    #vector u and v 
    u =Point(Triangle[1].x-Triangle[0].x,Triangle[1].y-Triangle[0].y)
    v =Point(Triangle[2].x-Triangle[0].x,Triangle[2].y-Triangle[0].y)
    vX = u.x*r1+ v.x*r2
    vY = u.y*r1 + v.y*r2
    #vY *= -1
    return Point(vX,vY)

def PointOnPolygon(polygon1,point):
    polygon = polygon1
    last = polygon[-1]
    current = polygon[0]
    polygon.append(current)
    polygon.pop(0)
    trueIntersections = 0
    while(polygon):
        if last.y != current.y:
            t = ((point.y-last.y)/(current.y-last.y))
            if ((t==1) and (point.x <current.x) and ( (last.y-point.y)*(polygon[0].y-point.y) )<0):
                trueIntersections +=1
            if (0<t) and (t <1) and (point.x < t * current.x+ (1-t)*last.x):
                trueIntersections +=1 
        last = current
        current = polygon[0]
        polygon.pop(0)
    # if cuts are odd, point lies on polygon
    if trueIntersections%2 == 1:
        print(f"{point} lies on polygon")
        return True
    return trueIntersections%2 == 1 

#naive version of taking any point in 2d
def generateRandomPoint(mmax=0):
    vX = random.random()*math.inf
    vY = random.random()*math.inf
    if mmax:
        vX = random.random()*mmax
        vY = random.random()*mmax
    signs = [-1,1]
    return Point(vX*random.choice(signs),vY*random.choice(signs))

def MCI_christian(M, Function,mmax= 0):
    areaM = Area(M)
    n = 1   #number of iterations
    sum = 0 
    integral = 0
    lastintegral =-1
    points = []
    while lastintegral != integral and n<=100000: 
        point =generateRandomPoint(mmax=mmax)
        #print(f"in function: {polygon}")
        if PointOnPolygon(M.copy(),point):
            sum += Function(point)
            lastintegral = integral
            integral = areaM/n *sum
            print(f"iteration: {n}: {integral}")
            n+=1
            points.append(point)
        else:
            print(f"not on point {n}")
    
    return integral



def MCI (M, Function):
    areaM = Area(M)
    Triangulation = [[tplToPoint(tpl) for tpl in triangle]for triangle in tripy.earclip(M)]
    #print(Triangulation)
    #exit()
    probs = []
    probs = [Area(triangle) for triangle in Triangulation]
    areaM =sum(probs)
    probs = [prob/areaM for prob in probs]
    for i in range(1,len(probs)):
        probs[i]+=probs[i-1]
    #actual area, as the loop above represents more of a work around a bug
    areaM = Area(M)
    print(probs)
    points  = []
    n = 1   #number of iterations
    sumM = 0 
    integral = 0
    lastintegral =-1
    while lastintegral!=integral and n<=100000 :
        randomNum = random.random()
        i = 0
        try:
            
            while probs[i]<randomNum:
                print(probs[i],randomNum)
                i+=1
        except:
            print(i,len(probs))
            exit()

        print(len(probs),i)
        randomPoint = randomPointonTriangle(Triangulation[i])
        points.append(randomPoint)
        #pure debugging purposes
        
        """if not PointOnPolygon(M.copy(),randomPoint):
            print("Falsely Generated Point")
            if not PointOnPolygon(list(Triangulation[i].copy()),randomPoint):
                print("point not on triangle eigher",randomPoint)
                exit()
             continue
        """
        sumM += Function(randomPoint)
        lastintegral = integral
        integral = areaM/n *sumM
        print(f"iteration: {n}: {integral}")
        n+=1

    #plt.scatter([p.x for p in points],[p.y for p in points])
    #plt.show()
    return integral

#does not work properly, replaced by external implementation

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
def f3(P):
    return P.x

if __name__ == "__main__":

    """
    Christians Test
    """
    #ax = plt.subplot(3,1,1)
    #plt.plot()
    polygon = [Point(0,0),Point(1,0),Point(1,1),Point(0,1)]
    meins = MCI(polygon, f2)          #width of the square 
    seins = MCI_christian(polygon, f2,mmax =1.5)
    print(meins,seins)
    #MCI(polygon, f2)
    #plt.show()
    #MCI_christian(polygon,f2, mmax =1 )
    #exit(0)

    """
    My Tests
    """
    #exit()
    listofPoints = random_points(1000,50000,50000)
    convexHull = GrahamScan(listofPoints)
    ax = plt.subplot(2,1,1)
    ax.scatter([p.x for p in convexHull],[p.y for p in convexHull], color='#33cc33')
    ax.scatter([p.x for p in listofPoints],[p.y for p in listofPoints], color='#6699cc')
    ax.scatter([p.x for p in convexHull],[p.y for p in convexHull], color='#33cc33')
    ax.scatter(convexHull[0].x,convexHull[0].y, color='#0000ff')
    #plt.plot()
    #plt.subplot(2,1,2)
    #MCI(convexHull, f3)
    #plt.plot 
    plt.show()