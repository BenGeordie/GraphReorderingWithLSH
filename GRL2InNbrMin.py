from MinHash import Hash
import numpy
import sys
import mmh3
from collections import defaultdict


class Mmh3:
    def __init__(self, seed=100):
        self.seed = seed

    def get_hash(self, item):
        return mmh3.hash(str(item), seed=self.seed)


class GRL2InNbrMin:
    def __init__(self, n_nodes, n_minhashes, seed=100):
        self.n_nodes = n_nodes
        self.n_minhashes = n_minhashes
        self.minhashers = [Mmh3(seed=seed * (i + 1)) for i in range(n_minhashes)]
        self.fin_minhasher = Hash(sys.maxsize)

        # Initialize array that would be filled by hashes
        self.minhashes = numpy.full((n_nodes, n_minhashes), sys.maxsize)

    def insert(self, vec_id, vector):
        for hash_num, hasher in enumerate(self.minhashers):
            hash_ = hasher.get_hash(vec_id)
            for out_nbr in vector:
                self.minhashes[out_nbr, hash_num] = min(self.minhashes[out_nbr, hash_num], hash_)

    def get_order(self):
        mins = defaultdict(lambda: sys.maxsize)
        MIN_hashes = [str(self.fin_minhasher.get_hash(minhashes)) + str(self.minhashes[i][0]) + str(self.minhashes[i][1]) for i, minhashes in enumerate(self.minhashes.tolist())]
        return numpy.argsort(MIN_hashes)


# TODO: New idea: implement Ben's reordering mincut thing with minhash;
#  This means we use minhash to split the graph into partitions
#  Then we reorder each partition, probably with a stricter set of minhash
#  Then we reorder summaries of the partitions, maybe with another set of minhash.



