from GRL import GRL
from GRL2 import GRL2
from GRL3 import GRL3
from RandomReorder import RandomReorder
from EgoFacebookGraph import EgoFacebookGraph
from EvaluateGraphOrder import evaluate
from Diagnostics import pairwise_overlap
import time
import cProfile
import flameprof


# https://github.com/rmax/databrewer-recipes/blob/master/bigann.yaml

def main():
    graph = EgoFacebookGraph("facebook_combined_randomly_ordered.txt").export_arr()
    print(len(graph))
    evaluate("No reordering", list(range(len(graph))), lambda x: graph[x], graph=False)
    print('\n')
    # pairwise_overlap("Ego Facebook", graph)

    grl_start = time.time()
    grl = GRL(50000, len(graph))
    for i, vec in enumerate(graph):
        grl.insert(i, vec)
    grl_order = grl.get_order()
    grl_end = time.time()
    evaluate("GRL Reordering", grl_order, lambda x: graph[x], graph=False)
    print(f'GRL finished in {grl_end - grl_start} seconds\n')

    grl2_start = time.time()
    grl2 = GRL2(len(graph))
    grl2_init = time.time()
    for i, vec in enumerate(graph):
        grl2.insert(i, vec)
    grl2_hash = time.time()
    grl2_order = grl2.get_order()
    grl2_end = time.time()
    evaluate("GRL2 Reordering", grl2_order, lambda x: graph[x])
    print(f'GRL2 initialized in {grl2_init - grl2_start} seconds')
    print(f'GRL2 hashed in {grl2_hash - grl2_init} seconds')
    print(f'GRL2 ordered  in {grl2_end - grl2_hash} seconds')
    print(f'GRL2 finished in {grl2_end - grl2_start} seconds\n')

    # grl3_start = time.time()
    # grl3 = GRL3(len(graph))
    # grl3_init = time.time()
    # print(f'GRL3 initialized in {grl3_init - grl3_start} seconds')
    # for i, vec in enumerate(graph):
    #     grl3.insert(i, vec)
    # grl3_hash = time.time()
    # print(f'GRL3 hashed in {grl3_hash - grl3_init} seconds')
    # grl3_order = grl3.get_order()
    # grl3_end = time.time()
    # print(f'GRL3 ordered  in {grl3_end - grl3_hash} seconds')
    # evaluate("GRL3 Reordering", grl3_order, lambda x: graph[x])
    # print(f'GRL3 finished in {grl3_end - grl3_start} seconds\n')

    # rr_start = time.time()
    # rr = RandomReorder(len(graph))
    # for i, vec in enumerate(graph):
    #     rr.insert(i, vec)
    # rr_order = rr.get_order()
    # rr_end = time.time()
    # evaluate("Random Reordering", rr_order, lambda x: graph[x])
    # print(f'Random Reordering finished in {rr_end - rr_start} seconds\n')

    # Used Gorder with default parameters. Gorder implemented in CPP.
    Gorder = EgoFacebookGraph("facebook_combined_Gorder.txt")
    ground_truth = Gorder.export_dict()
    ground_truth_keys = Gorder.export_keys()
    print(len(ground_truth))
    evaluate("Gorder", ground_truth_keys, lambda x: ground_truth[x])
    print(f'Gorder finished in 0.01367 seconds\n')

main()