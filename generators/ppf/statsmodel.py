from statsmodels.stats.libqsturng import qsturng

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
        p, k, nu = case.p, case.k, case.v
        res = qsturng(p, k, nu)
        #print(res)
        return res

