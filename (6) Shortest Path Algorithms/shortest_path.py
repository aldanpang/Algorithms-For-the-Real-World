from random import randint
import math
import networkx as nx
import matplotlib.pyplot as plt

NODES = 8              # defines number of nodes in the graph
EDGES = 16              # defines number of edges in the graph
DIRECTED = True         # defines if the graph is directed or undirected
NEGATIVE_WEIGHT = False # defines if the edges can have negative weight
INFINITY = math.inf     # defines a variable for infinity

# function that implements the Dijkstra's algorithm for single-pair shortest paths
def dijkstra(graph, start_node):
    n = len(graph)
    D = [INFINITY]*n
    D[start_node] = 0
    cloud = [False]*n

    while True: # keeps looping until all nodes are visited
        v = None # represents closest node we can travel to
        for i in range(n): # for each node,
            if not cloud[i] and (v is None or D[i]< D[v]): # if node not found in cloud/we just started algo/ if dist. to i is shorter than dist. to v
                v = i
        if v is None: # if there are no nodes we can travel to then break
            break 
        
        cloud[v] = True # adds v to cloud    
                
        for b, w in graph[v]: # b is end node, w is weight 
            if not cloud[b]:
                if D[v] + w < D[b]: # if distance to end node from v is shorter than current shortest distance
                    D[b] = D[v] + w # update distance
        
    return D

# function that implements the Floyd-Warshall's algorithm for all-pairs shortest paths
def floyd_warshall(graph):
    D = [[[ INFINITY for i in range(len(graph)) ] for j in range(len(graph)) ] for k in range(len(graph)+1) ]
    n = len(graph)
    
    def is_connected(graph, vertex_1, vertex_2): # function that checks if two vertices are connected by an edge
        for edge in g[i]:
            if edge[0] == j:
                return [True, edge[1]] # returns True if vertices are connected
        return [False, 0] # initialised weight as dummy value 0
    
    # initialisation
    for i in range(n):
        for j in range(n):
            if i == j: # if both vertices chosen are same then distance is naturally 0
                D[0][i][i]= 0 
            elif is_connected(graph, i, j)[0]: # else if there is an edge from i to j  
                D[0][i][j] = is_connected(graph, i, j)[1]  # update distance table with weight of edge from i to j
            else:
                D[0][i][j]=  INFINITY # no path exists from i to j
                
    # recursion formula 
    for k in range(n):
        for i in range(n):
            for j in range(n):
                D[k+1][i][j] = min(D[k][i][j], D[k][i][k] + D[k][k][j])
            
    return D[n][:][:]

    
# function that creates the graph
def make_graph(NUMBER_NODES, NUMBER_EDGES, NEGATIVE_WEIGHT, DIRECTED):
    if NODES*NODES<NUMBER_EDGES: 
        print("Impossible to generate a simple graph with %i nodes and %i edges!\n" %(NUMBER_NODES,NUMBER_EDGES))
        return None
    g = [[] for i in range(NUMBER_NODES)]
    for i in range(NUMBER_EDGES):
        while True:
            start_node = randint(0,NUMBER_NODES-1)
            end_node = randint(0,NUMBER_NODES-1)
            if NEGATIVE_WEIGHT: weight = randint(-20,20)
            else: weight = randint(1,20)
            if (start_node != end_node): 
                found = False
                for j in range(len(g[start_node])): 
                    if g[start_node][j][0] == end_node: found = True
                if not found: break            
        g[start_node].append([end_node, weight])
        if DIRECTED==False: g[end_node].append([start_node, weight])
    return g
 

# function that prints the graph
def print_graph(g, DIRECTED):
    if DIRECTED: G = nx.DiGraph()
    else: G = nx.Graph()
    for i in range(len(g)): G.add_node(i)
    for i in range(len(g)):
        for j in range(len(g[i])): G.add_edge(i,g[i][j][0],weight=g[i][j][1])
    for i in range(len(g)):
        print("from node %02i: " %(i),end="")
        print(g[i])
    try: 
        pos = nx.planar_layout(G)
        nx.draw(G,pos, with_labels=True)
    except nx.NetworkXException:
        print("\nGraph is not planar, using alternative representation")
        pos = nx.spring_layout(G)
        nx.draw(G,pos, with_labels=True)
    if DIRECTED: 
        labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels, label_pos=0.3)
    else:
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)



    
print("\n\n ******** GENERATING GRAPH ********" )     
g = make_graph(NODES,EDGES,NEGATIVE_WEIGHT,DIRECTED)
if g==None: raise SystemExit(0)
elif NODES<50 and EDGES<2500:
    plt.figure(1,figsize=(10,10))
    print_graph(g,DIRECTED)

print("\n\n ******** PERFORMING DIJKSTRA ********" )    
D = dijkstra(g,0)
print("Single-Pair Distance Table (from node 0): ",end="")
print(D)

print("\n\n ******** PERFORMING FLOYD WARSHALL ********" )   
D = floyd_warshall(g)
print("All-Pairs Distance Table: \n",end="")
for i in range(len(g)): 
    print("from node %02i: " %(i),end="")
    print(D[i])

