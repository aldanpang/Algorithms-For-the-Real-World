from random import shuffle, randrange, random
import math
import collections

MAZE_SIZE = 10

def DFS_search(g,start_node,end_node):
    visited = set() # initialise set containing nodes we visited before
    path = [] # initialise list where we store path towards node. note that its a stack
    
    def dfs(node): # returns dfs traversal 
        visited.add(node) # everytime we call dfs, we add the node to visited and path
        path.append(node)

        if node == end_node: # if we reach target node, then the path is just to itself and we found the path (True)
            return True
        
        for neighbour in g[node]: # for every neighbour of the current node
            if neighbour not in visited: # if we haven't visited it,
                if dfs(neighbour):  # tells us whether path to end from neighbour has been found from 'if node == end_node'
                    return True
                
        path.pop() # pops current node if there is no path to end from current neighbour
        return False # tells us that no path was found as the loop ends without finding a path (no Trues were returned)
    
    dfs(start_node) # start dfs traversal
    
    if path[-1] == end_node: # returns path if we found end_node 
        return path
    else:
        return []

    
def BFS_search(g, start_node, end_node):
    visited = set() # track visited nodes
    queue = collections.deque([(start_node, [start_node])])  # not really necessary to use double ended queues, but does help make the algorithm faster 
    # note that queue is a tuple containing the starting node and it's path (an empty list containing a start node for now)

    while queue: # loops while queue is not empty. 
        current_node, path = queue.popleft() # dequeues front of the queue. assigns the currently explored node to current_node and path to path
        visited.add(current_node) # adds removed node (currently explored node) to visited 

        if current_node == end_node: # if reach target node, we return path 
            return path 

        for neighbour in g[current_node]: # iterates through neighbours of dequeued node to check if they're visited.
            if neighbour not in visited:
                queue.append((neighbour, path + [neighbour]))  # if unvisited, we insert neighbours of removed nodes into the queue

    return [] # returns [] if no path was found

 
def make_maze():
    vis = [[0] * MAZE_SIZE + [1] for _ in range(MAZE_SIZE)] + [[1] * (MAZE_SIZE + 1)]
    ver = [["|:"] * MAZE_SIZE + ['|'] for _ in range(MAZE_SIZE)] + [[]]
    hor = [["+-"] * MAZE_SIZE + ['+'] for _ in range(MAZE_SIZE + 1)]
 
    def walk(x, y):
        vis[y][x] = 1
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+ "
            if yy == y: ver[y][max(x, xx)] = " :"
            walk(xx, yy)
 
    walk(randrange(MAZE_SIZE), randrange(MAZE_SIZE))
 
    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    
    s_temp = s
    graph = [[] for i in range(MAZE_SIZE*MAZE_SIZE)]
    for col in range(MAZE_SIZE):
        for row in range(MAZE_SIZE):
            if s_temp[(2*row+1)*(2*MAZE_SIZE+2)+(2*col)] == " " or (random() < 1/(2*MAZE_SIZE) and col != 0): 
                graph[col+MAZE_SIZE*row].append(col-1+MAZE_SIZE*row)
                graph[col-1+MAZE_SIZE*row].append(col+MAZE_SIZE*row)
                
            if s_temp[(2*row+2)*(2*MAZE_SIZE+2)+(2*col)+1] == " " or (random() < 1/(2*MAZE_SIZE) and row != MAZE_SIZE-1): 
                graph[col+MAZE_SIZE*row].append(col+MAZE_SIZE*(row+1))
                graph[col+MAZE_SIZE*(row+1)].append(col+MAZE_SIZE*row)
    
    return s,graph
 
   
def print_maze(g, path, players):
      
    s = ""
    for col in range(MAZE_SIZE): s+="+---"
    s+="+\n"
    
    for row in range(MAZE_SIZE): 
        s+="|"
        for col in range(MAZE_SIZE): 
            if row*MAZE_SIZE+col == players[0]: s+="👨 "
            elif row*MAZE_SIZE+col == players[1]: s+="🍒 "
            elif row*MAZE_SIZE+col in path: 
                ind = path.index(row*MAZE_SIZE+col)
                if path[ind+1] == row*MAZE_SIZE+col+1: s+=" → "
                elif path[ind+1] == row*MAZE_SIZE+col-1: s+=" ← "
                elif path[ind+1] == row*MAZE_SIZE+col+MAZE_SIZE: s+=" ↓ "
                elif path[ind+1] == row*MAZE_SIZE+col-MAZE_SIZE: s+=" ↑ "
                else: s+="ppp"
            else: s+="   " 
            if (row*MAZE_SIZE+col+1) in g[row*MAZE_SIZE+col]: s+=" "
            else: s+="|"
                
        s+="\n+" 
        for col in range(MAZE_SIZE): 
            if ((row+1)*MAZE_SIZE+col) in g[row*MAZE_SIZE+col]: s+="   +"
            else: s+="---+"
        s+="\n"
        
        
    print(s)
                
    
    
s, g = make_maze()    
# g = [[3, 1], [0, 4], [5], [0], [1, 5], [2, 4, 8], [7], [6, 8], [5, 7]]
players = [0,MAZE_SIZE*MAZE_SIZE-1]
print(g)

print("\n\n ******** PERFORMING DFS ********" )
path_DFS = DFS_search(g,players[0],players[1])
print_maze(g,path_DFS,players)
print("Path length for DFS is %i" % (len(path_DFS)-1))

print("\n\n ******** PERFORMING BFS ********" )
path_BFS = BFS_search(g,players[0],players[1])
print_maze(g,path_BFS,players)
print("Path length for BFS is %i" % (len(path_BFS)-1))