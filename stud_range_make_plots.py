#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 14:43:11 2020

@author: swallan
"""

import numpy as np

from mpmath import gamma, pi, erf, exp, sqrt, quad, inf, mpf
from mpmath import npdf as phi
from mpmath import ncdf as Phi
from mpmath import mp

import matplotlib.pyplot as plt


# read in data and times from string.
with open("stud_range_data.txt", 'r') as in_:
    all_data = in_.read()
with open("stud_range_times.txt", 'r') as in_:
    all_times = in_.read()


# gather values and times from "dblquad", "mp-ts", Fortran, and C
Fs, Ts = None, None
exec(f"Fs = {all_data}")
exec(f"Ts = {all_times}")

# make sure these match how the data was generated
_min=6
_max=20
itr=1
dpss = np.array(range(_min, _max, itr))

# gather values from statsmodels:
from statsmodels.stats.libqsturng import psturng
import time
for F_key in Fs.keys():
    q, k, nu = F_key.split("-")
    print(q, k, nu)
    datas = []
    times = []
    for i in dpss:
        ti = time.time()
        try:
            call = psturng(float(q), int(k), int(nu))
            
        except:
            call = 3
        tf = time.time()
        datas.append(1 - call)
        dt = tf - ti
        times.append(dt)
        
    Fs[F_key]['psturng'] = datas
    Ts[F_key]['psturng'] = times
        



for F_key in Fs.keys():
    q, k, nu = F_key.split("-")
    F = Fs[F_key]
    gt = None
    exec(f'gt = {F["mp-ts"][-1]}')
    # make sure this is the correct range as how the data was generated.
    
    err2 = np.abs(np.array([x - gt for x in F["dblquad"]], dtype=float))
    err3 = np.abs(np.array([x - gt for x in F["mp-ts"]], dtype=float))
    err4 = np.abs(np.array([x - gt for x in F["ft"]], dtype=float))
    err5 = np.abs(np.array([x - gt for x in F["dom"]], dtype=float))
    err6 = np.abs(np.array([x - gt for x in F["psturng"]], dtype=float))

    
    # make a plot for each calcualtion (DATA)
    plt.semilogy(dpss, err2, dpss, err3, dpss, err4, dpss, err5, dpss, err6)
    plt.legend(("dblquad", "mp-ts", "Fortran", "C", "psturng"))
    plt.title(f'Magnitude Difference from \'mp-ts\'@{_max-1} \n'
              f'q: {q}, k: {k}, nu: {nu}')
    plt.ylabel('magnitude difference')
    plt.xlabel('degree of precision')
    plt.savefig(f"images/q{str(q).strip('.')}-k{int(k)}-nu{int(nu)}_DATA.png", dpi=250)
    plt.clf()

for T_key in Ts.keys():
    q, k, nu = T_key.split("-")
    T = Ts[T_key]
    # make plot for times
    plt.semilogy(dpss, T["dblquad"], dpss, T["mp-ts"], dpss, T["ft"], dpss, T["dom"], dpss, T["psturng"])
    plt.legend(("dblquad", "mp-ts", "Fortran", "C", "psturng"))
    plt.title(f'Computation Time at Different Levels of Accuracy'
              f'\nq: {q}, k: {k}, nu: {nu}')
    plt.ylabel('time (seconds)')
    plt.xlabel('degree of precision')
    plt.savefig(f"images/q{str(q).strip('.')}-k{int(k)}-nu{int(nu)}_TIME.png", dpi=250)
    plt.clf()