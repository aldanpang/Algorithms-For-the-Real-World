import matplotlib.pyplot as plt
import time
import random


# function that checks if three points a,b,c are clockwise positioned 
def is_clockwise(a,b,c):
    if ((c[1] - a[1]) * (b[0] - a[0])) < ((b[1] - a[1]) * (c[0] - a[0])): # if (cy − ay) ∗ (bx − ax) < (by − ay) ∗ (cx − ax)
        return True # in clockwise order
    else:
        return False # in not clockwise order 

# compute with naive method the convex hull of the points cloud pts     
# and store it as a list of vectors
# NOTE: pts comprises of sublists - ie. pts = [[4,5], [1,2], [3,4]]
def convex_hull_2d_gift_wrapping(pts):
    
    # Finding leftmost point
    leftPoint = 0 # index of leftmost point 
    for i in range(1, len(pts)):
        if pts[i][0] < pts[leftPoint][0]: # iterate through each sublist. if i'th x value is smaller than min's x value, update min with i 
            leftPoint = i # since i'th x value is smaller than min's x value, we update min
        elif pts[i][0] == pts[leftPoint][0]: # but if i'th x value  = min's x value, we tie break by checking y value
            if pts[i][1] > pts[leftPoint][1]: # leftmost point is higher y value
                leftPoint = i
                
    newpts = [] #initialise new list to order
    newpts.append(pts[leftPoint])
    
    # Forming lines with leftPoint and all other values, then checking if right side 
    for j in range(len(pts)): # j represents point we're forming line with, with leftPoint
        if j == leftPoint: # making sure we don't choose the leftPoint again
            pass
        
        else:
            for k in range(len(pts)): # checks if k is in front or behind the line
                if j == leftPoint or k == leftPoint: # again, ignores leftPoint indexes
                    pass
                elif is_clockwise(pts[leftPoint], pts[j], pts[k]):
                    newpts.append(pts[k])
        
    pts = newpts #replacing pts with ordered list
    return [pts[0]]

# compute with divide and conquer method the convex hull of the points  
# cloud pts and store it as a list of vectors
def convex_hull_2d_divide_conquer(pts):
    
    return [pts[0]]

NUMBER_OF_POINTS = 20

# generate random points and sort them accoridng to x coordinate
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


    
