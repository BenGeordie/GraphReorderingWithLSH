from collections import defaultdict
import math
import numpy as np
import sys
import mmh3


class Mmh3:
    def __init__(self, seed=100):
        self.seed = seed

    def get_hash(self, item):
        return mmh3.hash(str(item), seed=self.seed)


class MinhashSortingK3:
    def __init__(self, seed=100):
        self.n_nodes = 2
        self.hasher1 = Mmh3(seed=seed)
        self.hasher2 = Mmh3(seed=seed * 2)
        self.hasher3 = Mmh3(seed=seed * 3)

        # Initialize array that would be filled by hashes
        self.min_hashes = np.empty((2, 3), dtype=int)
        # print(np.shape(self.min_hashes))
        self.m = 0

    def insert_edge(self, line):
        self.m += 1
        if not (self.m % 100000):
            print(self.m)
        u, v = [int(node) for node in line.split()]
        max_idx = max(u, v)
        if self.n_nodes <= max_idx:
            self.min_hashes = np.pad(
                self.min_hashes,
                ((0, max_idx + 1 - self.n_nodes), (0, 0)),
                'constant', constant_values=sys.maxsize)
            self.n_nodes = max_idx + 1
        # print(np.shape(self.min_hashes))
        self.min_hashes[v][0] = min(self.min_hashes[v][0], self.hasher1.get_hash(u))
        self.min_hashes[v][1] = min(self.min_hashes[v][1], self.hasher2.get_hash(u))
        self.min_hashes[v][2] = min(self.min_hashes[v][2], self.hasher3.get_hash(u))

    def get_order(self):
        mins1 = defaultdict(lambda: sys.maxsize)
        mins2 = defaultdict(lambda: sys.maxsize)
        mins3 = defaultdict(lambda: sys.maxsize)
        order_arr_str = np.empty(self.n_nodes, dtype=str)
        for i in range(self.n_nodes):
            [hash1, hash2, hash3] = self.min_hashes[i]
            mins1[hash3] = min(mins1[hash2], hash1)
            mins2[hash1] = min(mins2[hash1], hash2)
            mins3[hash2] = min(mins3[hash2], hash3)
        for i in range(self.n_nodes):
            [hash1, hash2, hash3] = self.min_hashes[i]
            # self.order_arr_str[i] = str(mins1[mins3[mins2[hash1]]]) + str(mins3[mins2[hash1]]) + str(mins2[hash1]) + str(hash1) + str(hash2) + str(hash3)
            order_arr_str[i] = str(mins3[mins2[hash1]]) + str(mins2[hash1]) + str(hash1) + str(hash2) + str(hash3)
        sort_index = np.argsort(order_arr_str)
        return sort_index

    def get_operation_count(self):
        return math.floor(self.m + self.n_nodes * math.log(self.n_nodes, 2))

