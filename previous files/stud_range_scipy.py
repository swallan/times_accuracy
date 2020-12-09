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


def F_R(q, k, nu=np.inf):
    """CDF of studentized range distribution"""
    # Direct implementation of formulas from Wikipedia
    # https://en.wikipedia.org/wiki/Studentized_range_distribution
    if nu > 40:
        # asymptotic version
        # results may not be very accurate for 40 < nu < 120;
        def integrand(z):
            return phi(z)*(Phi(z+q)-Phi(z))**(k-1)
        F, err = quad(integrand, -np.inf, np.inf, epsabs=1e-12, limit=1000)
        return k*F

    def outer(s):
        def inner(z):
            return phi(z)*(Phi(z+q*s)-Phi(z))**(k-1)
        inner_int = quad(inner, -np.inf, np.inf, epsabs=1e-12, limit=1000)[0]
        return s**(nu-1)*phi(np.sqrt(nu)*s)*inner_int

    outer_int = quad(outer, 0, np.inf, epsabs=1e-12, limit=1000)[0]
    return np.sqrt(2*np.pi)*k*nu**(nu/2) / (gamma(nu/2)*2**(nu/2-1))*outer_int


def F_R2(q, k, nu, atol=1.49e-08, rtol=1.49e-08):
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


def F_R3(q, k, nu, method='tanh-sinh', verbose=True, error=True, dps=15):
    mp.dps = dps
    q, k, nu = mpf(q), mpf(k), mpf(nu)
    print(f"Using q={q}, k={k}, nu={nu}")

    def inner(s, z):
        return phi(z)*(Phi(z+q*s)-Phi(z))**(k-1)

    def outer(s, z):
        return s**(nu-1)*phi(sqrt(nu)*s)*inner(s, z)

    def whole(s, z):
        return sqrt(2*pi)*k*nu**(nu/2) / (gamma(nu/2)*2**(nu/2-1))*outer(s, z)
    res = quad(whole, [0, inf], [-inf, inf], error=error,
               method=method, maxdegree=10)
    return res

from scipy.stats.statlib import prtrng
def F_R4(q, k, nu):
    return prtrng(q, nu, k)[0], None
    

from scipy.stats import studentized_cdf
def F_R5(q, k, nu, atol=1.49e-08, rtol=1.49e-08):
    return studentized_cdf(q, k, nu, atol=atol, rtol=rtol), None


q = mpf('6.87')
k = mpf(8)
nu = mpf(10)

import time

def plot_mag_diff(q, k, nu, _min=6, _max=20, itr=1):
    F = {"dblquad":[], "mp-ts":[], "mp-gl":[], "ft":[], "dom":[]}
    T = {"dblquad":[], "mp-ts":[], "mp-gl":[], "ft":[], "dom":[]}

    dpss = range(_min, _max, itr)
    for dps in dpss:
        print(f"dps:{dps}")

        # dblquad
        T2_i = time.time()
        F2, err2 = F_R2(q, k, nu, atol=10**(-dps))
        T2_F = time.time()
        T2 = T2_F - T2_i

        # mp-ts
        T3_i = time.time()
        F3, err3 = F_R3(q, k, nu, method='tanh-sinh', dps=dps)
        T3_F = time.time()
        T3 = T3_F - T3_i

        # Fortran
        T5_i = time.time()
        F5, err5 = F_R4(q, k, nu)
        T5_F = time.time()
        T5 = T5_F - T5_i

        # C
        T6_i = time.time()
        F6, err6 = F_R5(float(q), float(k), float(nu), atol=10**(-dps))
        T6_F = time.time()
        T6 = T6_F - T6_i

        F["dblquad"].append(F2)
        F["mp-ts"].append(F3)
        F["ft"].append(F5)
        F["dom"].append(F6)

        T["dblquad"].append(T2)
        T["mp-ts"].append(T3)
        T["ft"].append(T5)
        T["dom"].append(T6)

    return F, T


# most Q_crits are under 20.
q_crits = [26.976, 6.825, 4.577]
ks = [1, 10, 30, 100]
nus = [3, 5, 10]

datas = dict()
times = dict()

start_time = time.time()
for q in q_crits:
    for k in ks:
        for nu in nus:
            print(f'starting: q: {q}, k: {k}, nu: {nu}')
            t1 = time.time()
            d, t = plot_mag_diff(mpf(str(q)), mpf(k), mpf(nu))
            t2 = time.time()
            t_run = t2-t1
            print(f"this run: {t_run / 60} minutes.")
            datas[f'{q}-{k}-{nu}'] = d
            times[f'{q}-{k}-{nu}'] = t

end_time = time.time()

time_elapsed_total = end_time - start_time
print(f"time elapsed: {time_elapsed_total / 60} minutes")
with open("stud_range_data.txt", 'w+') as out:
    out.write(f"{str(datas)}")
with open("stud_range_times.txt", 'w+') as out:
    out.write(f"{str(times)}")
