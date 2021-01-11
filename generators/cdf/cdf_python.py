import scipy.stats as stats
from scipy.integrate import quad, dblquad
from scipy.special import gamma
import numpy as np


phi = stats.distributions.norm.pdf
Phi = stats.distributions.norm.cdf

class Generator:
    enabled = False
    display_name = "python"

    @staticmethod
    def init_parser(parser):
        parser.add_argument('--python', action="store_true")

    @classmethod
    def init_args(cls, arg):
        cls.enabled = arg.python

    @staticmethod
    def process(case, dop):
        q, k, nu = case.q, case.k, case.v
        atol = 10 ** (-dop)

        def inner(s, z):
            return phi(z) * (Phi(z + q * s) - Phi(z)) ** (k - 1)

        def outer(s, z):
            inner_int = inner(s, z)
            return s ** (nu - 1) * phi(np.sqrt(nu) * s) * inner_int

        def whole(s, z):
            return (np.sqrt(2 * np.pi) * k * nu ** (nu / 2) /
                    (gamma(nu / 2) * 2 ** (nu / 2 - 1)) * outer(s, z))

        res = dblquad(whole, -np.inf, np.inf, lambda x: 0, lambda x: np.inf,
                      epsabs=atol)
        return res[0]
