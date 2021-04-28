import matplotlib.pyplot as plt
from collections import defaultdict


def evaluate(title, get_graph_nodes, get_node_out_nbrs, graph=True):
    total = 0
    sum_of_squares = 0
    max_overlap = 0
    graph_nodes = get_graph_nodes()
    min_overlap = len(graph_nodes)
    histogram_data = []

    # create table of in-degrees
    indegree_table = defaultdict(lambda: [])
    for node in get_graph_nodes():
        out_nbrs = get_node_out_nbrs(node)
        for out_nbr in out_nbrs:
            if node != out_nbr:
                indegree_table[out_nbr].append(node)

    for node in graph_nodes:
        adj_set_1 = set(indegree_table[node])
        adj_set_2 = set(indegree_table[(node + 1) % len(graph_nodes)])
        overlap = len(adj_set_1.intersection(adj_set_2))
        max_overlap = max(max_overlap, overlap)
        min_overlap = min(min_overlap, overlap)
        total += overlap
        sum_of_squares += overlap ** 2
        histogram_data.append(overlap)
    title_str = f'|| Evaluating: {title} ||'
    print('-' * len(title_str))
    print(title_str)
    print('-' * len(title_str))
    print(f'Number of adjacent node pairs with 0 overlap: {histogram_data.count(0)}')
    print(f'Average # overlapping neighbors between adjacent nodes: {total / len(graph_nodes)}')
    print(f'Average # overlapping neighbors RMS between adjacent nodes: {(sum_of_squares / len(graph_nodes)) ** 0.5}')
    print(f'Maximum # overlapping neighbors between adjacent nodes: {max_overlap}')
    print(f'Minimum # overlapping neighbors between adjacent nodes: {min_overlap}')
    if graph:
        plt.xlabel("# overlapping neighbors between adjacent nodes")
        plt.ylabel("# adjacent node pairs")
        plt.hist(histogram_data, bins=[0, 1, 2, 5, 10, 25, 70, 200])
        plt.title(f'{title} bins [0, 1, 2, 5, 10, 25, 70, 200]')
        plt.ylim(0, 1000)
        plt.xlim(0, 175)
        plt.yticks([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
        plt.show()
        plt.xlabel("# overlapping neighbors between adjacent nodes")
        plt.ylabel("# adjacent node pairs")
        plt.hist(histogram_data, bins=210)
        plt.title(f'{title}')
        plt.ylim(0, 1000)
        plt.xlim(0, 200)
        plt.yticks([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
        plt.show()

