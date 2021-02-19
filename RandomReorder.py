import random


class RandomReorder:
    def __init__(self, n_nodes):
        self.n_nodes = n_nodes
        self.order = [0] * n_nodes
        self.lowest_empty = 0

    def insert(self, vec_id, vector):
        self.order[self.lowest_empty] = vec_id
        self.lowest_empty += 1

    def get_order(self):
        random.shuffle(self.order)
        return self.order



