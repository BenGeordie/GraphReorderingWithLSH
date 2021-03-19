from MinHash import Hash
import numpy
import sys


class GRL2:
    def __init__(self, n_nodes, seed=100):
        self.n_nodes = n_nodes
        self.hasher1 = Hash(sys.maxsize, seed=seed)
        self.hasher2 = Hash(sys.maxsize, seed=seed * 2)
        self.order_arr = ["a" * 102] * n_nodes
        self.min_hash1_arr = [sys.maxsize] * n_nodes
        self.min_hash2_arr = [sys.maxsize] * n_nodes
        self.min_hash1_used = {}
        self.min_hash2_used = {}

    def insert(self, vec_id, vector):
        hash1 = self.hasher1.get_hash(vector)
        hash2 = self.hasher2.get_hash(vector)
        vec_hash = str(hash1) + '.' + str(hash2)
        self.min_hash2_arr[hash1 % self.n_nodes] = min(self.min_hash2_arr[hash1 % self.n_nodes], hash2)
        self.min_hash1_arr[hash2 % self.n_nodes] = min(self.min_hash1_arr[hash2 % self.n_nodes], hash1)
        self.order_arr[vec_id] = vec_hash

    def get_order(self):
        for i in range(self.n_nodes):
            [hash1, hash2] = self.order_arr[i].split('.')
            min_hash2 = self.min_hash2_arr[int(hash1) % self.n_nodes]
            min_hash1 = self.min_hash1_arr[min_hash2 % self.n_nodes]
            self.min_hash1_used[min_hash1] = 1
            self.min_hash2_used[min_hash2] = 1
            self.order_arr[i] = str(min_hash1) + str(min_hash2) + hash1 + hash2
        print("Unique min hash1 used:", len(self.min_hash1_used))
        print("Unique min hash2 used:", len(self.min_hash2_used))
        s = numpy.array(self.order_arr)
        sort_index = numpy.argsort(s)
        return sort_index

# TODO: New idea: implement Ben's reordering mincut thing with minhash;
#  This means we use minhash to split the graph into partitions
#  Then we reorder each partition, probably with a stricter set of minhash
#  Then we reorder summaries of the partitions, maybe with another set of minhash.



