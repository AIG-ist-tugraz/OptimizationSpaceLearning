import subprocess
import time

from gcc_options import read_configs_from_csv, perform_run, compute_O3_xor
from metrics import CQMetrics
from perfresults import PerfResults


def training():
    configs = read_configs_from_csv('data/config_tWise4.csv', skip_lines=1)
    with open('data/benchmark_list') as b, open('data/metrics.csv') as m:  # TODO short or not!
        programs = b.readlines()
    res: list[PerfResults] = []
    counter = 0
    for p in programs:
        print('[Program ' + str(counter) + ']')
        counter += 1
        for c in configs:
            flipped_config = compute_O3_xor(c)  # TODO just for use with O3 as base!
            pr = perform_run(p, flipped_config.gcc_format())  # TODO adapt if you use flipped config!
            res.append(pr)
        pr_o0 = perform_run(p, '-O0 ')
        res.append(pr_o0)
        pr_o3 = perform_run(p, '-O3 ')
        res.append(pr_o3)

    with open('results/train_O3_tWise4.csv', "w") as f:  # TODO adapt file name!
        for pr in res:
            f.write(pr.to_csv(with_newline=True))
