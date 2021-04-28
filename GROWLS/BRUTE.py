import numpy as np
import mmh3
import sys
from collections import defaultdict


class BRUTE:
    def __init__(self, n_nodes, seed=100):
        # Save parameters
        self.n_nodes = n_nodes
        self.seed = seed
        # Initialize in-neighbor graph
        self.in_graph = [[] for _ in range(self.n_nodes)]
        # Keep track of in-degrees
        self.in_deg = [0 for _ in range(n_nodes)]
        # Keep track of nodes that would make cycles
        self.cycle_node = [i for i in range(n_nodes)]
        # Keep track of nodes that the current node would cause a cycle
        self.inv_cycle_node = [i for i in range(n_nodes)]
        # Declare edge list
        self.edges = []
        self.degrees = [0 for _ in range(self.n_nodes)]
        # Initialize sparse graph
        self.sparse_graph = defaultdict(lambda: defaultdict(lambda: [0, 0]))
        self.sparsest_graph = [[] for _ in range(self.n_nodes)]
        # Ordering
        self.taken = [False for _ in range(self.n_nodes)]
        self.orig_node_at_idx = np.full(self.n_nodes, 0)
        self.made_order = False

    # Step 1: Insertion
    def insert_edge(self, u, v):
        self.in_graph[v].append(u)
        self.sparse_graph[min(u, v)][max(u, v)][1] += 1

    def insert(self, u, vector):
        for v in vector:
            self.insert_edge(u, v)

    # Step 3
    def __build_sparse_graph(self):
        for u in range(self.n_nodes):
            for v in range(self.n_nodes):
                if u < v:
                    set_u = set(self.in_graph[u])
                    set_v = set(self.in_graph[v])
                    intersect_size = len(set_u.intersection(set_v))
                    union_size = len(set_u.union(set_v))
                    self.sparse_graph[u][v][0] = intersect_size / union_size if union_size != 0 else 0
                    self.sparse_graph[u][v][0] += self.sparse_graph[u][v][1]

    # Step 4
    def __sort_sparse_graph_edges_by_weight(self):
        for u in self.sparse_graph:
            for v in self.sparse_graph[u]:
                if u < v:
                    weight, _ = self.sparse_graph[u][v]
                    self.edges.append((u, v, weight))
        self.edges.sort(key=lambda edge: edge[2], reverse=True)

    # Step 5
    def __filter_edges(self):
        for u, v, weight in self.edges:
            # print("EDGE:", u, v)
            if self.degrees[u] < 2 and self.degrees[v] < 2 and self.cycle_node[u] != v:
                cn_u = self.cycle_node[u]
                cn_v = self.cycle_node[v]
                self.cycle_node[self.cycle_node[u]] = cn_v
                self.cycle_node[self.cycle_node[v]] = cn_u
                self.degrees[u] += 1
                self.degrees[v] += 1
                self.sparsest_graph[u].append(v)
                self.sparsest_graph[v].append(u)

    def get_order(self):
        self.__build_sparse_graph()
        self.__sort_sparse_graph_edges_by_weight()
        self.__filter_edges()
        start_node = 0
        idx = 0
        while idx < self.n_nodes:
            # print("Idx:", idx)
            # print("N_nodes:", self.n_nodes)
            while start_node < self.n_nodes and (self.degrees[start_node] != 1 or self.taken[start_node]):
                # print("Start_node", start_node)
                if self.degrees[start_node] == 0:
                    self.orig_node_at_idx[idx] = start_node
                    self.taken[start_node] = True
                    idx += 1
                start_node += 1
            if start_node == self.n_nodes:
                break
            # print("Degree of Start_node", self.degrees[start_node])
            self.orig_node_at_idx[idx] = start_node
            self.taken[start_node] = True
            idx += 1
            cur_node = start_node
            # print(self.degrees[cur_node])
            next_node = self.sparsest_graph[cur_node][0]
            while self.degrees[next_node] == 2:
                self.orig_node_at_idx[idx] = next_node
                self.taken[next_node] = True
                idx += 1

                # Moving on
                temp_cur_node = cur_node
                cur_node = next_node
                next_node = list(filter(lambda node: node != temp_cur_node, self.sparsest_graph[next_node]))[0]
            if idx < self.n_nodes:
                self.orig_node_at_idx[idx] = next_node
                self.taken[next_node] = True
            idx += 1
            start_node += 1

        return self.orig_node_at_idx









