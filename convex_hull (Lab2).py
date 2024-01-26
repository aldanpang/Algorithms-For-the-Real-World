import matplotlib.pyplot as plt
import time
import random


# function that checks if three points a,b,c are clockwise positioned, ACCEPTS [X,Y] ONLY
def is_clockwise(a,b,c):
    if ((c[1] - a[1]) * (b[0] - a[0])) < ((b[1] - a[1]) * (c[0] - a[0])): # if (cy − ay) ∗ (bx − ax) < (by − ay) ∗ (cx − ax)
        return True # in clockwise order
    else:
        return False # in not clockwise order 

# compute with naive method the convex hull of the points cloud pts     
# and store it as a list of vectors
# NOTE: pts comprises of sublists - ie. pts = [[4,5], [1,2], [3,4]]

def convex_hull_2d_gift_wrapping(pts):
    
    # leftPoint = 0 # index of leftmost point 
    # startingIndex = 0
    # leftPoint = 0
    # for i in range(1, len(pts)):
    #     if pts[i][0] < pts[leftPoint][0]: # iterate through each sublist. if i'th x value is smaller than min's x value, update min with i 
    #         leftPoint = i # since i'th x value is smaller than min's x value, we update min
    #     elif pts[i][0] == pts[leftPoint][0]: # but if i'th x value  = min's x value, we tie break by checking y value
    #         if pts[i][1] > pts[leftPoint][1]: # leftmost point is higher y value
    #             leftPoint = i
    # Finding leftmost point
    startPoint = min(pts) # naive method of finding leftmost point, not considering tiebreakers
    convexHull = []
    currentPoint = startPoint
    nextPoint = None
    
    while nextPoint != startPoint:
        convexHull.append(currentPoint) # adding left point as first hull point
        nextPoint = pts[0]
        for i in pts[1:]:
            if nextPoint == currentPoint or is_clockwise(currentPoint, nextPoint, i ):
                nextPoint = i
        
        currentPoint = nextPoint 
                    
    return convexHull        
    
    ###############################
    ## ATTEMPT NUMBER 5000 BELOW ##
    ###############################
    
    #1) Initialize p as leftmost point.
    #2) Do following while we do not come back to the first (or leftmost) point.
        #a) The next point q is the point such that the triplet (p, q, r) is counterclockwise for any other point r.
        #b) next[p] = q (Store q as next of p in the output convex hull).
        #c) p = q (Set p as q for next iteration).

    # convexHull = [leftPoint] # adding first point into hull
    # print(convexHull)
    # counter = 0
    # endPoint = 0
    # print(endPoint)
    
    # while endPoint != convexHull[0]:
    #     endPoint = pts[0] # initial endpoint for line (l, p)
        
    #     for i in range(len(pts)):
    #         if endPoint == leftPoint or is_clockwise(convexHull[counter], endPoint, pts[i]) == False: # if haven't reached the end and is clockwise, update endpoint
    #             endPoint = pts[i]
        
    #     counter += 1
    #     leftPoint = endPoint
    
    # pts = convexHull
    # return [pts]

# compute with divide and conquer method the convex hull of the points  
# cloud pts and store it as a list of vectors
def convex_hull_2d_divide_conquer(pts):
    
    # if len(left) <= 4: #base case
    #     convex_hull_2d_gift_wrapping(left)
    #     # probably need to return solved left
        
    # elif len(right) < 4:
    #     convex_hull_2d_gift_wrapping(right)
    #     # same thing, prob need return solved right
    
    # mid = len(pts)//2  
    # left = convex_hull_2d_divide_conquer(pts[0:mid]) # divides into halves
    # right = convex_hull_2d_divide_conquer(pts[mid:])
        
    return [pts[0]]

NUMBER_OF_POINTS = 20

# generate random points and sort them according to x coordinate
pts = []
for i in range(NUMBER_OF_POINTS): pts.append([random.random(),random.random()]) 
pts = sorted(pts, key=lambda x: x[0])

# compute the convex hulls
print("Computing convex hull using gift wrapping technique ... ",end="")
t = time.time()
hull_gift_wrapping = convex_hull_2d_gift_wrapping(pts)
print("done ! It took ",time.time() - t," seconds")

print("Computing convex hull using divide and conquer technique ... ",end="")
t = time.time()
hull_divide_conquer = convex_hull_2d_divide_conquer(pts)
print("done ! It took ",time.time() - t," seconds")

# close the convex hull for display
hull_gift_wrapping.append(hull_gift_wrapping[0])
hull_divide_conquer.append(hull_divide_conquer[0])

# display the convex hulls
if NUMBER_OF_POINTS<1000:
    fig = plt.figure()
    ax = fig.add_subplot(131)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    ax.title.set_text('Points')
    ax = fig.add_subplot(132)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    ax.plot([x[0] for x in hull_gift_wrapping], [x[1] for x in hull_gift_wrapping], "ro--")
    ax.title.set_text('Gift Wrapping')
    ax = fig.add_subplot(133)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    ax.plot([x[0] for x in hull_divide_conquer], [x[1] for x in hull_divide_conquer], "ro--")
    ax.title.set_text('Divide/Conquer')
    plt.show(block=False)

