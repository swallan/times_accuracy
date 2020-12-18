
"""
Created on Fri Dec  4 18:28:22 2020

@author: swallan
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:02:37 2020

@author: mhaberla
"""

from scipy.stats import norm
from scipy.integrate import quad, dblquad
import numpy as np
from numpy.testing import assert_allclose
from scipy.special import gamma
import matplotlib.pyplot as plt
from numpy import random as rnd

phi = norm.pdf
Phi = norm.cdf

def cdf_dblquad(q, k, nu, dps, atol=1.49e-08, rtol=1.49e-08):
    atol = 10**(-dps)
    def inner(s, z):
        return phi(z)*(Phi(z+q*s)-Phi(z))**(k-1)

    def outer(s, z):
        inner_int = inner(s, z)
        return s**(nu-1)*phi(np.sqrt(nu)*s)*inner_int

    def whole(s, z):
        return (np.sqrt(2*np.pi)*k*nu**(nu/2) /
                (gamma(nu/2)*2**(nu/2-1))*outer(s, z))
    res = dblquad(whole, -np.inf, np.inf, lambda x: 0, lambda x: np.inf,
                  epsabs=atol, epsrel=rtol)
    return res



from mpmath import gamma, pi, erf, exp, sqrt, quad, inf, mpf
from mpmath import npdf as phi
from mpmath import ncdf as Phi
from mpmath import mp


def cdf_mp(q, k, nu, method, verbose=True, error=True, dps=15):
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


def cdf_mp_gl(q, k, nu, verbose=True, error=True, dps=15):
    return cdf_mp(q, k, nu, method='gauss-legendre', verbose=verbose,
                  error=error, dps=dps)


def cdf_mp_ts(q, k, nu, verbose=True, error=True, dps=15):
    return cdf_mp(q, k, nu, method='tanh-sinh', verbose=verbose, error=error,
                  dps=dps)


def cdf_fortran(q, k, nu, *args, **kwargs):
    from scipy.stats.statlib import prtrng
    # there is no way to improve the accuracy of this function.
    return prtrng(q, nu, k)[0], None


def cdf_cplusplus(q, k, nu, *args, **kwds):
    from scipy.stats import studentized_cdf
    if kwds.get('dps'):
        atol = 10**-(kwds.get('dps'))
    else:
        atol = 1.49e-08
    return studentized_cdf(q, k, nu, atol=atol), None

def cdf_statsmodel(q, k, nu, *args, **kwds):
    from statsmodels.stats.libqsturng import psturng
    try:
        return 1 - psturng(q, k, nu).item(), None
    except: 
        return 2, None

def cdf_cython(q, k, nu, *args, **kwds):
    from scipy.stats import studentized_t as srd
    atol = 10**-(kwds.get('dps', 8))
    # print(atol)
    return srd._cdf((q, atol), k, nu), None


