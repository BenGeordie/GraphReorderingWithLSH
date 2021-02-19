from Hash import Hash
from LinearProbing import LinearProbing


class GRL:
    def __init__(self, array_size, n_nodes, seed=100):
        n_hashes = 2
        self.array_size = array_size
        self.averages = [[0, 0]] * array_size
        self.n_nodes = n_nodes
        self.hasher = Hash(n_nodes, n_hashes, seed=seed)
        self.lp = LinearProbing(array_size)

    def insert(self, vec_id, vector):
        vec_hashes = self.hasher.get_hash(vector)
        # What if instead of linear probing with this hash, we use the hash of the list of nodes
        # that are hashed to the same buckets as this node?
        coord_hash = vec_hashes[0]
        averaging_hash = vec_hashes[1]
        self.averages[averaging_hash % self.array_size][0] += coord_hash
        self.averages[averaging_hash % self.array_size][1] += 1
        entry = self.averages[averaging_hash % self.array_size]
        vec_hash = int(0.999999 * coord_hash + 0.000001 * entry[0] / entry[1])



        # 2 hashes. The first is a "real coordinate"
        # second hash is for a second array which holds the current "average real coordinate" of the nodes passed to it.
        # Second array also holds counter for number of elements.
        # final hash is (first_hash + second_array[second_hash][average] * second_array[second_hash][counter]) / second_array[second_hash][counter + 1]
        self.lp.insert(vec_id, vec_hash)

    def get_order(self):
        arr = [0] * self.n_nodes
        i = 0
        for item in self.lp.get_array():
            if item:
                arr[i] = item
                i += 1
        return arr



