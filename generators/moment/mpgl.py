from mpmath import gamma, pi, erf, exp, sqrt, quad, inf, mpf
from mpmath import npdf as phi
from mpmath import ncdf as Phi
from mpmath import mp

def pdf_mp(m, k, nu, method, error=True, dps=15):
    mp.dps = dps
    k, nu = mpf(k), mpf(nu)

    def integral(q, s, z):
        return k * (k - 1) * s * phi(z) * phi(s * q + z) \
               * (Phi(s * q + z) - Phi(z)) ** (k - 2)

    def whole(q, s, z):
        return q**m * nu ** (nu / 2) / (gamma(nu / 2) * 2 ** (nu / 2 - 1)) * s ** (
                    nu - 1) * exp(-nu * s ** 2 / 2) * integral(q, s, z)

    res = quad(whole, [0, inf], [0, inf], [-inf, inf], error=error,
               method=method, maxdegree=10)
    return res


class Generator:
    enabled = False
    display_name = "mpgl"

    @staticmethod
    def init_parser(parser):
        parser.add_argument('--mpgl', action="store_true")

    @classmethod
    def init_args(cls, arg):
        cls.enabled = arg.mpgl

    @staticmethod
    def process(case, dop):
        m, k, nu = case.m, case.k, case.v

        return pdf_mp(m, k, nu, method='gauss-legendre', dps=dop)[0]
