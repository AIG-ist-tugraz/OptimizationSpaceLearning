#! /bin/python3
from argparse import ArgumentParser
from csv import reader
from statistics import fmean, median


def analyse(directory, k, a, verbose, chosen_only):
    chosen_ones = [2, 3, 15, 28, 18, 0, 23, 11, 26, 1]  # indices in benchmark_list, zero-based - from "P1" to "P10"
    assert len(chosen_ones) == 10

    data = []
    csv_file_path = directory.rstrip('/') + '/k' + k + '-a' + a + '.csv'
    with open(csv_file_path) as csv_file:
        csv_reader = reader(csv_file, delimiter=',', skipinitialspace=True)
        for line in csv_reader:
            data.append(line)

    speedups = []
    num_real_speedups = 0
    for d in range(len(data)):
        if chosen_only and d not in chosen_ones:
            continue
        data_entry = data[d]
        speedup = float(data_entry[2]) / float(data_entry[0])
        speedups.append(speedup)
        if speedup > 1.0:
            num_real_speedups += 1
        if verbose:
            print(speedup)
    if verbose:
        print()
    print("[AVG] Average Speedup:", fmean(speedups))
    print("[MED] Median Speedup:", median(speedups))
    print("[NUM] Number Of Real Speedups:", str(num_real_speedups) + "/" + str(len(speedups)))
    print()


def main():
    parser = ArgumentParser()
    parser.add_argument('dir')
    parser.add_argument('k')
    parser.add_argument('a')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-c', '--chosen-ones', action='store_true')
    args = parser.parse_args()

    analyse(args.dir, args.k, args.a, args.verbose, args.chosen_ones)


if __name__ == '__main__':
    main()
