from pingouin.external.qsturng import qsturng


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
        p, k, nu = case.p, case.k, case.v
        return qsturng(p, k, nu)
