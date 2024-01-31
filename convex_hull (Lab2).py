import matplotlib.pyplot as plt
import time
import random


# function that checks if three points a,b,c are clockwise positioned, ACCEPTS [X,Y] ONLY
def is_clockwise(a,b,c):
    if ((c[1] - a[1]) * (b[0] - a[0])) < ((b[1] - a[1]) * (c[0] - a[0])): # if (cy − ay) ∗ (bx − ax) < (by − ay) ∗ (cx − ax)
        return True # in clockwise order
    else:
        return False # in not clockwise order. note this means that c is a better point for convex hull 

# compute with naive method the convex hull of the points cloud pts     
# and store it as a list of vectors
# NOTE: pts comprises of sublists - ie. pts = [[4,5], [1,2], [3,4]]

def convex_hull_2d_gift_wrapping(pts):
    # Finding leftmost point
    leftPoint = min(pts) # naive method of finding leftmost point, not considering tiebreakers
    convexHull = []
    startPoint = leftPoint
    endPoint = None
    
    while endPoint != leftPoint: # repeats until we reach the first point again
        convexHull.append(startPoint) # appends clockwise points i 
        endPoint = pts[0] 
        #print("added point ", pts.index(startPoint))
        for i in pts[1:]: # for every [x,y] in pts
            #print("next iteration")
            if endPoint == startPoint or is_clockwise(startPoint, endPoint, i ):
                 # if start = end we must update end to the next [x,y]
                 # OR, if i is RHS of line formed by start and endpoint, we just make 
                endPoint = i
                #print("if loop, endPoint value is ", endPoint)
        startPoint = endPoint 
        #print("after for loop, startPoint value is ", startPoint)
                    
    return convexHull      
# return [pts[0]] ?  
    
# compute with divide and conquer method the convex hull of the points  
# cloud pts and store it as a list of vectors
def convex_hull_2d_divide_conquer(pts):
    if len(pts) <= 5: #base case
        print("base case giftwrap", convex_hull_2d_gift_wrapping(pts))
        return convex_hull_2d_gift_wrapping(pts)
        
    mid = len(pts)//2  
    left = pts[:mid] # divides into halves
    right = pts[mid:]
    leftHull = convex_hull_2d_divide_conquer(left) # run divide conquer algorithm recursively until we reach base case and obtain convex hulls of small left and rights
    rightHull = convex_hull_2d_divide_conquer(right)
    print("leftHull", leftHull)
    print("rightHull", rightHull)
    print("max", max(leftHull))
    print("min", min(rightHull))
    
    def merge(leftHull, rightHull):
        rightmostPoint = max(leftHull, key = lambda p: p[0]) # of left hull, returns rightmost point by x coords
        leftmostPoint = min(rightHull, key = lambda p: p[0]) # of right hull, returns leftmost point

       # deriving upper tangent
        for i in rightHull:
            while is_clockwise(rightmostPoint, leftmostPoint, i): # repeat until we reach a point that is a better convex hull
                # otherwise, keep removing unsuitable points until we reach point with better convex hull
                if i in rightHull:
                    rightHull.pop(rightHull.index(i)) # removes clockwise points because it's below line
                    print("popping rightHull")
                if len(rightHull) < 3:
                    break
                
        # deriving lower tangent
        leftHull.reverse() # REVERSE LIST SO THAT WE CAN ITERATE FROM RIGHTMOST POINT, remember to reverse back at the end
        for j in leftHull:
            while is_clockwise(leftmostPoint, rightmostPoint, j):
                if j in leftHull:
                    # again, removing unsuitable points until we reach point w better convex hull
                    leftHull.pop(leftHull.index(j))
                    print("popping leftHull")
                if len(leftHull) < 3:
                    break
            
        # after arranging left and right hull,
        leftHull.reverse() # reverse list back to original
        combinedHull = leftHull + rightHull + [leftmostPoint, rightmostPoint]# combining hulls at leftmost, rightmost point
        
        return combinedHull
    
    convexHull = merge(leftHull, rightHull)     
    
    return convexHull
    #return [pts[0]]

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
    # for (i, j) in pts:
    #     plt.text(i, j, f'({i}, {j})')
    ax.title.set_text('Divide/Conquer')
    plt.show(block=False)

