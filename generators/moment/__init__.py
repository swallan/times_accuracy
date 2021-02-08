from argparse import ArgumentError

from . import cython, mpgl, mpts

gens = [cython.Generator, mpgl.Generator, mpts.Generator]


class Case:
    def __init__(self, m, k, v):
        self.k, self.v, self.m = k, v, m
        self.case_set = "moment"
        self.uid = f"{self.case_set}-{m}-{k}-{v}"

    def __str__(self):
        return f"{self.case_set}-k={self.k}, v={self.v}, m={self.m}"


C = Case


class GenContainer:
    enabled = False

    cases = [
        C(1, 3, 1),
        C(1, 3, 10),
        C(1, 3, 120),
        C(1, 10, 1),
        C(1, 10, 10),
        C(1, 10, 120),
        C(1, 20, 1),
        C(1, 20, 10),
        C(1, 20, 120),

        C(2, 3, 1),
        C(2, 3, 10),
        C(2, 3, 120),
        C(2, 10, 1),
        C(2, 10, 10),
        C(2, 10, 120),
        C(2, 20, 1),
        C(2, 20, 10),
        C(2, 20, 120),

        C(3, 3, 1),
        C(3, 3, 10),
        C(3, 3, 120),
        C(3, 10, 1),
        C(3, 10, 10),
        C(3, 10, 120),
        C(3, 20, 1),
        C(3, 20, 10),
        C(3, 20, 120),

        C(4, 3, 1),
        C(4, 3, 10),
        C(4, 3, 120),
        C(4, 10, 1),
        C(4, 10, 10),
        C(4, 10, 120),
        C(4, 20, 1),
        C(4, 20, 10),
        C(4, 20, 120),
    ]

    @classmethod
    def init_parser(cls, parser):
        parser.add_argument('--moment', action='store_true',
                            help="Enable moment data generation.")

        for gen in gens:
            try:
                gen.init_parser(parser)
            except ArgumentError:
                print(
                    f"Error in init_parse for {gen.__name__}. This is probably not an issue. (duplicate args are expected)")

    @classmethod
    def init_args(cls, arg):
        cls.enabled = arg.moment

        for gen in gens:
            gen.init_args(arg)

    @classmethod
    def collect_processes(cls):
        if not cls.enabled:
            return

        enabled_classes = filter(lambda g: g.enabled, gens)

        # Return a tuple with the function, case.
        return [(f, c)
                for f in enabled_classes
                for c in cls.cases]
