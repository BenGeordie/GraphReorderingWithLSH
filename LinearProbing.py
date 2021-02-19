class LinearProbing:
    def __init__(self, size):
        self.size = size
        self.arr = [None] * size

    def insert(self, vec_id, vec_hash):
        fin_hash = vec_hash % self.size
        while self.arr[fin_hash]:
            fin_hash = (fin_hash + 1) % self.size
        self.arr[fin_hash] = vec_id

    def get_array(self):
        return self.arr
