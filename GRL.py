from Hash import Hash
from LinearProbing import LinearProbing


class GRL:
    def __init__(self, array_size, n_nodes, n_hashes=1, seed=100):
        self.n_nodes = n_nodes
        self.hasher = Hash(n_nodes, n_hashes, seed=seed)
        self.lp = LinearProbing(array_size)

    def insert(self, vec_id, vector):
        vec_hash = self.hasher.get_hash(vector)[0]
        self.lp.insert(vec_id, vec_hash)

    def get_order(self):
        arr = [0] * self.n_nodes
        i = 0
        for item in self.lp.get_array():
            if item:
                arr[i] = item
                i += 1
        return arr



