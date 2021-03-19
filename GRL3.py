from MinHash import Hash
import numpy
import sys


# Main difference from GRL2: hash is fit into 32 bit int.
class GRL3:
    def __init__(self, n_nodes, seed=100):
        self.n_nodes = n_nodes
        self.hasher1 = Hash(sys.maxsize, seed=seed)
        self.hasher2 = Hash(sys.maxsize, seed=seed * 2)
        self.order_arr = [0] * n_nodes
        self.min_hash2_arr = [sys.maxsize] * n_nodes

    def insert(self, vec_id, vector):
        hash1 = self.hasher1.get_hash(vector) & 4095  # Extract last 12 bits
        hash2 = self.hasher2.get_hash(vector) & 4095  # Extract last 12 bits
        vec_hash = hash1 << 8 + hash2 >> 4
        self.min_hash2_arr[hash1 % self.n_nodes] = min(self.min_hash2_arr[hash1 % self.n_nodes], hash2)
        self.order_arr[vec_id] = vec_hash

    def get_order(self):
        for i in range(self.n_nodes):
            hash1 = self.order_arr[i] >> 8
            min_hash2 = self.min_hash2_arr[hash1 % self.n_nodes] << 20  # Move last 8 bits to first 8 bits of 32-bit int
            self.order_arr[i] += min_hash2
        s = numpy.array(self.order_arr)
        sort_index = numpy.argsort(s)
        return sort_index

# TODO: New idea: implement Ben's reordering mincut thing with minhash;
#  This means we use minhash to split the graph into partitions
#  Then we reorder each partition, probably with a stricter set of minhash
#  Then we reorder summaries of the partitions, maybe with another set of minhash.


