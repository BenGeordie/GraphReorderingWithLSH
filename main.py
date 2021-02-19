from GRL import GRL
from RandomReorder import RandomReorder
from EgoFacebookGraph import EgoFacebookGraph
from EvaluateGraphOrder import evaluate


def main():
    graph = EgoFacebookGraph("facebook_combined.txt").export_arr()
    grl = GRL(1000000, len(graph))
    rr = RandomReorder(len(graph))
    for i, vec in enumerate(graph):
        grl.insert(i, vec)
        rr.insert(i, vec)

    evaluate("Random Reordering", rr.get_order(), lambda x: graph[x])
    evaluate("GRL Reordering", grl.get_order(), lambda x: graph[x])


main()

