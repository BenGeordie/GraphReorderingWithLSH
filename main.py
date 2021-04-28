import time
import numpy as np
import math
from utils.ReadGraph import ReadGraph
from utils.GOrderObjective import gorder_objective
from algorithms.hubsorting import HubSorting
from algorithms.MinhashSortingK2 import MinhashSortingK2
from algorithms.MinhashSortingK3 import MinhashSortingK3
from algorithms.MinhashGreedyEdges import MinhashGreedyEdges


def test(graph, test_name, model, *args):
    print('------------------------------------------')
    print(test_name)
    print('------------------------------------------')
    times = [0.0] * 4
    times[0] = time.time()
    _model = model(*args)
    times[1] = time.time()
    for i, vec in enumerate(graph):
        _model.insert(i, vec)
    times[2] = time.time()
    ordering = _model.get_order()
    times[3] = time.time()
    ordering_inverse = np.argsort(ordering)
    gorder_obj_score = gorder_objective(5, lambda: ordering, lambda node: [ordering_inverse[nbr] for nbr in graph[node]])

    print(f'{test_name} | GOrder Objective Score: {gorder_obj_score}')
    print(f'{test_name} | # Operations: {_model.get_operation_count()}\n')
    print()


class NoOp:
    def __init__(self, n_nodes):
        self.n_nodes = n_nodes

    def insert(self, i, vec):
        return

    def get_order(self):
        return list(range(self.n_nodes))

    def get_operation_count(self):
        return 0


def main():
    graph = ReadGraph("datasets/facebook_combined.txt").export_arr()
    n = len(graph)
    m = sum([len(vec) for vec in graph])

    # No Reordering
    test(graph, "No Reordering", NoOp, len(graph))

    # GOrder
    print('------------------------------------------')
    print("GOrder")
    print('------------------------------------------')
    Gorder = ReadGraph("datasets/facebook_combined_Gorder.txt")
    ground_truth = Gorder.export_dict()
    ground_truth_keys = Gorder.export_keys()
    gorder_obj_Gorder = gorder_objective(5, lambda: ground_truth_keys, lambda node: ground_truth[node])
    print(f'GOrder | GOrder Objective Score : {gorder_obj_Gorder}')
    print(f"GOrder | # operations: {sum([len(vec) ** 2 for vec in graph])}\n")

    # Hub Sorting
    test(graph, "Hub Sorting", HubSorting, len(graph))

    # Minhash + Greedy Edge Selection, L = 5, K = 2
    n_tables = 5
    n_hashes = 2
    test(graph, f"Minhash + Greedy Edge Selection, L = {n_tables}, K = {n_hashes}", MinhashGreedyEdges,
         n_tables, n_hashes, len(graph))

    # Minhash + Greedy Edge Selection, L = 10, K = 2
    n_tables = 10
    n_hashes = 2
    test(graph, f"Minhash + Greedy Edge Selection, L = {n_tables}, K = {n_hashes}", MinhashGreedyEdges,
         n_tables, n_hashes, len(graph))

    # Minhash Sorting, K = 2
    test(graph, "Minhash Sorting, K = 2", MinhashSortingK2, len(graph))

    # Minhash Sorting, K = 3
    test(graph, "Minhash Sorting, K = 3", MinhashSortingK3, len(graph))




main()


