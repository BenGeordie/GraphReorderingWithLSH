import random
import mmh3
import numpy as np
from MinHash import Hash as Minhash


class Hash:
    def __init__(self, max_token, reps=10, seed=100):
        random.seed(seed)
        self.Parent = Minhash(max_token)
        self.Children = [Minhash(max_token) for _ in range(reps)]

    def get_hash(self, vector):
        return self.Parent.get_hash([Child.get_hash(vector) for Child in self.Children])


