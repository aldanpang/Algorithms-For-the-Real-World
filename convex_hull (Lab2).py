import matplotlib.pyplot as plt
import time
import random

# IMPORTANT NOTES: I've commented out the code initialising test for divide and conquer (just 3 lines) to facilitate testing for gift-wrapping as my DNC algorithm 
# does not work. I've indicated * beside the code i've commented out, but feel free to uncomment it and test it if you would like.
# The complexity of this function is O(n^2), but a typical giftwrapping function can perform in O(nh) time.
# using Master Theorem, O(nlogh). 

# function that checks if three points a,b,c are clockwise positioned, ACCEPTS [X,Y] ONLY
def is_clockwise(a,b,c):
    if ((c[1] - a[1]) * (b[0] - a[0])) < ((b[1] - a[1]) * (c[0] - a[0])): # if (cy − ay) ∗ (bx − ax) < (by − ay) ∗ (cx − ax)
        return True # in clockwise order. this means that a and b forms line that leaves c on RHS
    else:
        return False # in not clockwise order

# compute with naive method the convex hull of the points cloud pts and store it as a list of vectors
def convex_hull_2d_gift_wrapping(pts): 
    # Finding leftmost point
    leftPoint = min(pts) # naive method of finding leftmost point, not considering tiebreakers
    convexHull = [] # initialising empty convex hull to append candidates for forming convex hull with
    startPoint = leftPoint
    endPoint = None # need to initilaise to use in while loop
    
    while endPoint != leftPoint: # repeats until we reach the first point again
        convexHull.append(startPoint) # appends leftmostpoint, suitable candidates for convex hull
        endPoint = pts[0] # initialise endpoint as beginning of list
        for i in pts[1:]: # for every [x,y] in pts
            if endPoint == startPoint or is_clockwise(startPoint, endPoint, i ):
                # 1) if we reach the end OR 
                # 2) we try every permutation of lines starting from start point to every endpoint + whether it leaves
                # every other point on RHS  
                endPoint = i # assists with 2) where endpoints are updated as i to try every endpoint
        startPoint = endPoint # else, endpoint that leaves all other points on RHS becomes startPoint, which will be appended at
                              # start of while loop
    return convexHull      # returns our final convex hull list
    
# compute with divide and conquer method the convex hull of the points  
# cloud pts and store it as a list of vectors
def convex_hull_2d_divide_conquer(pts): 
    if len(pts) <= 5: #base case, solves with naive method if len(pts) is too small
        print("base case giftwrap", convex_hull_2d_gift_wrapping(pts))
        return convex_hull_2d_gift_wrapping(pts)
        
    mid = len(pts)//2  
    left = pts[:mid] # just splits pts into halves
    right = pts[mid:]
    leftHull = convex_hull_2d_divide_conquer(left) # Recursively breaks down list, computes convex hull of smallest subproblems
    rightHull = convex_hull_2d_divide_conquer(right)
    
    def merge(leftHull, rightHull): # merge function to combine base cases
        rightmostPoint = max(leftHull, key = lambda p: p[0]) # of left hull, returns rightmost point by x coords
        leftmostPoint = min(rightHull, key = lambda p: p[0]) # of right hull, returns leftmost point

        leftHull += [rightmostPoint] # adds another copy of leftmost and rightmost points, to form tangents with
        rightHull += [leftmostPoint]
    
       # deriving upper tangent
        upperTangentHull = [] # initialising empty convex hull to append candidates for forming convex hull with
        startPoint = rightmostPoint
        endPoint = None # upper tangent's line won't exceed (go below) the leftmost point of right hull, so might be better to fix this value
        
        while endPoint != rightmostPoint: # repeats until we reach the end point
            upperTangentHull.append(startPoint) # appends rightmostpoint and suitable candidates for convex hull
            endPoint = rightHull[0] # checks through every right hull point 
            for i in rightHull: # for every [x,y] in right hull
                if endPoint == startPoint or is_clockwise(startPoint, endPoint, i) == False:
                    # 1) if we reach the end OR 
                    # 2) we try every permutation of lines starting from start point to every endpoint and checks whether it leaves
                    # every other point on LHS, since it's the lower tangent  
                    endPoint = i # assists with 2) where endpoints are updated as i to try every endpoint
            startPoint = endPoint # else, endpoint that leaves all other points on LHS becomes startPoint, which will be appended at
                                # start of while loop
       
        # deriving lower tangent
        lowerTangentHull = [] # initialising empty convex hull to append candidates for forming convex hull with
        startPoint = leftmostPoint
        endPoint = None # as lower tangent's line won't exceed (go above) the rightmost point of right hull 
        
        while endPoint != leftmostPoint: # repeats until we reach the end point
            lowerTangentHull.append(startPoint) # appends leftmostpoint and suitable candidates for convex hull
            endPoint = rightHull[0]
            for i in rightHull: # for every [x,y] in right hull
                if endPoint == startPoint or is_clockwise(startPoint, endPoint, i) == False:
                    # 1) if we reach the end OR 
                    # 2) we try every permutation of lines starting from start point to every endpoint and checks whether it leaves
                    # every other point on LHS, since it's the lower tangent  
                    endPoint = i # assists with 2) where endpoints are updated as i to try every endpoint
            startPoint = endPoint # else, endpoint that leaves all other points on LHS becomes startPoint, which will be appended at
                                # start of while loop

        combinedHull = upperTangentHull + lowerTangentHull # combining hulls at leftmost, rightmost point
        
        return combinedHull
    
    convexHull = merge(leftHull, rightHull)     
    
    return convexHull


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
# * hull_divide_conquer = convex_hull_2d_divide_conquer(pts)
print("done ! It took ",time.time() - t," seconds")

# close the convex hull for display
hull_gift_wrapping.append(hull_gift_wrapping[0])
# * hull_divide_conquer.append(hull_divide_conquer[0])

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
    # * ax.plot([x[0] for x in hull_divide_conquer], [x[1] for x in hull_divide_conquer], "ro--")
    ax.title.set_text('Divide/Conquer')
    plt.show(block=False)

