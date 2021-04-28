from MinHash import Hash
import numpy
import sys
import mmh3


class Mmh3:
    def __init__(self, seed=100):
        self.seed = seed

    def get_hash(self, item):
        return mmh3.hash(str(item), seed=self.seed)


class GRL2InNbr:
    def __init__(self, n_nodes, n_minhashes, seed=100):
        self.n_nodes = n_nodes
        self.murmurhashers = [Mmh3(seed=seed * (i + 1)) for i in range(n_minhashes)]

        # Initialize array that would be filled by hashes
        self.minhashes = [[sys.maxsize for _ in range(n_minhashes)] for _ in range(n_nodes)]
        self.hashes_str = [""] * n_nodes

    def insert(self, vec_id, vector):
        for hash_num, hasher in enumerate(self.murmurhashers):
            hash_ = hasher.get_hash(vec_id)
            for out_nbr in vector:
                self.minhashes[out_nbr][hash_num] = min(self.minhashes[out_nbr][hash_num], hash_)

    def get_order(self):
        for i in range(self.n_nodes):
            [hash1, hash2] = self.minhashes[i]
            self.hashes_str[i] = str(hash1) + str(hash2)
        sort_index = numpy.argsort(numpy.array(self.hashes_str))
        return sort_index

