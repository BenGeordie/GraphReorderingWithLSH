import networkx as nx
import time
from GRL2InNbrForGraphFormat import GRL2InNbr


def main():
    f = open("twitter_rv.net", 'r')
    file_lines = f

    print("PageRank without reordering")
    # Build graph
    start_building_graph = time.time()
    G = nx.Graph()
    for line in file_lines:
        [u, v] = line.split('\t')
        G.add_edge(int(u), int(v))
    end_building_graph = time.time()
    print(f"Time taken to build graph: {end_building_graph - start_building_graph}")
    start_no_reordering = time.time()
    nx.pagerank(G)
    end_no_reordering = time.time()
    print(f"Time taken to run pagerank without reordering: {end_no_reordering - start_no_reordering}")

    # Count number of nodes
    print("Reordering")
    start_counting_nodes = time.time()
    prev = ''
    count = 0
    for line in file_lines:
        [u, _] = line.split('\t')
        if u != prev:
            prev = u
            count += 1
    end_counting_nodes = time.time()
    print(f"Time taken to count nodes: {end_counting_nodes - start_counting_nodes}")

    # Initialize GRL
    start_insert_edges_to_grl = time.time()
    GRL = GRL2InNbr(count)
    for line in file_lines:
        GRL.insert_line(line)
    end_insert_edges_to_grl = time.time()
    print(f"Time taken to insert edges to GRL: {end_insert_edges_to_grl - start_insert_edges_to_grl}")
    start_grl = time.time()
    ordering = GRL.get_order()
    end_grl = time.time()
    print(f"Time taken to reorder: {end_grl - start_grl}")

    print("PageRank with reordering")
    start_with_reordering = time.time()
    # Build graph
    GR = nx.Graph()
    for line in file_lines:
        [u, v] = line.split('\t')
        GR.add_edge(ordering[int(u)], ordering[int(v)])
    nx.pagerank(GR)
    end_with_reordering = time.time()
    print(f"Time taken to run pagerank without reordering: {end_with_reordering - start_with_reordering}")


main()

