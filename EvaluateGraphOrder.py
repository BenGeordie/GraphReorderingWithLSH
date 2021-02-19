def evaluate(title, graph_order, get_adjacent_vectors_fn):
    total = 0
    sum_of_squares = 0
    max_overlap = 0
    min_overlap = len(graph_order)
    for i in range(len(graph_order)):
        adj_set_1 = set(get_adjacent_vectors_fn(graph_order[i]))
        adj_set_2 = set(get_adjacent_vectors_fn(graph_order[(i + 1) % len(graph_order)]))
        overlap = len(adj_set_1.intersection(adj_set_2))
        max_overlap = max(max_overlap, overlap)
        min_overlap = min(min_overlap, overlap)
        total += overlap
        sum_of_squares += overlap ** 2
    title_str = f'|| Evaluating: {title} ||'
    print('-' * len(title_str))
    print(title_str)
    print('-' * len(title_str))
    print(f'Average # overlapping neighbors between adjacent nodes: {total / len(graph_order)}')
    print(f'Average # overlapping neighbors squared between adjacent nodes: {sum_of_squares / len(graph_order)}')
    print(f'Maximum # overlapping neighbors between adjacent nodes: {max_overlap}')
    print(f'Minimum # overlapping neighbors between adjacent nodes: {min_overlap}')
