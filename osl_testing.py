import time

from gcc_options import read_configs_from_csv
from metrics import CQMetrics
from osl import OSL


def main():
    configs = read_configs_from_csv('data/config_tWise4.csv', 1)
    with open('data/metrics.csv') as m, open('results/train_O3_tWise4.csv') as r:
        program_metrics = [CQMetrics(line.strip()) for line in m.readlines()]
        training_data = [[float(f) for f in line.strip('\n').split(',')] for line in r.readlines()]

    osl = OSL(configs, program_metrics, training_data)
    timer_start = time.time()
    osl.recommend_config(program_metrics[28], "", 3, 1)
    timer_end = time.time()
    osl_time = timer_end - timer_start
    print("OSL took", osl_time, "s")


if __name__ == '__main__':
    main()
