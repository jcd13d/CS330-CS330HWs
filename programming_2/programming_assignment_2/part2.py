import sys
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from pa2_starter import readGraph, dijkstra, make_undirected_graph, kruskal

"""
What we want:
    * TWR and MDF for each input.txt graph
        * TWR = cost(T_sp)/cost(T_mst)
        * MDR = max(d_tmst(s, u)/d_tsp(s, u))
    * output
        * table of these values
        * scatter plots 
"""


def graph_total_weight(adj_list):
    # iterate through all edges and add up weights
    # have to be careful not to count both of the same edge twice? two directional edges
    weight_counted = [[False]*len(adj_list) for i in range(len(adj_list))]
    total_weight = 0

    for node, adj_nodes in enumerate(adj_list):
        for adj_node, weight in adj_nodes:
            if not weight_counted[node][adj_node]:
                total_weight += weight
                weight_counted[node][adj_node] = True
                weight_counted[adj_node][node] = True

    return total_weight


def get_twr(tsp, tmst):
    return graph_total_weight(tsp) / graph_total_weight(tmst)


def get_mdr(tsp_distances, tmst_distances):
    # calc d_tmst(s, u)/d_tsp(s, u) for each u != s (ignore distance zero)
    # can run dijkstra on mst to get distances dict
    assert len(tsp_distances) == len(tmst_distances)
    dist_ratios = [0]*len(tsp_distances)

    for node_sp, distance_sp in tsp_distances.items():
        if distance_sp != 0:
            dist_ratios[node_sp] = tmst_distances[node_sp] / distance_sp

    return max(dist_ratios)


def run_part_2(input_file):

    N, m, s, adj_list = readGraph(input_file)
    distances_sp, parents_sp, sp = dijkstra(N, m, s, adj_list, return_adj_list=True)
    undirected_adj_list = make_undirected_graph(N, adj_list)
    mst = kruskal(N, m, undirected_adj_list)
    distances_mst, _ = dijkstra(N=N, m=m, s=s, adj_list=mst)     # source shoudlnt

    twr = get_twr(sp, mst)
    mdr = get_mdr(distances_sp, distances_mst)

    return twr, mdr


def plots(data, output, show=False):
    for graph_name, (twr, mdr) in data.items():
        plt.scatter(twr, mdr, label=graph_name)
    plt.legend()
    plt.title("TWR vs MDR for Different Graphs")
    plt.ylabel("Maximum Distance Ratio")
    plt.xlabel("Total Weight Ratio")
    plt.grid()
    if show:
        plt.show()
    plt.savefig(os.path.join(output, "chart.jpg"))


if __name__ == "__main__":
    directory = glob.glob(os.path.join(sys.argv[1], '*.txt'))
    output_dir = sys.argv[2]
    output_data = {}

    for file_path in directory:
        file_name = os.path.basename(file_path).split(".")[0]
        output_data[file_name] = run_part_2(file_path)

    for k, (twr, mdr) in output_data.items():
        print("{0}: Total Weight Ratio: {1:.4f}, Max Distance Ratio: {2:.4f}".format(k, twr, mdr))

    plots(output_data, output=output_dir)








