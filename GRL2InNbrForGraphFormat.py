from collections import defaultdict

from MinHash import Hash
import numpy
import sys
import mmh3


class Mmh3:
    def __init__(self, seed=100):
        self.seed = seed

    def get_hash(self, item):
        return mmh3.hash(item, seed=self.seed, signed=False)


class GRL2InNbr:
    def __init__(self, n_nodes, seed=100):
        self.n_nodes = n_nodes
        self.hasher1 = Mmh3(seed=seed)
        self.hasher2 = Mmh3(seed=seed * 2)

        # Initialize array that would be filled by hashes
        self.order_arr = [[float('inf'), float('inf')] for _ in range(n_nodes)]
        self.order_arr_str = ["a" * 102] * n_nodes

    def insert_line(self, line):
        [vec_id, out_nbr] = line.split()
        hash1 = self.hasher1.get_hash(vec_id)
        hash2 = self.hasher2.get_hash(vec_id)
        self.order_arr[out_nbr][0] = min(self.order_arr[out_nbr][0], hash1)
        self.order_arr[out_nbr][1] = min(self.order_arr[out_nbr][1], hash2)

    def get_order(self):
        mins1 = defaultdict(lambda: sys.maxsize)
        mins2 = defaultdict(lambda: sys.maxsize)
        for i in range(self.n_nodes):
            [hash1, hash2] = self.order_arr[i]
            mins1[hash2] = min(mins1[hash2], hash1)
            mins2[hash1] = min(mins2[hash1], hash2)
        for i in range(self.n_nodes):
            [hash1, hash2] = self.order_arr[i]
            self.order_arr_str[i] = str(mins1[mins2[hash1]]) + str(mins2[hash1]) + str(hash1) + str(hash2)
            # self.order_arr_str[i] = str(maxs1[maxs2[hash1]]) + str(maxs2[hash1]) + str(hash1) + str(hash2)
        s = numpy.array(self.order_arr_str)
        sort_index = numpy.argsort(s)
        ordering = [0] * self.n_nodes
        for idx, orig_id in enumerate(sort_index):
            ordering[orig_id] = idx
        return sort_index

# TODO: New idea: implement Ben's reordering mincut thing with minhash;
#  This means we use minhash to split the graph into partitions
#  Then we reorder each partition, probably with a stricter set of minhash
#  Then we reorder summaries of the partitions, maybe with another set of minhash.


