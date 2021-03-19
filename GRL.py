from MinHash import Hash
from LinearProbing import LinearProbing
import sys


class GRL:
    def __init__(self, array_size, n_nodes, seed=100):
        self.size = array_size
        self.n_nodes = n_nodes
        self.hasher = Hash(sys.maxsize, seed=seed)
        self.lp = LinearProbing(array_size)
        self.hashes_obtained = {}

    def insert(self, vec_id, vector):
        vec_hash = self.hasher.get_hash(vector)
        self.hashes_obtained[vec_hash] = 1
        self.lp.insert(vec_id, vec_hash)

    def get_order(self):
        print("Hashes obtained", len(self.hashes_obtained))
        arr = [0] * self.n_nodes
        i = 0
        for item in self.lp.get_array():
            if item:
                arr[i] = item
                i += 1
        return arr

# TODO: New idea: implement Ben's reordering mincut thing with minhash;
#  This means we use minhash to split the graph into partitions
#  Then we reorder each partition, probably with a stricter set of minhash
#  Then we reorder summaries of the partitions, maybe with another set of minhash.


