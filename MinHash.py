import random
import mmh3
import numpy as np


class Hash:
    def __init__(self, max_token, seed=100):
        random.seed(seed)
        self.a = random.randrange(1, max_token)
        self.b = random.randrange(1, max_token)
        self.c = random.randrange(1, max_token)

    def get_hash(self, vector):
        minhash = min((self.a * x + self.b) % self.c for x in vector)
        return mmh3.hash(str(minhash), signed=False)


