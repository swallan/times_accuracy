from pingouin.external.qsturng import psturng


class Generator:
    enabled = False
    display_name = "pingouin"

    @staticmethod
    def init_parser(parser):
        parser.add_argument('--pingouin', action="store_true")

    @classmethod
    def init_args(cls, arg):
        cls.enabled = arg.pingouin

    @staticmethod
    def process(case, dop):
        q, k, nu = case.q, case.k, case.v
        atol = 10 ** (-dop)
        return 1 - psturng(q, k, nu)
