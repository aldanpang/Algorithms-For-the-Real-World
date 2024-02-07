# class that represents a tree node
class Node:
    def __init__(self, height, left, right, key): # tree node implemented. assuming t = Node()
        self.height = height # integer, represents height of node in tree. accessed with t.height
        self.left = left # left child, = None if no left child, accessed with t.left
        self.right = right # right child, = None if no right child, accessed with t.right
        self.key = key # holds value (an integer) stored in node. accessed with t.node 

# class that represents an AVL tree
class AVL_tree:
    
    def __init__(self, root): # only the root is initialised
        self.root = root
    
    # method that adds a node into the AVL tree
    def search_node(self, value):
        stack = []
        t = self.root
        stack.append([t,'o'])        
        while True: 
            if t == None: return stack
            if value > t.key: 
                t = t.right
                stack.append([t,'r'])
            elif value < t.key: 
                t = t.left
                stack.append([t,'l'])
            else: return stack 

    # method that computes the height of a node t and also detects unbalanced
    # between the left and right childs
    def compute_height(self, t): # NOTE WE MUST RECOMPUTE HEIGHT OF NODE THEN CHECK IF UNBALANCED, NOT TAKE .HEIGHT
        if t == None: # if we reach the leaf
            return 0 

        leftHeight = self.compute_height(t.left) # recursively compute height of left/right child
        rightHeight = self.compute_height(t.right)
        t.height = 1 + max(leftHeight, rightHeight) # updating height of t
        
        balanceFactor = self.height(t.left) - self.height(t.right) # using balance factor to check balance
        if balanceFactor > 1 or balanceFactor < -1:
            return True # Unbalanced Node
        else:
            return False
        
    # method that applies a rotation correction
    def rotation_tree(self,a,z,y,x):
        # refer to image from AVL tree rotations - (LL RR LR RL) youtube vid to know which child is t3
        # note that z, y, x are already initialised in position, ie. z is parent of y, y is parent of x

        #########################################################################################################################################################
        ### NOTE THAT left_rotate and right_rotate FUNCTIONS WORK ONLY WHEN THE ENDING NODE X HAS BOTH LEFT AND RIGHT CHILD, OTHERWISE WILL RECURR INFINITELY ###
        #########################################################################################################################################################
        
        def left_rotate(a, z, y, x):
            t2 = y.left # stores t2, the left subtree of y
            y.left = z # replace y's left with z subtree
            
            if t2 != None: # if t2 is not leaf, update z's right to be t2
                z.right = t2 # sets z's right child as t2
                if y.key > a.key:
                    a.right = y
                else:
                    a.left = y

        def right_rotate(a, z, y, x): # WORKING
            t3 = y.right # stores t3 subtree, right child of y
            y.right = z # sets y's right child as node z
            if t3 != None: # if t3 is not leaf, update z's left to be t3
                z.left = t3 
                if y.key > a.key: # reattaches parent based on value of y
                    a.right = y
                else:
                    a.left = y 
        
        # case 1: Right right case, left rotation 
        if x.key == y.right.key and y.key == z.right.key:
            print("right right case")
            left_rotate(a, z, y, x)
            # t2 = y.left.key # stores y's left child for later use
            # y.left = z # updates y's left to become z (which carries over z's child t1) 
            # z.right.key = t2 # carries y's child to z's right 
            
            # if y.key > a.key: # reattaching y's parent
            #     a.right = y
            # else:
            #     a.left = y
        
        # case 2: Left left case, right rotation 
        elif x.key == y.left.key and y.key == z.left.key:
            print("left left case")            
            right_rotate(a, z, y, x)
            
            #################
            # if x.left == None or x.right == None: # if x has no left/right child, don't store t3 and just make z right child of y
            #     if x.left == None:
            #         t3 = y.right.key # stores y's right child as t3
            #         y.right = z # makes z right child of y 
            #         z.left.key = t3 # sets z's left as t3
            #         x.left = None
                    
            #         if y.key > a.key: # reattaching x's parent
            #             a.right = y
            #         else:
            #             a.left = y
                    
            #     elif x.right == None:
            #         t3 = y.right.key # stores y's right child as t3
            #         y.right = z # makes z right child of y 
            #         z.left.key = t3 # sets z's left as t3
            #         x.right = None
                    
            #         if y.key > a.key: # reattaching x's parent
            #             a.right = y
            #         else:
            #             a.left = y                    
                    
            # elif x.left != None and x.right != None: # if x has a left/right child, then we need to store as t2, assign it to z
            #     t3 = y.right.key # stores y's right child as t3
            #     y.right = z # makes z right child of y 
            #     z.left.key = t3 # sets z's left as t3 
                
            #     if y.key > a.key: # reattaching x's parent
            #         a.right = y
            #     else:
            #         a.left = y                
            
        ###############################################################################################
        ## NOTE THAT FROM HERE ON OUT, IT'S A CONCERN IF WE TAKE X LEFT/RIGHT KEY AS IT MAY BE NONE ###
        ###############################################################################################
        
        # case 3: Left right case, left rotation then right rotation (WORKING)
        elif x.key == y.right.key and y.key == z.left.key:
            print("left right case")
            left_rotate(a, z, y, x)
            right_rotate(a, z, x, y)
            
            
            # # left rotation first
            # if x.left == None: # if x has no left child, don't store t2 and just swap positions of x and y
            #     x.left = y
            #     z.left = x # reassigns parent of x to z
            #     y.right = None
                
            # else: # if x has a left child, then we need to store as t2, assign it to z
            #     t2 = x.left.key # stores t2
            #     x.left = y # swaps position of x and y
            #     y.right.key = t2 # reassigns y's right to t2
            #     z.left = x # reassigns parent of x to z
            
            # # right rotation
            # if x.right == None: # if x has no right child, don't store as t3 and just swap positions of x and z
            #     print("right rotation")
            #     x.right = z
            #     z.left = None
                
            #     if x.key > a.key: # reattaching x's parent
            #         a.right = x
            #     else:
            #         a.left = x
                    
            
            # else: # if x has right child, store as t3 and assign to z's left. swap positions of x and z
            #     t3 = x.right.key
            #     x.right = z
            #     z.left.key = t3
                
            #     if x.key > a.key: # reattaching x's parent
            #         a.right = x
            #     else:
            #         a.left = x                
                        
        # case 4: Right left case, right rotation then left rotation:
        elif x.key == y.left.key and y.key == z.right.key:
            print("right left case")
            right_rotate(a, z, y, x)
            left_rotate(a, z, y, x)
            
            
        #     # right rotation first
        #     t3 = x.right.key # stores x's right child
        #     x.right = y # swaps position of x and y 
        #     y.left.key = t3 # updates y's left child to t3
        #     z.right = x # reattach x's parent
            
        #     # left rotation
        #     t2 = x.left.key # store x's left
        #     x.left = z # swaps x and z
        #     z.right.key = t2 # updates child of z to t2
            
        #     if x.key > a.key: # reattaching x's parent
        #         a.right = x
        #     else:
        #         a.left = x
            
        # else:
        #     print("none of the cases can be applied")
        
    #### NOTE FOR BELOW: .key might not be necessary if 55.left returns left key of 55 already    
        
    # method that will look for possible unbalances in the tree after a node has been added
    def backtrack_height_from_add(self, path):  
        backwardPath = path.reverse()
        addedKey = path[-1][0]
        for i in backwardPath: # for every node in path to node
            if self.compute_height(i[0]) == True: # if node is imbalanced
                leftHeight = i[0].left.height # NOTE MAYBE CALLING 55.LEFT.HEIGHT wouldnt work
                rightHeight = i[0].right.height
                if abs(leftHeight - rightHeight) > 1: # positive balance factor > 1
                    # then unbalanced with LL or LR case
                    if addedKey < i[0].left.key: # if added key < root of left subtree, LL case
                        # NOTE THAT MAYBE CALLING I[0] MEANS WE DON'T NEED TO CALL KEY AGAIN, CHECK
                        self.rotation_tree(i[0].parent, i[0], i[0].left, i[0].left.left) # NOTE SECOND ENTRY, i[0].left MIGHT BE WRONG                    
                    else: # else, LR case
                        self.rotation_tree(i[0].parent, i[0], i[0].left, i[0].left.right)
                        # note that i[0].parent is a, i would be node z, i[0].left is y, then last entry is x.

                elif abs(leftHeight- rightHeight) < -1: # negative balance factor < -1
                    # unbalanced with RR or RL case
                    if addedKey > i[0].right.key: # RR Case, if added key is more than right subtree's root.
                        self.rotation_tree(i[0].parent, i[0], i[0].right, i[0].right.right)
                    
                    else: # RL case, if added key < right subtree's root.
                        self.rotation_tree(i[0].parent, i[0], i[0].right, i[0].right.left)
            
            else: 
                print("Tree already balanced after adding node")
            
    # method that will look for possible unbalances in the tree after a node has been removed
    def backtrack_height_from_remove(self, path):
        # note path includes removed node 
        # backwardPath = path.reverse()
        # for i in backwardPath:
            
        pass
    
    
    # method that adds a node into the AVL tree
    def add_node(self, value):
        # searchNode = self.search_node(value) # returns list of path towards value
        # searchNode = searchNode[-1][0] # extracting value within node, if None means node was not found
        # if searchNode == None:
        #     return None
        
        currentNode = self.root # start from root and goes downwards
        # create node and add value
        if self.root == None:
            self.root = value
        
        elif value < currentNode.key: # if inserted value is less than root, 
            if currentNode.left == None: # if we reach leaf, then we add here
                currentNode.left = Node(value)
                currentNode.left.parent = currentNode # pointing back at parent
                self.backtrack_height_from_add(self.search_node(value)) # correct any errors if there is
            
            else:
                self.add_node(value) # if there is a value in left child, go downwards even more

        elif value > currentNode.key: # if inserted value more than root, insert in right side
            if currentNode.right == None: # if reach leaf, then add value to right side
                currentNode.right = Node(value)
                currentNode.left.parent = currentNode
                self.backtrack_height_from_add(self.search_node(value))
            
            else:
                self.add_node(value) 

        else: 
            print("Node is in tree")
        
    # method that removes a node from the AVL tree
    def remove_node(self, value):
        pass



