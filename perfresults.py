from itertools import islice


class PerfResults:
    def __init__(self, filename: str | None, compile_time: float, runtime: float = 0.0, energy_cores: float = 0.0,
                 energy_ram: float = 0.0, energy_gpu: float = 0.0, energy_pkg: float = 0.0, energy_psys: float = 0.0):
        self.compile_time: float = compile_time
        if filename is None:
            self.runtime: float = runtime
            self.energy_cores: float = energy_cores
            self.energy_ram: float = energy_ram
            self.energy_gpu: float = energy_gpu
            self.energy_pkg: float = energy_pkg
            self.energy_psys: float = energy_psys
        else:
            with (open(filename) as f):
                lines: list[str] = f.readlines()
                values = map(float, map(lambda l: l.split(' ')[0].replace('.', '').replace(',', '.'),
                                        map(str.strip, islice(filter(
                                            lambda l: (not l.startswith('#')) and l.strip(), lines), 1, None))))
                self.energy_cores = next(values)
                self.energy_ram = next(values)
                self.energy_gpu = next(values)
                self.energy_pkg = next(values)
                self.energy_psys = next(values)
                self.runtime = next(values)

    def to_csv(self, with_newline: bool = False) -> str:
        s: str = (str(self.compile_time) + ',' + str(self.runtime) + ',' + str(self.energy_cores) + ','
                  + str(self.energy_ram) + ',' + str(self.energy_gpu) + ',' + str(self.energy_pkg) + ','
                  + str(self.energy_psys))
        if with_newline:
            s += "\n"

        return s
