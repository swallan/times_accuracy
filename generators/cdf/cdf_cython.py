import scipy.stats as stats

class Generator:
    enabled = False
    display_name = "cdf-cython"

    @staticmethod
    def init_parser(parser):
        parser.add_argument('--cython', action="store_true")

    @classmethod
    def init_args(cls, arg):
        cls.enabled = arg.cython

    @staticmethod
    def process(case, dop):
        q, k, nu = case.q, case.k, case.v
        atol = 10 ** -dop
        return stats.distributions.studentized_range._cdf((q, atol), k, nu).item()
