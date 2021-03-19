import time


class LinearProbing:
    def __init__(self, size):
        self.size = size
        self.arr = [None] * size
        self.second_hash = list(range(size))
        self.total_checks = 0
        self.probes = 0

    def insert(self, vec_id, vec_hash):
        vec_hash_modulo = vec_hash % self.size
        fin_hash = self.second_hash[vec_hash_modulo]
        self.total_checks += 1
        while self.arr[fin_hash] is not None:
            self.total_checks += 1
            self.probes += 1
            fin_hash = self.second_hash[(fin_hash + 1) % self.size]
        self.arr[fin_hash] = vec_id
        self.second_hash[vec_hash_modulo] = (fin_hash + 1) % self.size

    def get_array(self):
        print(f"GRL:\nTotal array accesses: {self.total_checks}\nProbes: {self.probes}")
        return self.arr
