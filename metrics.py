class VectorMetric:
    def __init__(self):
        self.values: list[float] = []

    def vector(self) -> list[float]:
        return self.values


class CQMetrics(VectorMetric):
    headers: list[str] = None

    def __init__(self, data: str, sep: str = ','):
        super().__init__()
        # if CQMetrics.headers is None:
        #     with open('data/header.tab') as header_file:
        #         CQMetrics.headers = header_file.readline().split('\t')
        for s in data.split(sep):
            self.values.append(float(s))


class CQCodeMetric(CQMetrics):
    def __init__(self, data: str):
        super().__init__(data)
        self.values = self.values[0:66]


class CQCodeMetricsNormalized(CQCodeMetric):
    # FIXME! Used only code metrics...
    # Computed using feature_norm.py, hard-coded for PolyBench!
    norms = [{'min': 2427.0, 'max': 5230.0}, {'min': 110.0, 'max': 196.0}, {'min': 0.0, 'max': 0.0},
             {'min': 18.3788, 'max': 26.8397}, {'min': 17.0, 'max': 27.0}, {'min': 69.0, 'max': 162.0},
             {'min': 16.4826, 'max': 27.9052}, {'min': 23.0, 'max': 35.0}, {'min': 3.0, 'max': 4.0},
             {'min': 22.0, 'max': 58.0}, {'min': 0.0, 'max': 0.0}, {'min': 0.25, 'max': 1.02564},
             {'min': 0.0, 'max': 0.0}, {'min': 2.0, 'max': 5.0}, {'min': 0.721688, 'max': 1.51043},
             {'min': 2.0, 'max': 3.0}, {'min': 0.0, 'max': 0.0}, {'min': 0.0, 'max': 0.0}, {'min': 0.0, 'max': 0.0},
             {'min': 0.0, 'max': 0.0}, {'min': 0.0, 'max': 0.0}, {'min': 0.0, 'max': 0.0}, {'min': 0.0, 'max': 0.0},
             {'min': 0.0, 'max': 0.0}, {'min': 0.0, 'max': 0.0}, {'min': 0.0, 'max': 0.0}, {'min': 0.0, 'max': 0.0},
             {'min': 3.0, 'max': 3.0}, {'min': 0.0, 'max': 0.0}, {'min': 0.0, 'max': 1.0}, {'min': 15.0, 'max': 24.0},
             {'min': 783.0, 'max': 1110.0}, {'min': 0.0, 'max': 0.0}, {'min': 1.0, 'max': 1.0},
             {'min': 199.0, 'max': 199.0}, {'min': 8.0, 'max': 17.0}, {'min': 8.0, 'max': 10.0},
             {'min': 6.0, 'max': 6.0}, {'min': 0.0, 'max': 0.0}, {'min': 0.0, 'max': 2.0}, {'min': 0.0, 'max': 0.0},
             {'min': 0.0276134, 'max': 0.095339}, {'min': 3.0, 'max': 4.0}, {'min': 83.7618, 'max': 398.073},
             {'min': 234.945, 'max': 921.949}, {'min': 206.644, 'max': 800.798}, {'min': 298.678, 'max': 2784.37},
             {'min': 43.1532, 'max': 1083.02}, {'min': 3.0, 'max': 4.0}, {'min': 1.0, 'max': 1.0},
             {'min': 2.5, 'max': 6.5}, {'min': 2.5, 'max': 6.5}, {'min': 3.0, 'max': 12.0},
             {'min': 0.866025, 'max': 4.60977}, {'min': 148.0, 'max': 458.0}, {'min': 1.0, 'max': 1.0},
             {'min': 3.47231, 'max': 5.52703}, {'min': 1.0, 'max': 2.0}, {'min': 27.0, 'max': 27.0},
             {'min': 4.96552, 'max': 6.91399}, {'min': 37.0, 'max': 68.0}, {'min': 1.0, 'max': 1.0},
             {'min': 7.5, 'max': 11.2703}, {'min': 4.0, 'max': 9.0}, {'min': 27.0, 'max': 27.0},
             {'min': 7.47053, 'max': 8.64277}]

    def __init__(self, data: str):
        super().__init__(data)
        assert len(self.values) == len(self.norms), f"{len(self.values)} values and {len(self.norms)} norms!"
        for val_i in range(len(self.values)):
            # min-max normalization
            normalizer = self.norms[val_i]['max'] - self.norms[val_i]['min'] \
                if self.norms[val_i]['max'] - self.norms[val_i]['min'] != 0.0 else 0.00000001
            self.values[val_i] = (self.values[val_i] - self.norms[val_i]['min']) / normalizer


class CQCodeMetricsNormalizedWeighted(CQCodeMetricsNormalized):
    precomputed_weights = [
        0.594661816223014, 0.5716010302080994, 1.0, 0.7605687082356377, 0.591993044773299, 0.8661300730975156,
        0.7776440942635722, 0.28683805713926747, 0.957390693202726, 0.5126897298274635, 1.0, 0.2887499980125042, 1.0,
        0.27912719400337904, 0.48215042973478545, 0.9606064517804207, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 0.9680427967064773, 0.662912420384384, 0.28055560903917537, 1.0, 1.0, 1.0, 0.6432906658359485,
        0.9412461318874709, 1.0, 1.0, 0.958776987238302, 1.0, 0.6203906495335653, 0.953334653450801, 0.6950871499966246,
        0.6177806287014548, 0.678170108406305, 0.6200139904955116, 0.5401599741822412, 0.9555034735653061, 1.0,
        0.647439597502054, 0.6540060381036077, 0.3435470850635935, 0.3455850830375319, 0.6585473425381104, 1.0,
        0.6447223145262985, 0.7891180517596126, 1.0, 0.6361677405488791, 0.644180842007414, 1.0, 0.7129070422859358,
        0.7330968763461548, 1.0, 0.642394929654433]

    def __init__(self, data: str):
        super().__init__(data)
        assert len(self.values) == len(self.precomputed_weights), (f"{len(self.values)} values and "
                                                                   f"{len(self.precomputed_weights)} weights!")
        for val_i in range(len(self.values)):
            self.values[val_i] *= self.precomputed_weights[val_i]


class LineStatementMetric(CQMetrics):
    def __init__(self, data: str):
        super().__init__(data)
        self.values = self.values[0:1]  # FIXME! find correct slice


class KeywordMetric(CQMetrics):
    def __init__(self, data: str):
        super().__init__(data)
        self.values = self.values[0:1]  # FIXME! find correct slice


class HalsteadComplexity(CQMetrics):
    def __init__(self, data: str):
        super().__init__(data)
        self.values = self.values[0:1]  # FIXME! find correct slice


class CyclomaticComplexity(CQMetrics):
    def __init__(self, data: str):
        super().__init__(data)
        self.values = self.values[0:1]  # FIXME! find correct slice
