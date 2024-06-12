import subprocess

from sklearn.neighbors import NearestNeighbors

from gcc_options import aggregate_configs, GCCConfiguration
from metrics import CQMetrics


def compile_with_configuration(config: GCCConfiguration, program_path: str, out_file='osl_out', add_options_before='',
                               add_options_after='-lm'):
    gcc_command = ('gcc ' + add_options_before + ' -O ' + config.gcc_format() + ' -o ' + out_file + ' '
                   + program_path + ' ' + add_options_after)
    subprocess.run(gcc_command.split())


class OSL:
    def __init__(self, configs: list[GCCConfiguration], metrics: list[CQMetrics], training_data: list[list[float]]):
        for a in training_data:
            assert len(a) == 7
        self.configs = configs
        self.metrics = metrics
        self.training_data = training_data

    def recommend_config(self, cq_metrics: CQMetrics, program_path: str, k=1, a=1, one_hot_mode=False) -> GCCConfiguration:
        program_metrics = cq_metrics  # FIXME! Temporary
        neighbors = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit([m.vector() for m in self.metrics])
        distances, indices = neighbors.kneighbors([program_metrics.vector()])
        indices = indices[0]

        runtimes = [[t[1]] for t in self.training_data]

        neighbor_configs = []
        config_indices = None
        for i in indices:
            runtime_helper_neighbors = (NearestNeighbors(n_neighbors=a, algorithm='ball_tree').fit(
                runtimes[(i * (len(self.configs) + 2)):(i * (len(self.configs) + 2) + len(self.configs))]))
            values, config_indices = runtime_helper_neighbors.kneighbors([[0.0]])
            neighbor_configs.append(aggregate_configs([self.configs[index[0]] for index in config_indices],
                                                      one_hot=one_hot_mode))
        recommended_config = aggregate_configs(neighbor_configs, one_hot=one_hot_mode)
        return recommended_config
