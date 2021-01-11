from argparse import ArgumentError

from . import cdf_python, cdf_cython, cdf_fortran, cdf_mpgl, cdf_mpts

gens = [cdf_python.Generator, cdf_cython.Generator, cdf_fortran.Generator, cdf_mpgl.Generator, cdf_mpts.Generator]


class Case:
    def __init__(self, p, q, k, v):
        self.q, self.k, self.v, self.p = q, k, v, p
        self.case_set = "cdf"
        self.uid = f"{self.case_set}-{p}-{q}-{k}-{v}"

    def __str__(self):
        return f"{self.case_set}-q={self.q}, k={self.k}, v={self.v}, p={self.p}"


C = Case


class GenContainer:
    enabled = False

    cases = [
        C(0.001, 1476.5333964074937, 3, 1),
        C(0.001, 7.41070742788097, 3, 10),
        C(0.001, 5.21064641034589, 3, 120),
        C(0.001, 2435.021291209218, 10, 1),
        C(0.001, 9.76993411237901, 10, 10),
        C(0.001, 6.205695750861473, 10, 120),
        C(0.001, 2947.645607159285, 20, 1),
        C(0.001, 11.036493347521253, 20, 10),
        C(0.001, 6.695024219374616, 20, 120),

        C(0.01, 134.77261873831876, 3, 1),
        C(0.01, 5.270172252505278, 3, 10),
        C(0.01, 4.199944173590739, 3, 120),
        C(0.01, 244.8897708144631, 10, 1),
        C(0.01, 7.213394084352993, 10, 10),
        C(0.01, 5.299214160889432, 10, 120),
        C(0.01, 298.23872178428456, 20, 1),
        C(0.01, 8.225917112372644, 20, 10),
        C(0.01, 5.827186942720529, 20, 120),

        C(0.05, 26.96497723848384, 3, 1),
        C(0.05, 3.876778769063178, 3, 10),
        C(0.05, 3.3561384354345702, 3, 120),
        C(0.05, 49.090185505578575, 10, 1),
        C(0.05, 5.598390407973096, 10, 10),
        C(0.05, 4.559538018435397, 10, 120),
        C(0.05, 59.50675453132768, 20, 1),
        C(0.05, 6.467008871355576, 20, 10),
        C(0.05, 5.1259429030139385, 20, 120),

        C(0.5, 2.33738608679169, 3, 1),
        C(0.5, 1.6446890195113466, 3, 10),
        C(0.5, 1.5924063120539134, 3, 120),
        C(0.5, 4.491994152617345, 10, 1),
        C(0.5, 3.1368105218984836, 10, 10),
        C(0.5, 3.033699116937617, 10, 120),
        C(0.5, 5.514467779302668, 20, 1),
        C(0.5, 3.828559872259776, 20, 10),
        C(0.5, 3.698753334121135, 20, 120),

        C(0.9, 1.706958976157801, 10, 1),
        C(0.9, 1.989079109205615, 10, 10),
        C(0.9, 2.083518362913231, 10, 120),
        C(0.9, 2.1666456599090287, 20, 1),
        C(0.9, 2.6251959972375243, 20, 10),
        C(0.9, 2.814728881330585, 20, 120),

        C(0.99, 0.9467459184172438, 10, 1),
        C(0.99, 1.3329441146005874, 10, 10),
        C(0.99, 1.4529450970397833, 10, 120),
        C(0.99, 1.2720720538395054, 20, 1),
        C(0.99, 1.9422724694176192, 20, 10),
        C(0.99, 2.2151122178864724, 20, 120),
    ]

    @classmethod
    def init_parser(cls, parser):
        parser.add_argument('--cdf', action='store_true',
                            help="Enable CDF data generation.")

        for gen in gens:
            try:
                gen.init_parser(parser)
            except ArgumentError:
                print(
                    f"Error in init_parse for {gen.__name__}. This is probably not an issue. (duplicate args are expected)")

    @classmethod
    def init_args(cls, arg):
        cls.enabled = arg.cdf

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
