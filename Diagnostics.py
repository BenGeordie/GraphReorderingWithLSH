import matplotlib.pyplot as plt


def pairwise_overlap(title, graph):
    graph_copy = list(graph)

    def get_overlap(list1, list2):
        return len(set(list1).intersection(set(list2)))

    data = []
    graph_length = len(graph)
    graph_range = range(graph_length)
    for i in graph_range:
        line_i = graph_copy.pop(graph_length - i - 1)
        for line_j in graph_copy:
            data.append(get_overlap(line_i, line_j))

    plt.hist(data, bins=max(data))
    plt.title(f'Pairwise neighborhood overlap in {title}')
    plt.xlabel("# overlapping neighbors between any two nodes")
    plt.ylabel("Frequency")
    plt.show()



