import matplotlib.pyplot as plt


def evaluate(title, graph_order, get_adjacent_vectors_fn):
    total = 0
    sum_of_squares = 0
    max_overlap = 0
    min_overlap = len(graph_order)
    histogram_data = []
    for i in range(len(graph_order)):
        adj_set_1 = set(get_adjacent_vectors_fn(graph_order[i]))
        adj_set_2 = set(get_adjacent_vectors_fn(graph_order[(i + 1) % len(graph_order)]))
        overlap = len(adj_set_1.intersection(adj_set_2))
        max_overlap = max(max_overlap, overlap)
        min_overlap = min(min_overlap, overlap)
        total += overlap
        sum_of_squares += overlap ** 2
        histogram_data.append(overlap)
    title_str = f'|| Evaluating: {title} ||'
    print('-' * len(title_str))
    print(title_str)
    print('-' * len(title_str))
    print(f'Average # overlapping neighbors between adjacent nodes: {total / len(graph_order)}')
    print(f'Average # overlapping neighbors squared between adjacent nodes: {sum_of_squares / len(graph_order)}')
    print(f'Maximum # overlapping neighbors between adjacent nodes: {max_overlap}')
    print(f'Minimum # overlapping neighbors between adjacent nodes: {min_overlap}')
    plt.xlabel("# overlapping neighbors between adjacent nodes")
    plt.ylabel("# adjacent node pairs")
    plt.hist(histogram_data, bins=[0, 1, 2, 5, 10, 25, 70, 200])
    plt.title(f'{title} bins [0, 1, 2, 5, 10, 25, 70, 200]')
    plt.show()
    plt.hist(histogram_data, bins=200)
    plt.title(f'{title}')
    plt.show()

