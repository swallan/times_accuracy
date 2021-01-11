from mpmath import gamma, pi, erf, exp, sqrt, quad, inf, mpf
from mpmath import npdf as phi
from mpmath import ncdf as Phi
from mpmath import mp

def cdf_mp(q, k, nu, method, error=True, dps=15):
    mp.dps = dps
    q, k, nu = mpf(q), mpf(k), mpf(nu)

    def inner(s, z):
        return phi(z)*(Phi(z+q*s)-Phi(z))**(k-1)

    def outer(s, z):
        return s**(nu-1)*phi(sqrt(nu)*s)*inner(s, z)

    def whole(s, z):
        return sqrt(2*pi)*k*nu**(nu/2) / (gamma(nu/2)*2**(nu/2-1))*outer(s, z)
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

        return cdf_mp(q, k, nu, method='tanh-sinh', dps=dop)[0]
