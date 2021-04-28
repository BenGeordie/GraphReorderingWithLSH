class DegSorting:
    def __init__(self, n_nodes):
        self.n_nodes = n_nodes
        self.degrees = [0 for _ in range(self.n_nodes)]
        self.total_deg = 0

    def insert(self, u, vector):
        self.degrees[u] = len(vector)
        self.total_deg += len(vector)

    def get_order(self):
        ordering = [0 for _ in range(self.n_nodes)]
        hubs = filter(lambda elem: self.degrees[elem] >= avg_deg, list(range(self.n_nodes)))
        avg_deg = 0
        hubs = [(hub, self.degrees[hub]) for hub in hubs]
        hubs.sort(key=lambda elem: elem[1], reverse=True)
        for i, hub in enumerate(hubs):
            ordering[i] = hub[0]
        return ordering



