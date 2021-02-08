from statsmodels.stats.libqsturng import psturng

class Generator:
    enabled = False
    display_name = "statsmodel"

    @staticmethod
    def init_parser(parser):
        parser.add_argument('--statsmodel', action="store_true")

    @classmethod
    def init_args(cls, arg):
        cls.enabled = arg.statsmodel

    @staticmethod
    def process(case, dop):
        q, k, nu = case.q, case.k, case.v
        atol = 10 ** (-dop)
        return 1 - psturng(q, k, nu)
