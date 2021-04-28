import numpy as np
import mmh3
import sys
from collections import defaultdict


class GROWLSW:
    def __init__(self, l_tables, k_concat, n_nodes, seed=100):
        # Save parameters
        self.num_tables = l_tables
        self.num_concat = k_concat
        self.n_nodes = n_nodes
        self.seed = seed
        # Initialize hash functions
        self.hash_fns = [self.__make_hash_fn(i) for i in range(self.num_tables * self.num_concat)]
        # Initialize hash array
        self.hashes = [[sys.maxsize for _ in range(self.num_tables * self.num_concat)] for _ in range(self.n_nodes)]
        self.in_deg = [0 for _ in range(n_nodes)]
        # Declare hash table
        self.hash_tables = [defaultdict(lambda: []) for _ in range(self.num_tables)]
        # Declare edge list
        self.edges = []
        self.edge_is_valid = []
        # Declare degree bookkeeping
        self.degrees = [0 for _ in range(self.n_nodes)]
        # Initialize sparse graph
        self.sparse_graph = defaultdict(lambda: defaultdict(lambda: [0, 0]))
        self.sparse_graph_filtered = [[] for _ in range(self.n_nodes)]
        self.orig_node_at_idx = np.full(self.n_nodes, 0)
        self.made_order = False

    def __make_hash_fn(self, i):
        return lambda item: mmh3.hash(str(item), seed=self.seed * i, signed=False)

    # Step 1: Insertion
    def insert_edge(self, u, v):
        for i, hash_fn in enumerate(self.hash_fns):
            self.hashes[v][i] = min(self.hashes[v][i], hash_fn(u))
        self.in_deg[v] += 1

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
        edge_id = 0
        for t_num, table in enumerate(self.hash_tables):
            for bucket in table.values():
                if len(bucket) > 0:
                    for i in bucket:
                        for j in bucket:
                            if j < i:
                                # bidirectional
                                self.degrees[i] += 1
                                self.degrees[j] += 1
                                self.sparse_graph[i][j][0] += 1
                                self.sparse_graph[j][i][0] += 1
                                if self.sparse_graph[i][j][0] == 1:
                                    self.sparse_graph[i][j][1] = edge_id
                                    self.sparse_graph[j][i][1] = edge_id
                                    edge_id += 1
        for u in self.sparse_graph:
            for v in self.sparse_graph[u]:
                jac = self.sparse_graph[u][v][0] / self.num_tables
                self.sparse_graph[u][v][0] = jac * (self.in_deg[u] + self.in_deg[v]) / (1 + jac)

    # Step 4
    def __sort_sparse_graph_edges_by_weight(self):
        for u in self.sparse_graph:
            for v in self.sparse_graph[u]:
                if u < v:
                    weight, edge_id = self.sparse_graph[u][v]
                    self.edges.append((u, v, weight, edge_id))
        self.edges.sort(key=lambda edge: edge[2], reverse=True)
        self.edge_is_valid = np.full(len(self.edges), True)

    def __is_valid(self, edge):
        _, _, _, edge_id = edge
        return self.edge_is_valid[edge_id]

    def __find_heaviest_valid_nbr(self, node):
        max_nbr = None
        max_weight = 0
        for nbr in self.sparse_graph[node]:
            if self.sparse_graph[node][nbr][1] > max_weight:
                max_weight = self.sparse_graph[node][nbr][1]
                max_nbr = nbr
        return max_nbr, max_weight

    def __invalidate_single_edge(self, u, v):
        _, edge_id = self.sparse_graph[u][v]
        # Remove from sparse graph (both directions)
        self.sparse_graph[u].pop(v)
        self.sparse_graph[v].pop(u)
        # Set invalid edges array entry to invalid
        self.edge_is_valid[edge_id] = False

    def __has_valid_nbr(self, node):
        return len(self.sparse_graph[node]) != 0

    def __invalidate_edges_of(self, node):
        # For each edge, invalidate_single_edge
        for nbr in self.sparse_graph[node]:
            _, edge_id = self.sparse_graph[node][nbr]
            self.sparse_graph[nbr].pop(node)
            self.edge_is_valid[edge_id] = False
        self.sparse_graph.pop(node)
        return

    def __decide_direction(self, edge):
        u, v, _, _ = edge
        self.__invalidate_single_edge(u, v)
        _, max_weight_u = self.__find_heaviest_valid_nbr(u)
        _, max_weight_v = self.__find_heaviest_valid_nbr(v)
        if max_weight_u > max_weight_v:
            self.__invalidate_edges_of(v)
            return v, u
        else:
            self.__invalidate_edges_of(u)
            return u, v

    def __get_heaviest_valid_nbr(self, node):
        v, weight = self.__find_heaviest_valid_nbr(node)
        self.__invalidate_edges_of(node)
        return v

    # TODO: Somehow include lone nodes?
    def get_order(self):
        self.__build_hash_table()
        self.__build_sparse_graph()
        self.__sort_sparse_graph_edges_by_weight()
        count_disconnect = 0
        order_idx = 0
        edge_idx = 0
        edges_len = len(self.edges)
        while order_idx < self.n_nodes and edge_idx < edges_len:
            should_break = False
            while not should_break and not self.__is_valid(self.edges[edge_idx]):
                edge_idx += 1
                if edge_idx == edges_len:
                    should_break = True
            if should_break:
                break
            u, v = self.__decide_direction(self.edges[edge_idx])
            self.orig_node_at_idx[order_idx] = u
            order_idx += 1
            self.orig_node_at_idx[order_idx] = v
            order_idx += 1
            while self.__has_valid_nbr(v):
                v = self.__get_heaviest_valid_nbr(v)
                self.orig_node_at_idx[order_idx] = v
                order_idx += 1
            self.__invalidate_edges_of(v)
            count_disconnect += 1

        if edge_idx == edges_len and order_idx < self.n_nodes:
            for node in self.sparse_graph:
                self.orig_node_at_idx[order_idx] = node
                order_idx += 1
            for node, degree in enumerate(self.degrees):
                if degree == 0:
                    self.orig_node_at_idx[order_idx] = node
                    order_idx += 1
        print(f"Disconnected {count_disconnect} times.")
        return self.orig_node_at_idx

    def get_ordering(self):
        if not self.made_order:
            self.get_order()
        ordering = np.full(self.n_nodes, 0)
        for order, node in enumerate(self.orig_node_at_idx):
            ordering[node] = order
        return ordering

    # def __filter_edge(self, edge):
    #     u, v, _ = edge
    #     if self.degrees[u] < 2 and self.degrees[v] < 2:
    #         self.degrees[u] += 1
    #         self.degrees[v] += 1
    #         self.sparse_graph_filtered[u].append(v)
    #         return True
    #     return False
    #
    # def __filter_sparse_graph_edges(self):
    #     self.sparse_graph = None
    #     self.edges = filter(self.__filter_edge, self.edges)
    #
    # def __make_ordering(self):
    #     ordering = [0 for _ in range(self.n_nodes)]
    #     nodes = np.argsort(self.degrees)
    #
    #     def __walk_sparse_graph():
    #
    #         return
    #
    #     for i, node in enumerate(nodes):
    #         if self.degrees[node] == 0:
    #             ordering[i] = node
    #         else:
    #             if self.degrees[node] == 1:
    #                 __walk_sparse_graph()
    #             if self.degrees[node] == 2:
    #                 v = self.sparse_graph_filtered[node].pop()
    #                 self.sparse_graph_filtered[v].remove(node)
    #                 __walk_sparse_graph()

    # TODO: Scratch this. Instead, prevent cycles by doing walks in the edge filtering process.
    # The idea is, we still sort the edges by weights, and we still have a degrees mapping, but we will also keep
    # the first node so that we don't have a cycle.
    # However, instead of just going through this sorted list of edges, we only use this sorted list of edges
    # to get an edge to start with if we don't have any.
    # We then just do a walk from node to node, using the max valid edge each time.

    # def get_order(self):
    #     return



