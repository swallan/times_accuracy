import scipy.stats as stats
from scipy.integrate import quad, dblquad
from scipy.special import gamma
import numpy as np


phi = stats.distributions.norm.pdf
Phi = stats.distributions.norm.cdf

class Generator:
    enabled = False
    display_name = "cdf-fortan"

    @staticmethod
    def init_parser(parser):
        parser.add_argument('--fortran', action="store_true")

    @classmethod
    def init_args(cls, arg):
        cls.enabled = arg.fortran

    @staticmethod
    def process(case, dop):
        q, k, nu = case.q, case.k, case.v
        atol = 10 ** (-dop)

        return 0
