from collections import defaultdict


def gorder_objective(w, get_graph_nodes, get_node_out_nbrs):
    # create table of in-degrees
    indegree_table = defaultdict(lambda:[])
    for node in get_graph_nodes():
        out_nbrs = get_node_out_nbrs(node)
        for out_nbr in out_nbrs:
            if node != out_nbr:
                indegree_table[out_nbr].append(node)

    # Compute the objective function score
    s = 0
    n = 0
    for node in get_graph_nodes():
        for j in range(node - w, node):
            if j < 0:
                continue
            # compute S_s(u,v)
            for x in indegree_table[node]:
                for y in indegree_table[j]:
                    if x == y:
                        s += 1

            # Compute S_n(u,v)
            if j in get_node_out_nbrs(node):
                n += 1
            if node in get_node_out_nbrs(j):
                n += 1
    print(f'S_s: {s}, S_n: {n}')
    return s + n


