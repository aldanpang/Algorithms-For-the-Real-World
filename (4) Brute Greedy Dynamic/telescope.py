import random 
import time
import math

# this function checks if two tasks are conflicting. It assumes L is sorted according to starting time
def is_conflict(L):
    for i in range(len(L)-1):
        if L[i][1] > L[i+1][0]: return True # is overlapping
    return False

# this function makes a random search for assignments
def random_search(L):
    vec_assignment = [0]*len(L)
    
    while True:         
        non_conflicting_tasks = []
        for i,el in enumerate(L):
            if vec_assignment[i] == 0:
                vec_assignment[i] = 1
                assignment = [L[k] for k in range(len(L)) if vec_assignment[k]==1 ]
                if not is_conflict(assignment):
                    non_conflicting_tasks.append(i)
                vec_assignment[i] = 0
                        
        if len(non_conflicting_tasks)==0:
            assignment = [L[k] for k in range(len(L)) if vec_assignment[k]==1 ]
            val = sum([k[2] for k in assignment])
            return (val,assignment)
        
        i = non_conflicting_tasks[random.randint(0,len(non_conflicting_tasks)-1)]
        vec_assignment[i] = 1        

# this function makes a brute force search for assignments
def brute_force(L):      
    # note that each tuple is represented as: (start time, end time, scientific benefit)
    bestCombination = (0, None) # used in for loop, replaced by best combination with best benefit
    
    n = len(L) # number of tasks
    numCombinations = 2**n # number of combinations
    
    for i in range(numCombinations): # counter going from 0 to 2^n - 1
        binaryRep = format(i, f'0{n}b') # creates all possible combinations of bits. 1 selects task at that position
        chosenReq = [L[i] for i, bit in enumerate(binaryRep) if bit == '1'] # returns list of requests according to bit tuple. enumerate necessary to tag index to bit 0/1
        
        if not is_conflict(chosenReq): # if there is no overlap, do this
            totalBenefit = sum(request[2] for request in chosenReq)  # summing up benefit for each combination of requests
        # skips if there is overlap
        
        if totalBenefit > bestCombination[0]:
            bestCombination = (totalBenefit, chosenReq) # if we tabulate higher benefit from this combination, replace old combination with new one
        
    return bestCombination # outputs best found benefit, list of requests for that benefit. Note that the list is represented as task 1, task 2, task 3...


# this function makes a greedy force search for assignments
# Note that the greedy algorithm we used selects tasks with earliest end times, which is found to always produce an optimal solution
def greedy(L):
    currentEndTime = 0 # save earliest end times 
    bestCombination = (0, None) # for replacing and outputting later on
    chosenRequests = [] # stores tuple of requests
    chosenBenefits = [] # stores benefits 
    
    for i in L:
        startTime, endTime, benefit = i # saves start and endtimes, benefits in variables
        
        if startTime >= currentEndTime: # if next task does not conflict with previous entry, append it to final lists and update new end time
            chosenRequests.append(i)
            currentEndTime = endTime
            chosenBenefits.append(benefit)
            
    totalBenefit = sum(i for i in chosenBenefits)
    bestCombination = (totalBenefit, chosenRequests)
    
    return bestCombination


# this function makes a dynamic programing search for assignments

########################################################
## Works, but sometimes returns overlapping schedules ##
########################################################

def dynamic_prog(L): # note that this is an 0-1 knapsack problem as we lose all benefit when we take part of duration
    # variable Bi representing max benefit achieved with first i requests in L
    # final solution Bn for n observations 
    
    L.sort(key = lambda x: x[1]) # sorts end times in ascending order
    n = len(L) # storing length of lists
    
    W = max(task[1] for task in L) # stores largest end time from L
    K = [[0 for x in range(W+1)] for x in range(n+1)] # initialise 2D array for memoization with rows bounded by max end time, columns bounded by length of L
    chosenRequests = []
    
    for i in range(n + 1): # building table in bottom up manner. This line is for each tuple (rows)
        for w in range(W + 1): # this line represents each end time (columns). For each B[i][w] where w changes,
            if i == 0 or w == 0: # base case
                K[i][w] = 0 # replace in array the value at i, 
            
            elif L[i-1][1] > w:
                K[i][w] = K[i-1][w] # replace i'th best selection with k-1'th best selection
            
            else: # otherwise if end time of i'th item <= w'th end time
                K[i][w] = max(L[i-1][2] + K[i-1][w - L[i-1][1]], K[i-1][w]) # subproblem optimality
             
    i, w = n, W # backtracking to find tasks selected. starts from last tuple, largest end time 
    while i > 0 and w > 0:
        if K[i][w] != K[i - 1][w]:
            if not is_conflict(chosenRequests + [L[i - 1]]): # checks if there is a conflict between tasks 
                chosenRequests.append(L[i - 1]) # appends task corresponding to benefit
                w -= L[i - 1][1] # backtracks here by updating new value of i, w
        i -= 1

    return K[n][W], chosenRequests[::-1]  # note that we reverse the order of list given to obtain original


# this function prints the tasks
def print_tasks(L):
    for i,t in enumerate(L):
        print("task %2i (b=%2i):" %(i,t[2]),end="")
        print(" "*round(t[0]/10) + "-"*round((t[1]-t[0])/10))
        

# this function tests and times a telescope tasks assignment search
def test_telescope(algo,my_tab,display):
    tab = my_tab.copy()
    print("testing",algo,str(" "*(14-len(algo))),"... ",end='')
    t = time.time()
    (max_temp,assignment_temp) = eval(algo + "(tab)")
    print("done ! It took {:.2f} seconds".format(time.time() - t))
    if max_temp!=None:
        print("Solution with benefit = %i" %(max_temp),end='\n')
    if display: 
        if assignment_temp!=None:
            print_tasks(assignment_temp)
            print()
    
MAX_BENEFIT = 99
MAX_START_TIME = 500
MAX_DURATION = 250

NUMBER_OF_ELEMENTS = 10
print("\n ******** Testing to solve for %i events ********" %(NUMBER_OF_ELEMENTS))
val = [(random.randint(1, MAX_START_TIME),random.randint(1, MAX_DURATION),random.randint(1, MAX_BENEFIT)) for i in range(NUMBER_OF_ELEMENTS)] 
tab = sorted([(val[i][0],val[i][0]+val[i][1],val[i][2]) for i in range(NUMBER_OF_ELEMENTS)])
print("Problem instance: ")
print_tasks(tab)
print("")
test_telescope("random_search",tab,True)
test_telescope("brute_force",tab,True)
test_telescope("greedy",tab,True)
test_telescope("dynamic_prog",tab,True)


# NUMBER_OF_ELEMENTS = 20
# print("\n ******** Testing to solve for %i events ********" %(NUMBER_OF_ELEMENTS))
# val = [(random.randint(1, MAX_START_TIME),random.randint(1, MAX_DURATION),random.randint(1, MAX_BENEFIT)) for i in range(NUMBER_OF_ELEMENTS)] 
# tab = sorted([(val[i][0],val[i][0]+val[i][1],val[i][2]) for i in range(NUMBER_OF_ELEMENTS)])
# test_telescope("random_search",tab,False)
# test_telescope("brute_force",tab,False)
# test_telescope("greedy",tab,False)
# test_telescope("dynamic_prog",tab,False)

