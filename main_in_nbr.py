from GRL import GRL
from GRL2 import GRL2
from GRL2InNbr import GRL2InNbr
from GRL2InNbr_3minhashes import GRL2InNbr3Min
from GRL2InNbrSRP import GRL2InNbrSRP
from GRL2InNbrMin import GRL2InNbrMin
import numpy as np
from GRL3 import GRL3
from RandomReorder import RandomReorder
from EgoFacebookGraph import EgoFacebookGraph
from EvaluateGraphOrder import evaluate
from EvaluateGraphOrderInNbr import evaluate as evalInNbr
from Diagnostics import pairwise_overlap
import time
import cProfile
import flameprof
from GOrderObjective import gorder_objective
from GROWLS.GROWLSW import GROWLSW
from GROWLS.GROWLSE import GROWLSE
from GROWLS.BRUTE import BRUTE
from hubsorting import HubSorting
from degsorting import DegSorting


# https://github.com/rmax/databrewer-recipes/blob/master/bigann.yaml


def test(graph, test_name, model, *args):
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

    print('------------------------------------------')
    print(test_name)
    print('------------------------------------------')
    print(f'{test_name} initialized in {times[1] - times[0]} seconds')
    print(f'{test_name} hashed in {times[2] - times[1]} seconds')
    print(f'{test_name} ordered  in {times[3] - times[2]} seconds')
    print(f'{test_name} finished in {times[3] - times[0]} seconds')
    print(f'{test_name} GOrder Objective: {gorder_obj_score}\n')
    print()

# TODO: check the distribution of GOrder scores for each window. Does sorting have a small number of very high score clusters?
# TODO: Current weights are jaccard similarity. We have to normalize with the numbers of siblings/neighbors/degree that each of the nodes have. How good is this estimation, really??
# TODO: Implement random walk too.
# TODO: Theoretical guarantee of sorting.
# TODO: Implement lightweight methods.
# TODO: To detect cycles when picking highest weight edges, keep track of the cycle-node for each node with degree 1.
#  E.g. if we first pick an edge u, v, then u and v will both have degree 1, and their cycle-nodes are v and u
#  respectively. Now every time they link with another edge, their cycle-nodes are passed on. We also have an inverse
#  cycle-node array, mapping what other node the indexed node is the cycle-node of. So for example, if we have a new
#  edge v, w, then cycle_node[w] = cycle_node[v] and cycle_node[inverse_cycle_node[v]] = w.

class NoOp:
    def __init__(self, n_nodes):
        self.n_nodes = n_nodes

    def insert(self, i, vec):
        return

    def get_order(self):
        return list(range(self.n_nodes))


def main():
    graph = EgoFacebookGraph("facebook_combined.txt").export_arr()
    test(graph, "No Op", NoOp, len(graph))
    test(graph, "Plain sorting GRL2InNbr", GRL2InNbr, len(graph))
    test(graph, "Plain sorting GRL2InNbr3Min", GRL2InNbr3Min, len(graph))
    # graph = EgoFacebookGraph("facebook_combined_randomly_ordered.txt").export_arr()
    # test(graph, "GRL2 In Nbr Standard (randomly ordered graph)", GRL2InNbr, len(graph))
    # test(graph, "Greedy walk with 5 hash tables and 1 minhash each", GROWLS, 5, 1, len(graph))
    # test(graph, "Greedy walk with 5 hash tables and 2 concatenated minhashes", GROWLS, 5, 2, len(graph))
    # test(graph, f"Brute force", BRUTE, len(graph))
    # n_tables = 4
    # n_hashes = 1
    # test(graph, f"Greedy walk with {n_tables} hash tables and {n_hashes} concatenated minhashes", GROWLSW, n_tables, n_hashes, len(graph))
    # n_tables = 2
    # n_hashes = 1
    # test(graph, f"Greedy edge selection with {n_tables} hash tables", GROWLSE, n_tables, n_hashes, len(graph))
    # n_tables = 3
    # n_hashes = 1
    # test(graph, f"Greedy edge selection with {n_tables} hash tables", GROWLSE, n_tables, n_hashes, len(graph))
    # n_tables = 4
    # n_hashes = 1
    # test(graph, f"Greedy edge selection with {n_tables} hash tables", GROWLSE, n_tables, n_hashes, len(graph))
    test(graph, "Hub Sorting", HubSorting, len(graph))
    test(graph, "Degree Sorting", DegSorting, len(graph))
    n_tables = 10
    n_hashes = 1
    test(graph, f"Greedy edge selection with {n_tables} hash tables", GROWLSE, n_tables, n_hashes, len(graph))
    n_tables = 5
    n_hashes = 2
    test(graph, f"Greedy edge selection with {n_tables} hash tables and {n_hashes} hashes", GROWLSE, n_tables, n_hashes, len(graph))
    n_tables = 6
    n_hashes = 2
    test(graph, f"Greedy edge selection with {n_tables} hash tables and {n_hashes} hashes", GROWLSE, n_tables, n_hashes, len(graph))
    n_tables = 7
    n_hashes = 2
    test(graph, f"Greedy edge selection with {n_tables} hash tables and {n_hashes} hashes", GROWLSE, n_tables, n_hashes, len(graph))
    n_tables = 8
    n_hashes = 2
    test(graph, f"Greedy edge selection with {n_tables} hash tables and {n_hashes} hashes", GROWLSE, n_tables, n_hashes, len(graph))
    n_tables = 9
    n_hashes = 2
    test(graph, f"Greedy edge selection with {n_tables} hash tables and {n_hashes} hashes", GROWLSE, n_tables, n_hashes, len(graph))
    n_tables = 10
    n_hashes = 2
    test(graph, f"Greedy edge selection with {n_tables} hash tables and {n_hashes} hashes", GROWLSE, n_tables, n_hashes, len(graph))
    n_tables = 20
    n_hashes = 1
    test(graph, f"Greedy edge selection with {n_tables} hash tables", GROWLSE, n_tables, n_hashes, len(graph))
    n_tables = 20
    n_hashes = 3
    test(graph, f"Greedy edge selection with {n_tables} hash tables and {n_hashes} hashes", GROWLSE, n_tables, n_hashes, len(graph))
    # n_tables = 50
    # n_hashes = 1
    # test(graph, f"Greedy edge selection with {n_tables} hash tables", GROWLSE, n_tables, n_hashes, len(graph))

    # graph = EgoFacebookGraph("facebook_combined_randomly_ordered.txt").export_arr()
    # test(graph, "GROWLS (randomly ordered graph)", GROWLS, 10, 3, len(graph))
    # graph = EgoFacebookGraph("facebook_combined.txt").export_arr()
    # test(graph, "GRL2 In Nbr 3 Min (original graph)", GRL2InNbr3Min, len(graph))
    # graph = EgoFacebookGraph("facebook_combined_randomly_ordered.txt").export_arr()
    # test(graph, "GRL2 In Nbr 3 Min (randomly ordered graph)", GRL2InNbr3Min, len(graph))
    # for p in [5, 10, 25, 100]:
    #     test(graph, f'GRL2 In Nbr Min p={p}', GRL2InNbrMin, len(graph), p)
    # for p, d in [(100, 30)]:
    #     test(graph, f'GRL2 In Nbr SRP p={p} d={d}', GRL2InNbrSRP, len(graph), p, d)



main()


