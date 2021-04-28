import math


class HubSorting:
    def __init__(self, n_nodes):
        self.n_nodes = n_nodes
        self.degrees = [0 for _ in range(self.n_nodes)]
        self.total_deg = 0
        self.m = 0

    def insert(self, u, vector):
        self.degrees[u] = len(vector)
        self.total_deg += len(vector)
        self.m += 1

    def get_order(self):
        ordering = [0 for _ in range(self.n_nodes)]
        avg_deg = self.total_deg / self.n_nodes
        hubs = filter(lambda elem: self.degrees[elem] >= avg_deg, list(range(self.n_nodes)))
        non_hubs = filter(lambda elem: self.degrees[elem] < avg_deg, list(range(self.n_nodes)))
        hubs = [(hub, self.degrees[hub]) for hub in hubs]
        hubs.sort(key=lambda elem: elem[1], reverse=True)
        n_hubs = len(hubs)
        for i, hub in enumerate(hubs):
            ordering[i] = hub[0]
        for i, non_hub in enumerate(non_hubs):
            ordering[n_hubs + i] = non_hub
        return ordering

    def get_operation_count(self):
        return math.floor(self.m + self.n_nodes * math.log(self.n_nodes, 2))



