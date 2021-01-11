from mpmath import gamma, pi, erf, exp, sqrt, quad, inf, mpf
from mpmath import npdf as phi
from mpmath import ncdf as Phi
from mpmath import mp


def pdf_mp(q, k, nu, method, error=True, dps=15):
    mp.dps = dps
    q, k, nu = mpf(q), mpf(k), mpf(nu)

    def integral(s, z):
        return k * (k - 1) * s * phi(z) * phi(s * q + z) \
               * (Phi(s * q + z) - Phi(z)) ** (k - 2)

    def whole(s, z):
        return nu ** (nu / 2) / (gamma(nu / 2) * 2 ** (nu / 2 - 1)) * s ** (
                    nu - 1) * exp(-nu * s ** 2 / 2) * integral(s, z)

    res = quad(whole, [0, inf], [-inf, inf], error=error,
               method=method, maxdegree=10)
    return res



class Generator:
    enabled = False
    display_name = "mpts"

    @staticmethod
    def init_parser(parser):
        parser.add_argument('--mpts', action="store_true")

    @classmethod
    def init_args(cls, arg):
        cls.enabled = arg.mpts

    @staticmethod
    def process(case, dop):
        q, k, nu = case.q, case.k, case.v

        return pdf_mp(q, k, nu, method='tanh-sinh', dps=dop)[0]
