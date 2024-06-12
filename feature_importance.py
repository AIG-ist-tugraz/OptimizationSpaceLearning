import csv
import random

import numpy as np
from sklearn.neighbors import NearestNeighbors

from metrics import CQCodeMetricsNormalized


def generate_random_datapoints(len_per_point, num_points):
    points = []
    for vector in range(num_points):
        point = []
        for vector_feature in range(len_per_point):
            point.append(random.random())
        points.append(point)

    return points


def average_feature_distance(program_vector, other_program_vectors, other_program_ix):
    dists = [0.0 for _ in range(len(program_vector))]
    for ix in range(len(other_program_ix)):
        other_vector = other_program_vectors[ix]
        for feature_ix in range(len(program_vector)):
            dists[feature_ix] += abs(other_vector[feature_ix] - program_vector[feature_ix])

    dists = list(map(lambda s: s / len(other_program_ix), dists))
    assert len(dists) == len(program_vector)

    return dists


def compute_feature_importance(nn_used=5):
    with open('data/metrics.csv') as m:
        program_metrics = [CQCodeMetricsNormalized(line.strip()) for line in m.readlines()]
    assert len(program_metrics) == 30
    assert len(program_metrics[0].vector()) == 66

    # Choose the number such that the weights are not much influenced by the randomness
    random_points = generate_random_datapoints(len(program_metrics[0].vector()), 100000)

    neighbor_feature_dists = [0.0 for _ in range(len(program_metrics[0].vector()))]
    rand_feature_dists = [0.0 for _ in range(len(program_metrics[0].vector()))]
    for program in program_metrics:
        nn = NearestNeighbors(n_neighbors=nn_used, algorithm='ball_tree').fit([p.vector() for p in program_metrics])
        nb_distances, nb_indices = nn.kneighbors([program.vector()])

        nn_rand = NearestNeighbors(n_neighbors=len(random_points), algorithm='ball_tree').fit(random_points)
        rand_distances, rand_indices = nn_rand.kneighbors([program.vector()])

        nb_dists = average_feature_distance(program.vector(), [p.vector() for p in program_metrics], nb_indices)
        rand_dists = average_feature_distance(program.vector(), random_points, rand_indices)

        for ix in range(len(neighbor_feature_dists)):
            neighbor_feature_dists[ix] += nb_dists[ix]
        for ix in range(len(rand_feature_dists)):
            rand_feature_dists[ix] += rand_dists[ix]

    neighbor_feature_dists = list(map(lambda s: s / len(program_metrics), neighbor_feature_dists))
    rand_feature_dists = list(map(lambda s: s / len(program_metrics), rand_feature_dists))
    assert len(neighbor_feature_dists) == len(program_metrics[0].vector())
    assert len(rand_feature_dists) == len(program_metrics[0].vector())

    # The smaller the ratio, the higher the importance of that feature
    feature_ratios = [neighbor_feature_dists[ix] / rand_feature_dists[ix] for ix in range(len(program_metrics[0].vector()))]

    # Perform some normalization
    maximum = max(feature_ratios)
    minimum = min(feature_ratios)
    normalizer = maximum - minimum
    assert normalizer != 0.0
    normalized_feature_ratios = list(map(lambda r: (r - minimum) / normalizer, feature_ratios))

    # Weight is a factor to scale the feature's value
    weights = list(map(lambda norm_r: 1 - norm_r, normalized_feature_ratios))
    # print(weights)

    return weights


def average_feature_importance(runs=25, nn_used=5):
    sum_feature_importance = compute_feature_importance(nn_used)
    for _ in range(runs - 1):
        additional_feature_importance = compute_feature_importance(nn_used)
        for ix in range(len(sum_feature_importance)):
            sum_feature_importance[ix] += additional_feature_importance[ix]

    avg = list(map(lambda f: f / runs, sum_feature_importance))
    return avg


if __name__ == '__main__':
    feature_importance = average_feature_importance()
    print(feature_importance)
