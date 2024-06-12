from math import inf

from metrics import CQMetrics


def compute_normalization_helper():
    with open('data/metrics.csv') as m:
        program_metrics = [CQMetrics(line.strip()) for line in m.readlines()]

    num_metrics = len(program_metrics[0].vector())

    norm_helper = []
    for metric in range(num_metrics):
        minimum = inf
        maximum = -inf
        for program_metric in program_metrics:
            if program_metric.vector()[metric] < minimum:
                minimum = program_metric.vector()[metric]
            if program_metric.vector()[metric] > maximum:
                maximum = program_metric.vector()[metric]

        norm_helper.append({'min': minimum, 'max': maximum})

    assert len(norm_helper) == num_metrics
    for norm in norm_helper:
        assert norm['min'] <= norm['max']

    print(norm_helper)


if __name__ == '__main__':
    compute_normalization_helper()
