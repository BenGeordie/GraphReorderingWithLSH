import random
import mmh3


class Hash:
    def __init__(self, max_token, n_hashes, seed=100):
        random.seed(seed)

        def triple_randrange(mini, maxi):
            return [random.randrange(mini, maxi) for _ in [1, 2, 3]]

        self.abc_list = [triple_randrange(1, max_token) for _ in range(n_hashes)]

    def get_hash(self, vector):
        return [mmh3.hash(str(min([(a * x + b) % c for x in vector])), signed=False) for a, b, c in self.abc_list]
