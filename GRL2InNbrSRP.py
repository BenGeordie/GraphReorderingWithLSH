from MinHash import Hash
import numpy
import sys
import mmh3


class Mmh3:
    def __init__(self, seed=100):
        self.seed = seed

    def get_hash(self, item):
        return mmh3.hash(str(item), seed=self.seed)


class GRL2InNbrSRP:
    def __init__(self, n_nodes, n_minhashes, n_signs, seed=100):
        self.n_nodes = n_nodes
        self.minhashers = [Mmh3(seed=seed * (i + 1)) for i in range(n_minhashes)]
        self.SRP_mat = numpy.random.rand(n_minhashes, n_signs)

        # Initialize array that would be filled by hashes
        self.minhashes = numpy.full((n_nodes, n_minhashes), sys.maxsize)

    def insert(self, vec_id, vector):
        for hash_num, hasher in enumerate(self.minhashers):
            hash_ = hasher.get_hash(vec_id)
            for out_nbr in vector:
                self.minhashes[out_nbr, hash_num] = min(self.minhashes[out_nbr, hash_num], hash_)

    def get_order(self):
        SRP_hashes = (numpy.matmul(self.minhashes, self.SRP_mat) > 0).astype(int).astype(str).tolist()
        final_hashes = [''.join(row) + str(self.minhashes[i, 0]) + str(self.minhashes[i, 1]) for i, row in enumerate(SRP_hashes)]
        # final_hashes = [''.join(row) + str(self.minhashes[i, 0]) + str(self.minhashes[i, 1]) for i, row in enumerate(SRP_hashes)]
        return numpy.argsort(final_hashes)


# TODO: New idea: implement Ben's reordering mincut thing with minhash;
#  This means we use minhash to split the graph into partitions
#  Then we reorder each partition, probably with a stricter set of minhash
#  Then we reorder summaries of the partitions, maybe with another set of minhash.



