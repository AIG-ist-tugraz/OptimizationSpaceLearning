import time

import numpy as np
from sklearn.neighbors import NearestNeighbors

from gcc_options import read_configs_from_csv, aggregate_configs, perform_run, compute_O3_xor
from metrics import CQMetrics, CQCodeMetric, CQCodeMetricsNormalized, CQCodeMetricsNormalizedWeighted


def testing(arg_k, arg_a):
    configs = read_configs_from_csv('data/config_tWise3.csv', 1)  # TODO adapt files, skip lines
    with open('data/benchmark_list') as b, open('data/metrics.csv') as m, open('results/train_tWise3.csv') as r:
        names = [line.strip() for line in b.readlines()]
        program_metrics = [CQCodeMetricsNormalizedWeighted(line.strip()) for line in m.readlines()]
        training_data = [[float(f) for f in line.strip('\n').split(',')] for line in r.readlines()]

    assert len(names) == len(program_metrics)
    for a in training_data:
        assert len(a) == 7

    for p in range(len(program_metrics)):
        timer_start = time.time()
        evaluate(p, program_metrics, names, training_data, configs, k=arg_k, agg=arg_a, timing_mode=True)  # TODO adapt as you wish
        timer_end = time.time()
        print("Elapsed time:", timer_end - timer_start, "s")


def evaluate(index_to_test, program_metrics, names, training_data, configs, k=1, agg=1, timing_mode=False):
    configs_size = len(configs)
    test_program = program_metrics[index_to_test].vector()
    training_programs = [p.vector() for p in program_metrics]

    # best is always itself, thus k + 1
    neighbors = NearestNeighbors(n_neighbors=k + 1, algorithm='ball_tree').fit(training_programs)
    distances, indices_with_self = neighbors.kneighbors([test_program])
    indices = np.delete(indices_with_self[0], 0)
    assert index_to_test not in indices

    runtimes = [[t[1]] for t in training_data]

    neighbor_configs = []
    config_indices = None
    for i in indices:
        runtime_helper_neighbors = (NearestNeighbors(n_neighbors=agg, algorithm='ball_tree')
                                    .fit(runtimes[(i * (configs_size + 2)):(i * (configs_size + 2) + configs_size)]))
        values, config_indices = runtime_helper_neighbors.kneighbors([[0.0]])
        # print("Best configs:", config_indices)
        neighbor_configs.append(aggregate_configs([configs[index[0]] for index in config_indices], one_hot=False))
    recommended_config = aggregate_configs(neighbor_configs, one_hot=False)  # TODO enable/disable one-hot mode! (2x)

    if timing_mode:
        return

    if k == 1 and agg == 1:
        start_index = index_to_test * (configs_size + 2)
        print(str(runtimes[start_index + config_indices[0][0]][0]) + ',',
              str(runtimes[start_index + configs_size][0]) + ',',
              str(runtimes[start_index + configs_size + 1][0]))
    else:
        # flipped_config = compute_O3_xor(recommended_config)  # TODO just for use with O3 as base!
        # performance = perform_run(names[index_to_test], flipped_config.gcc_format())  # TODO use when using O3!
        performance = perform_run(names[index_to_test], recommended_config.gcc_format())  # TODO use when not using O3!
        start_index = index_to_test * (configs_size + 2)
        print(str(performance.runtime) + ',',
              str(runtimes[start_index + configs_size][0]) + ',',
              str(runtimes[start_index + configs_size + 1][0]))
