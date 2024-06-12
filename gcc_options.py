import subprocess
import time

from perfresults import PerfResults


class GCCConfiguration:
    def __init__(self):
        self.bool_options: list[int] = []
        self.spec_options: list[int] = []

    def append_bool(self, enabled: int):
        if not (enabled == 0 or enabled == 1):
            raise ValueError
        self.bool_options.append(enabled)

    def append_spec(self, choice: int):
        if choice < 1:
            raise ValueError
        self.spec_options.append(choice)

    def gcc_format(self) -> str:
        s: str = ''
        for b in range(len(self.bool_options)):
            if self.bool_options[b] == 1:
                s = s + '-f' + GCCOptions.BOOL[b] + ' '
            elif self.bool_options[b] == 0:
                s = s + '-fno-' + GCCOptions.BOOL[b] + ' '
            else:
                raise ValueError
        for v in range(len(self.spec_options)):
            s = s + '-f' + GCCOptions.SPEC[v][0] + '=' + GCCOptions.SPEC[v][self.spec_options[v]] + ' '

        return s


def read_configs_from_csv(filename: str, skip_lines: int = 0, separator: str = ',') -> list[GCCConfiguration]:
    with open(filename) as csv_file:
        configs = []
        skipped = 0

        for csv_line in csv_file.readlines():
            if csv_line.startswith('#'):  # skip comments
                continue
            if skipped < skip_lines:
                skipped += 1
                continue

            config = GCCConfiguration()
            i = 0
            for s in csv_line.split(separator):
                if i < len(GCCOptions.BOOL):
                    config.append_bool(int(s))
                else:
                    config.append_spec(int(s))
                i += 1
                if i > len(GCCOptions.BOOL) + len(GCCOptions.SPEC):
                    raise RuntimeError
            configs.append(config)

        return configs


def aggregate_configs(candidates: list[GCCConfiguration], one_hot=False) -> GCCConfiguration:
    aggregated_config = GCCConfiguration()
    num_candidates = len(candidates)

    for b in range(len(GCCOptions.BOOL)):
        agg_sum = 0
        for c in candidates:
            agg_sum += c.bool_options[b]
        activation_condition: bool = agg_sum > (num_candidates / 2) if not one_hot else agg_sum > 0  # FIXME check tendencies
        aggregated_config.append_bool(1 if activation_condition else 0)
    for v in range(len(GCCOptions.SPEC)):
        aggregated_config.append_spec(candidates[0].spec_options[v])

    return aggregated_config


def perform_run(program_file, options):  # Options must end with a space!
    gcc_command = ('gcc -I ../training/utilities -I ' + program_file[:(program_file.rfind('/'))] + ' -O ' + options +
                   '-o ' + 'temp/temp_out ' + '../training/utilities/polybench.c ../training/' + program_file + ' -lm')
    split_gcc_command = gcc_command.split()
    compile_start = time.time()
    subprocess.run(split_gcc_command)
    compile_end = time.time()
    compile_time = compile_end - compile_start

    perf_command = 'sudo perf stat -r 2 -o temp/temp_log -e power/energy-cores/,power/energy-ram/,' + \
                   'power/energy-gpu/,power/energy-pkg/,power/energy-psys/ ./temp/temp_out'
    subprocess.run(perf_command.split())
    pr = PerfResults('temp/temp_log', compile_time)

    rm_command = 'sudo rm temp/temp_out temp/temp_log'
    subprocess.run(rm_command.split())

    return pr


def compute_O3_xor(config: GCCConfiguration) -> GCCConfiguration:
    # source: https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
    o3_values = [
        4, 82, 7, 9, 10, 83, 17, 22, 30, 86, 39, 40, 43, 45, 51, 52, 53, 54, 78, 81, 97, 111, 136, 137, 143, 145, 146,
        152, 154, 155, 156, 157, 158, 159, 160, 161, 162, 166, 175, 177, 178, 179, 180, 183, 187,  # from -O1
        6, 163, 11, 12, 13, 18, 19, 20, 25, 29, 32, 35, 38, 42, 44, 41, 48, 46, 56, 192, 24, 49, 61, 75, 98, 99, 90,
        112, 113, 114, 129, 130, 92, 93, 148, 149, 150, 153, 172, 173, 181, 182, 185,  # from -O2
        33, 47, 70, 72, 100, 101, 141, 142, 167, 174, 191  # from -O3
    ]
    o3_based_config = GCCConfiguration()

    for b in range(len(GCCOptions.BOOL)):
        if b in o3_values:
            o3_based_config.append_bool(1 if config.bool_options[b] == 0 else 0)  # flip the value
        else:
            o3_based_config.append_bool(config.bool_options[b])
    for v in range(len(GCCOptions.SPEC)):
        o3_based_config.append_spec(config.spec_options[v])

    return o3_based_config


class GCCOptions:
    # numbers denote last index in that line
    BOOL = [
        "aggressive-loop-optimizations", "allocation-dce", "allow-store-data-races", "associative-math",  # 3
        "auto-inc-dec", "branch-probabilities", "caller-saves", "combine-stack-adjustments",  # 7
        "conserve-stack", "compare-elim", "cprop-registers", "crossjumping", "cse-follow-jumps", "cse-skip-blocks",  # 13
        "cx-fortran-rules", "cx-limited-range", "data-sections", "dce", "delete-null-pointer-checks",  # 18
        "devirtualize", "devirtualize-speculatively", "devirtualize-at-ltrans", "dse",  # 22
        "early-inlining", "ipa-sra", "expensive-optimizations", "fast-math", "finite-math-only",  # 27
        "float-store", "finite-loops", "forward-propagate", "function-sections", "gcse", "gcse-after-reload",  # 33
        "gcse-las", "gcse-lm", "graphite-identity", "gcse-sm", "hoist-adjacent-loads", "if-conversion",  # 39
        "if-conversion2", "indirect-inlining", "inline-functions", "inline-functions-called-once",  # 43
        "inline-small-functions", "ipa-modref", "ipa-cp", "ipa-cp-clone", "ipa-bit-cp", "ipa-vrp", "ipa-pta",  # 50
        "ipa-profile", "ipa-pure-const", "ipa-reference", "ipa-reference-addressable", "ipa-stack-alignment",  # 55
        "ipa-icf", "ira-hoist-pressure", "ira-loop-pressure", "ira-share-save-slots", "ira-share-spill-slots",  # 60
        "isolate-erroneous-paths-dereference", "isolate-erroneous-paths-attribute", "ivopts",  # 63
        "keep-inline-functions", "keep-static-functions", "keep-static-consts", "limit-function-alignment",  # 67
        "live-range-shrinkage", "loop-block", "loop-interchange", "loop-strip-mine", "loop-unroll-and-jam",  # 72
        "loop-nest-optimize", "loop-parallelize-all", "lra-remat", "lto", "merge-all-constants", "merge-constants",  # 78
        "modulo-sched", "modulo-sched-allow-regmoves", "move-loop-invariants", "branch-count-reg", "defer-pop",  # 83
        "fp-int-builtin-inexact", "function-cse", "guess-branch-probability", "inline", "math-errno", "peephole",  # 89
        "peephole2", "printf-return-value", "sched-interblock", "sched-spec", "signed-zeros",  # 94
        "trapping-math", "zero-initialized-in-bss", "omit-frame-pointer", "optimize-sibling-calls",  # 98
        "partial-inlining", "peel-loops", "predictive-commoning", "prefetch-loop-arrays", "profile-correction",  # 103
        "profile-use", "profile-partial-training", "profile-values", "profile-reorder-functions", "reciprocal-math",  # 108
        "ree", "rename-registers", "reorder-blocks", "reorder-blocks-and-partition", "reorder-functions",  # 113
        "rerun-cse-after-loop", "reschedule-modulo-scheduled-loops", "rounding-math", "save-optimization-record",  # 117
        "sched2-use-superblocks", "sched-pressure", "sched-spec-load", "sched-spec-load-dangerous",  # 121
        "sched-group-heuristic", "sched-critical-path-heuristic", "sched-spec-insn-heuristic",  # 124
        "sched-rank-heuristic", "sched-last-insn-heuristic", "sched-dep-count-heuristic", "schedule-fusion",  # 128
        "schedule-insns", "schedule-insns2", "selective-scheduling", "selective-scheduling2",  # 132
        "sel-sched-pipelining", "sel-sched-pipelining-outer-loops", "semantic-interposition", "shrink-wrap",  # 136
        "shrink-wrap-separate", "signaling-nans", "single-precision-constant", "split-ivs-in-unroller",  # 140
        "split-loops", "split-paths", "split-wide-types", "split-wide-types-early", "ssa-backprop", "ssa-phiopt",  # 146
        "stdarg-opt", "store-merging", "strict-aliasing", "thread-jumps", "tracer", "tree-bit-ccp",  # 152
        "tree-builtin-call-dce", "tree-ccp", "tree-ch", "tree-coalesce-vars", "tree-copy-prop", "tree-dce",  # 158
        "tree-dominator-opts", "tree-dse", "tree-forwprop", "tree-fre", "code-hoisting", "tree-loop-if-convert",  # 164
        "tree-loop-im", "tree-phiprop", "tree-loop-distribution", "tree-loop-distribute-patterns",  # 168
        "tree-loop-ivcanon", "tree-loop-linear", "tree-loop-optimize", "tree-loop-vectorize", "tree-pre",  # 173
        "tree-partial-pre", "tree-pta", "tree-reassoc", "tree-scev-cprop", "tree-sink", "tree-slsr", "tree-sra",  # 180
        "tree-switch-conversion", "tree-tail-merge", "tree-ter", "tree-vectorize", "tree-vrp",  # 185
        "unconstrained-commons", "unit-at-a-time", "unroll-all-loops", "unroll-loops", "unsafe-math-optimizations",  # 190
        "unswitch-loops", "ipa-ra", "variable-expansion-in-unroller", "vect-cost-model", "vpt", "web",  # 196
        "use-linker-plugin"  # 197
    ]

    SPEC = [
        ["fp-contract", "fast", "on", "off"],
        ["ira-algorithm", "priority", "CB"],
        ["ira-region", "all", "mixed", "one"],
        ["lto-partition", "balanced", "1to1", "max", "one", "none"],
        ["reorder-blocks-algorithm", "simple", "stc"]
    ]
