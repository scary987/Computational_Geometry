from collections import namedtuple
import random
import math
import fastFail
Point = namedtuple('Point','x y')



def Area(polygon):
    sum = 0
    for i in range(len(polygon)):
        sum = sum + (polygon[i][1]+polygon[i+1][1])*(polygon[i][0]-polygon[i+1][0])

    sum = sum + (polygon[-1][1]+polygon[0][1])*(polygon[-1][0]-polygon[0][0])
    return sum/20


def randomPointonTriangle( Triangle):
    x = random.random()
    y = random.random()*(1-x) #0<=x+y <=1

    vX = (Triangle[2]-Triangle[0])*x