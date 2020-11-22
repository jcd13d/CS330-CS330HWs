
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


def pop_unvisited(heap, visit_list):
    pop_dist, pop_node = heapq.heappop(heap)
    if visit_list[pop_node]:
        return pop_unvisited(heap, visit_list)
    else:
        return pop_dist, pop_node


def dijkstra(N, m, s, adj_list, return_adj_list=False):
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

    distances = {}
    parents = {}
    pq = []
    visited = [False]*N
    visited_count = 0
    new_adj_list = [[] for i in range(N)]

    for i in range(N):
        if i == s:
            distances[i] = 0
            heapq.heappush(pq, (distances[s], s))
        else:
            distances[i] = np.inf
            heapq.heappush(pq, (distances[i], i))
        parents[i] = None

    while visited_count < N:
        dist, node = pop_unvisited(pq, visited)

        # Building adjacency list for spanning tree for part 2
        None if parents[node] is None else new_adj_list[parents[node]].append((node, distances[node] - distances[parents[node]]))

        visited_count += 1
        visited[node] = True
        for adj_node, adj_weight in adj_list[node]:
            if not visited[adj_node]:
                d_prime = distances[node] + adj_weight
                if d_prime < distances[adj_node]:
                    distances[adj_node] = d_prime
                    heapq.heappush(pq, (d_prime, adj_node))     # dec key
                    parents[adj_node] = node

    if return_adj_list:
        return distances, parents, new_adj_list
    else:
        return distances, parents


class UnionFind:
    def __init__(self, N):
        self.sizes = [1]*N
        self.set_names = [i for i in range(N)]

    def name(self, node):
        if self.set_names[node] == node:
            return node
        else:
            return self.name(self.set_names[node])

    def _union_sets_helper(self, n1, n2):
        self.sizes[self.name(n1)] += self.sizes[self.name(n2)]
        self.set_names[self.name(n2)] = self.name(n1)

    def union_sets(self, node1, node2):
        if self.sizes[self.name(node1)] >= self.sizes[self.name(node2)]:
            self._union_sets_helper(node1, node2)
        else:
            self._union_sets_helper(node2, node1)


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

    edge_list = []
    mst_adj_list = [[] for i in range(N)]

    # TODO limit to putting edges in edge list once - gives slightly better runtime
    for node, adj_nodes in enumerate(undirected_adj_list):
        for adj_node, adj_weight in adj_nodes:
            edge_list.append((node, adj_node, adj_weight))

    edge_list = sorted(edge_list, key=lambda x: x[2])
    uf = UnionFind(N)

    # print(edge_list)
    for lnode, rnode, weight in edge_list:
        if uf.name(lnode) != uf.name(rnode):
            mst_adj_list[lnode].append((rnode, weight))
            mst_adj_list[rnode].append((lnode, weight))
            uf.union_sets(lnode, rnode)

    # Return the adjacency list for the MST, formatted as a list-of-lists in exactly the same way as undirected_adj_list
    return mst_adj_list




#############################
# CHANGE INPUT FILES FOR PART 2 HERE

#############################

def main(args=[]):
    # WHEN YOU SUBMIT TO THE AUTOGRADER, 
    # PLEASE MAKE SURE THE FOLLOWING FUNCTION LOOKS LIKE:
    # Run('input.txt', 'output')
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