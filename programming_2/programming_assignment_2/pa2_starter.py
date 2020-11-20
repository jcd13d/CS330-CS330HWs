
import numpy as np
import sys
import heapq

############################

# DO NOT CHANGE THIS PART!!

############################

def readGraph(input_file):
    with open(input_file, 'r') as f:
        raw = [[float(x) for x in s.split(',')] for s in f.read().splitlines()]
    N = int(raw[0][0])
    m = int(raw[1][0])
    s = int(raw[2][0])
    adj_list = [[] for foo in range(N)]
    for edge in raw[3:]:
        adj_list[int(edge[0])].append((int(edge[1]), edge[2]))
    return N, m, s, adj_list


def writeOutput(output_file, N, s, distances, parents, mst):
    with open(output_file, 'w') as f:
        # output dijkstra
        for i in range(N):
            if i == s:
                f.write('0.0,-\n')
            else:
                f.write(str(distances[i])+','+str(parents[i])+'\n')
        
        # blank space
        f.write('\n')

        #output MST (just neighbors, no edge weights)
        for j in range(N):
            neighbors = []
            for node in mst[j]:
                neighbors.append(str(node[0]))
            # sort for the autograder
            neighbors.sort()
            f.write(','.join(neighbors) +'\n')

# 
def make_undirected_graph(N, adj_list):
    G = {}
    for u in range(N):
        G[u] ={}

    # move our stuff in
    for u in range(N):
        for v in adj_list[u]:
            G[u][v[0]] = v[1]
            G[v[0]][u] = v[1]
    #back to list
    adj_list = ['x' for x in range(N)]
    for u in range(N):
        neighbors = []
        for v in G[u].keys():
            neighbors.append((v, G[u][v]))
        adj_list[u] = list(set(neighbors))
    return adj_list





def Run(input_file, output_file):
    N, m, s, adj_list = readGraph(input_file)
    distances, parents =   dijkstra(N, m, s, adj_list)
    undirected_adj_list = make_undirected_graph(N, adj_list)
    mst = kruskal(N, m, undirected_adj_list)
    writeOutput(output_file, N, s, distances, parents, mst)


############################

# ADD YOUR OWN METHODS HERE (IF YOU'D LIKE)

############################






############################

# FINISH THESE METHODS

############################


def decrease_key(heap, kv_tuple):
    """
    TODO: this dec key operation runs in O(n) time
        - O(n) search for value
        - O(logn) sift heapify operations

    Is there are way to do better?

    """
    key, value = kv_tuple
    index = None
    for i, (k, v) in enumerate(heap):
        if v == value:
            index = i
            break

    if index is not None:
        heap[index] = kv_tuple
        heapq._siftup(heap, index)
        heapq._siftdown(heap, 0, index)

    return heap


def dijkstra(N, m, s, adj_list):
    # You are given the following variables:
    # N = number of nodes in the graph
    # m = number of edges in the graph
    # s = source node for the algorithm
    # adj_list = a list of lists of size N, where each index represents a node n
    #               the sublist at index n has a list of two-tuples,
    #               representing outgoing edges from n: (adjacent node, weight of edge)
    #               NOTE: If a node has no outgoing edges, it is represented by an empty list
    #
    # WRITE YOUR CODE HERE:


    # Return two lists of size N, in which each index represents a node n:
    # distances: the shortest distance from s to n
    # parents: the last (previous) node before n on the shortest path

    # def binary_search(list, val):
    #
    #     def binary_search_inner(list, left, right, val):
    #         if left > right:
    #             return None
    #
    #         mid = (left + right)//2
    #
    #         if list[mid][1] == val:
    #             return mid
    #         if list[mid][1] > val:
    #             return binary_search_inner(list, left, mid - 1, val)
    #         elif list[mid][1] <= val:
    #             return binary_search_inner(list, mid + 1, right, val)
    #
    #     return binary_search_inner(list, 0, len(list), val)
    #
    # print(binary_search([(1, 5), (2, 10), (3, 2), (4, 20), (5, 22)], val=10))

    distances = {}
    parents = {}
    pq = []
    visited = [False]*N

    for i in range(N):
        if i == s:
            distances[i] = 0
            heapq.heappush(pq, (distances[s], 0))
        else:
            distances[i] = np.inf
            heapq.heappush(pq, (distances[i], i))
        parents[i] = None

    while len(pq) > 0:
        dist, node = heapq.heappop(pq)
        for adj_node, adj_weight in adj_list[node]:
            if not visited[adj_node]:
                d_prime = distances[node] + adj_weight
                if d_prime < distances[adj_node]:
                    distances[adj_node] = d_prime
                    decrease_key(pq, (d_prime, adj_node))
                    parents[adj_node] = node

    return distances, parents


def kruskal(N, m, undirected_adj_list):
    # You are given the following variables:
    # N = number of nodes in the graph
    # PLEASE NOTE THAT THE ADJACENCY LIST IS FORMATTED ENTIRELY DIFFERENTLY FROM DIJKSTRA ABOVE
    # undireced_adj_list = a list of lists of size N, where each index represents a node n
    #                       the sublist at index n has a list of two-tuples, representing edges from n: (adjacent node, weight of edge)
    #                       NOTE: Since the graph is undirected, each edge (u,v) is now represented twice in this adjacency list:
    #                               once at index u and once at index v
    #
    # WRITE YOUR CODE HERE:


    # Return the adjacency list for the MST, formatted as a list-of-lists in exactly the same way as undirected_adj_list

    mst_adj_list = [[(1, 1, 0), (2, 2, 0)] for i in range(N)]
    return mst_adj_list




#############################
# CHANGE INPUT FILES FOR PART 2 HERE

#############################

def main(args=[]):
    # WHEN YOU SUBMIT TO THE AUTOGRADER, 
    # PLEASE MAKE SURE THE FOLLOWING FUNCTION LOOKS LIKE:
    # Run('input', 'output')
    Run('input', 'output')

    # AFTER YOUR RUN THE AUTOGRADER,
    # you may change comment out the above line
    # and uncomment the Run commend for the graph from part 2
    # that you wish to work on:
    
    #Run('g_randomEdges.txt', 'output')
    #Run('g_donutEdges.txt', 'output')
    #Run('g_zigzagEdges.txt', 'output')

if __name__ == "__main__":
    main(sys.argv[1:])    