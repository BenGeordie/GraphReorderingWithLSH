import time
import numpy as np
from utils.GOrderObjective import gorder_objective
from algorithms.MinhashSortingK3Stream import MinhashSortingK3

test_name = "Minhash Sorting K3 Stream"
print('------------------------------------------')
print(test_name)
print('------------------------------------------')
times = [0.0] * 4
times[0] = time.time()
_model = MinhashSortingK3()
times[1] = time.time()
for line in open("datasets/pld-arc"):
    _model.insert_edge(line)
times[2] = time.time()
ordering = _model.get_order()
times[3] = time.time()
ordering_inverse = np.argsort(ordering)
gorder_obj_score = gorder_objective(5, lambda: ordering, lambda node: [ordering_inverse[nbr] for nbr in graph[node]])

print(f'{test_name} | GOrder Objective Score: {gorder_obj_score}')
print(f'{test_name} | # Operations: {_model.get_operation_count()}\n')
print()


