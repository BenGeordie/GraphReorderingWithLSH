import numpy as np
import mmh3
import math
import sys
from collections import defaultdict


class MinhashGreedyEdges:
    def __init__(self, l_tables, k_concat, n_nodes, seed=100):
        self.numedges = 0
        # Save parameters
        self.num_tables = l_tables
        self.num_concat = k_concat
        self.n_nodes = n_nodes
        self.seed = seed
        # Initialize hash functions
        self.hash_fns = [self.__make_hash_fn(i) for i in range(self.num_tables * self.num_concat)]
        # Initialize hash array
        self.hashes = [[sys.maxsize for _ in range(self.num_tables * self.num_concat)] for _ in range(self.n_nodes)]
        # Keep track of in-degrees
        self.in_deg = [0 for _ in range(n_nodes)]
        # Keep track of nodes that would make cycles
        self.cycle_node = [i for i in range(n_nodes)]
        # Keep track of nodes that the current node would cause a cycle
        self.inv_cycle_node = [i for i in range(n_nodes)]
        # Declare hash table
        self.hash_tables = [defaultdict(lambda: []) for _ in range(self.num_tables)]
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

        self.pairwise_collisions = 0
        self.m_hat = 0

    def __make_hash_fn(self, i):
        return lambda item: mmh3.hash(str(item), seed=self.seed * i, signed=False)

    # Step 1: Insertion
    def insert_edge(self, u, v):
        self.numedges += 1
        for i, hash_fn in enumerate(self.hash_fns):
            self.hashes[v][i] = min(self.hashes[v][i], hash_fn(u))
        self.in_deg[v] += 1
        self.sparse_graph[min(u, v)][max(u, v)][1] += 1

    def insert(self, u, vector):
        for v in vector:
            self.insert_edge(u, v)

    # Step 2
    def __build_hash_table(self):
        for i, min_hashes in enumerate(self.hashes):
            for j in range(self.num_tables):
                _hash = ''.join([str(min_hashes[j * self.num_concat + k]) for k in range(self.num_concat)])
                self.hash_tables[j][_hash].append(i)

    # Step 3
    def __build_sparse_graph(self):
        for t_num, table in enumerate(self.hash_tables):
            for bucket in table.values():
                if len(bucket) > 0:
                    for i in bucket:
                        for j in bucket:
                            self.pairwise_collisions += 1
                            if i < j:
                                self.sparse_graph[i][j][0] += 1
        for u in self.sparse_graph:
            for v in self.sparse_graph[u]:
                jac = self.sparse_graph[u][v][0] / self.num_tables
                # print("Jac:", jac)
                # print("Indeg total:", self.in_deg[u] + self.in_deg[v])
                sn = self.sparse_graph[u][v][1]
                self.sparse_graph[u][v][0] = jac * (self.in_deg[u] + self.in_deg[v]) / (1 + jac) + sn
                # self.sparse_graph[u][v][0] = (self.in_deg[u] + self.in_deg[v]) / (1 + jac)

    # Step 4
    def __sort_sparse_graph_edges_by_weight(self):
        for u in self.sparse_graph:
            for v in self.sparse_graph[u]:
                if u < v:
                    weight, _ = self.sparse_graph[u][v]
                    self.edges.append((u, v, weight))
        self.edges.sort(key=lambda edge: edge[2], reverse=True)
        self.m_hat = len(self.edges)

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
        self.__build_hash_table()
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

    def get_operation_count(self):
        p = self.pairwise_collisions
        m = self.m_hat
        return math.floor(p + m * math.log(m, 2))









