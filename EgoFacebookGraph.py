from collections import defaultdict


class EgoFacebookGraph:
    def __init__(self, path):
        self.adj_dict = defaultdict(lambda: [])
        for line in open(path, 'r'):
            row = [int(i) for i in line.split()]
            self.adj_dict[row[0]].append(row[1])

    def export_arr(self):
        return list(self.adj_dict.values())