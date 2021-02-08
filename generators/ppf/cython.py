import scipy.stats as stats

class Generator:
    enabled = False
    display_name = "cython"

    @staticmethod
    def init_parser(parser):
        parser.add_argument('--cython', action="store_true")

    @classmethod
    def init_args(cls, arg):
        cls.enabled = arg.cython

    @staticmethod
    def process(case, dop):
        p, k, nu = case.p, case.k, case.v
        stats.distributions.studentized_range._epsabs = 10 ** -dop
        return stats.distributions.studentized_range.ppf(p, k, nu).item()
