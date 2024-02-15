import random 
import time
import math


def bubble_sort(my_list):       
    # do n passes on the list
    swapped = True
    while swapped:
       swapped = False   

	   # check neighbours and swap them if needed     
       for j in range(len(my_list)-1):
           if my_list[j] > my_list[j+1]:
               temp = my_list[j]
               my_list[j] = my_list[j+1]
               my_list[j+1] = temp     
               swapped = True


def selection_sort(my_list):  
    for i in range(len(my_list)-1): # perform n-1 passes
        
    	# find the minimum in the unsorted part of my_list 
        min_index = i
        for j in range(i+1,len(my_list)):
            if my_list[j]< my_list[min_index]:
                min_index = j
            
        # swap this min element with the first unsorted element from my_list 
        temp = my_list[i]
        my_list[i] = my_list[min_index]
        my_list[min_index] = temp 


def insertion_sort(my_list):
    i = 1                   # i is the size of the sorted list
    while i < len(my_list): # while the list is not sorted yet
    	j = i
    
    	# place the element j at the proper place in the sorted list
    	while j > 0 and my_list[j-1] > my_list[j]:
    	  # swap 
    	  temp = my_list[j]
    	  my_list[j] = my_list[j-1]
    	  my_list[j-1] = temp
    	  j = j - 1 
            
    	i = i + 1


def merge_sort(my_list):
    # if the list is empty or contains just one element, no need to sort 
    if len(my_list) <= 1: return my_list
     
    # we divide the work in two halves, and sort them recursively
    mid = int(len(my_list) / 2)
    left = merge_sort(my_list[:mid])      
    right = merge_sort(my_list[mid:])   
    
    # merge the two sorted halves, while keeping the list sorted
    my_sorted_list = []
    while left != [] or right != []: 
        if left == []: my_sorted_list.append(right.pop(0))  # left is empty
        elif right == []: my_sorted_list.append(left.pop(0)) # right is empty
        elif left[0] < right[0]: my_sorted_list.append(left.pop(0))
        else:  my_sorted_list.append(right.pop(0))
    
    return my_sorted_list

def quick_sort(my_list):
    if len(my_list) <= 1: # base case
        return my_list
    
    else: 
        randomIndex = random.randint(0, len(my_list)-1) # returns random index of pivot according to length of list
        pivot = my_list[randomIndex] # saves the value of pivot using the randomly chosen index 
        left = [i for i in my_list if i < pivot] # saves left half of list with values less than pivot 
        equal = [i for i in my_list if i == pivot] # saves duplicate values equal to pivot, note that without this we lose some entries
        right = [i for i in my_list if i > pivot] # saves right half, with values more than pivot
        return quick_sort(left) + equal + quick_sort(right)
    
def add_to_heap(heap, element): # adds element into heap and ensures that heap properties are maintained
    heap.append(element) # adds element into heap
    addedIndex = len(heap) - 1 # index of added element, which is always the last element

    while addedIndex > 0: # keeps swapping until we reach root
        parentIndex = math.ceil(addedIndex / 2) - 1 # simple function in lab that shows index of parent of added element

        if heap[addedIndex] < heap[parentIndex]: # if value of added < value of it's parent then we swap them around
            heap[addedIndex], heap[parentIndex] = heap[parentIndex], heap[addedIndex] # swapping
            addedIndex = parentIndex # updates new index for added node
        else:
            break

def remove_min_from_heap(heap):
    minElement = heap[0] # storing min value
    heap[0] = heap[-1] # replacing root with min value
    heap.pop() # popping min value

    i = 0
    while True: # iterate until there are no more comparable heap values (left, right, smallest) and that smallest != i. ie. we reached the leaf
        leftChildIDX = 2 * i + 1 # just indices given by lab notes, applies to both left and right child
        rightChildIDX = 2 * i + 2

        smallest = i # initialises index of smallest value. Updated every iteration of checks in the if statements below

        # note that for the following, we are:
        # 1) ensuring that updated indices are not out of range
        # 2) checking if our current min value heap[smallest] is larger than the left/right child. If it is, then we shift the value down 
        if leftChildIDX < len(heap) and heap[leftChildIDX] < heap[smallest]:
            smallest = leftChildIDX

        if rightChildIDX < len(heap) and heap[rightChildIDX] < heap[smallest]:
            smallest = rightChildIDX

        if smallest != i: # this if statement swaps the values of min value and smaller child around, then updates i 
            heap[i], heap[smallest] = heap[smallest], heap[i]
            i = smallest
        else:
            break

    return minElement 

def heap_sort(my_list): 
    # phase 1, taking input data and creating heap
    heap = [] # initialises empty heap
    for i in my_list:
        add_to_heap(heap, i) # adds every item in the list into the heap
    
    # phase 2, sorting heap n times
    sorted_heap = []
    while len(heap) > 0:
        sorted_heap.append(remove_min_from_heap(heap))
        
    return sorted_heap 

def test_sorting(algo,my_tab,display):
    tab = my_tab.copy()
    print("testing",algo,str(" "*(14-len(algo))),"... ",end='')
    t = time.time()
    temp = eval(algo + "(tab)")
    if temp != None: tab = temp
    print("done ! It took {:.2f} seconds".format(time.time() - t))
    if display: print(tab,end='\n\n')
    

print("\n ******** Testing to sort a small table of 30 elements ********")
NUMBER_OF_ELEMENTS = 30
tab = [random.randint(1, 40) for i in range(NUMBER_OF_ELEMENTS)] # no issues found other than 0.04 seconds difference in speed, continue
# tab = list(set([random.randint(1, 40) for i in range(NUMBER_OF_ELEMENTS)]))
print("Original table: ")
print(tab,end='\n\n')
test_sorting("bubble_sort",tab,True)
test_sorting("selection_sort",tab,True)
test_sorting("insertion_sort",tab,True)
test_sorting("merge_sort",tab,True)
test_sorting("quick_sort",tab,True)
test_sorting("heap_sort",tab,True)

print("\n ******** Testing to sort a big table of 5000 elements ********")
NUMBER_OF_ELEMENTS = 5000
tab = list(set([random.random() for i in range(NUMBER_OF_ELEMENTS)]))
test_sorting("bubble_sort",tab,False)
test_sorting("selection_sort",tab,False)
test_sorting("insertion_sort",tab,False)
test_sorting("merge_sort",tab,False)
test_sorting("quick_sort",tab,False)
test_sorting("heap_sort",tab,False)
