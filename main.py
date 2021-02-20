from GRL import GRL
from RandomReorder import RandomReorder
from EgoFacebookGraph import EgoFacebookGraph
from EvaluateGraphOrder import evaluate
from Diagnostics import pairwise_overlap
import time


def main():
    graph = EgoFacebookGraph("facebook_combined.txt").export_arr()
    # pairwise_overlap("Ego Facebook", graph)

    grl_start = time.time()
    grl = GRL(100000, len(graph))
    for i, vec in enumerate(graph):
        grl.insert(i, vec)
    grl_order = grl.get_order()
    grl_end = time.time()
    evaluate("GRL Reordering", grl_order, lambda x: graph[x])
    print(f'GRL finished in {grl_end - grl_start} seconds')

    rr_start = time.time()
    rr = RandomReorder(len(graph))
    for i, vec in enumerate(graph):
        rr.insert(i, vec)
    rr_order = rr.get_order()
    rr_end = time.time()
    evaluate("Random Reordering", rr_order, lambda x: graph[x])
    print(f'Random Reordering finished in {rr_end - rr_start} seconds')

    ground_truth = EgoFacebookGraph("facebook_combined_Gorder.txt").export_arr()
    evaluate("Gorder", list(range(len(ground_truth))), lambda x: graph[x])
    print(f'Gorder finished in 0.013517 seconds')


main()

