#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 16:36:10 2020

@author: swallan
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from compute_cdf import (cdf_dblquad, cdf_mp_ts, cdf_mp_gl, cdf_fortran,
                         cdf_cplusplus, cdf_statsmodel, cdf_cython, cdf_cython)
import time
import argparse
import sys
import concurrent.futures


#%%

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dblquad', action='store_true')
parser.add_argument('-t', '--mpts', action='store_true')
parser.add_argument('-g', '--mpgl', action='store_true')
parser.add_argument('-f', '--fortran', action='store_true')
parser.add_argument('-s', '--statsmodel', action='store_true')
parser.add_argument('-c', '--cython', action='store_true')
parser.add_argument('-c_o', '--cython_old', action='store_true')
parser.add_argument('-cpp', '--cplusplus', action='store_true')
arg = parser.parse_args()
print(arg)

# indicate which you would like to have data generated for
truths = [arg.dblquad,  # dblquad
          arg.mpts,  # mp-ts
          arg.mpgl,  # mp-gl
          arg.fortran,  # Fortran
          arg.statsmodel,  # statsmodel
          arg.cython,   # Cython
          arg.cplusplus,
          arg.cython_old
          ]
methods = [cdf_dblquad, cdf_mp_ts, cdf_mp_gl, cdf_fortran,
           cdf_statsmodel, cdf_cython, cdf_cplusplus, cdf_cython]
names = ['cdf_dblquad', 'cdf_mp_ts', 'cdf_mp_gl', 'cdf_fortran',
         'cdf_statsmodel', 'cdf_cython', 'cdf_cplusplus', 'cdf_cython_old']


# for i in len(truths):
#     in_ = input(f"calculate for {names[i]} (enter 't' or 'f')")
#     if in_ == 't':
#         truth
#%%

ps = [0.001, 0.01, 0.05, 0.5, 0.9, 0.99]
ks = [3, 10, 20]
nus = [1, 10, 120]
# nu = 1, k =10

# def wrapper(a, k, nu):
#     import scipy.optimize as optimize
#     # from scipy.stats import studentized_range
#     def func(q, k, nu):
#         return a - (1 - cdf_cython(q , k, nu, dps=10)[0])
#     return optimize.root(func, 3, args=(k, nu))

# combinations = dict()
# impossible_sets = dict()
# for p in ps:
#     combinations[p] = []
#     impossible_sets[p] = []
#     for k in ks:
#         for nu in nus:
#             try:
#                 q_wrap = wrapper(p, k, nu)
#                 if q_wrap.success:
#                     q = (q_wrap.x).item()
#                     combinations[p].append((q, k, nu))
#                 else:
                    
#                     q = None
#                     impossible_sets[p].append((q, k, nu))
#             except:
#                 q = None
#                 impossible_sets[p].append((q, k, nu))

combinations_old = {
    0.001: [(1476.5333964074937, 3, 1),
            (7.41070742788097, 3, 10),
            (5.21064641034589, 3, 120),
            (2435.021291209218, 10, 1),
            (9.76993411237901, 10, 10),
            (6.205695750861473, 10, 120),
            (2947.645607159285, 20, 1),
            (11.036493347521253, 20, 10),
            (6.695024219374616, 20, 120)],
    00.01: [(134.77261873831876, 3, 1),
            (5.270172252505278, 3, 10),
            (4.199944173590739, 3, 120),
            (244.8897708144631, 10, 1),
            (7.213394084352993, 10, 10),
            (5.299214160889432, 10, 120),
            (298.23872178428456, 20, 1),
            (8.225917112372644, 20, 10),
            (5.827186942720529, 20, 120)],
    00.05: [(26.96497723848384, 3, 1),
            (3.876778769063178, 3, 10),
            (3.3561384354345702, 3, 120),
            (49.090185505578575, 10, 1),
            (5.598390407973096, 10, 10),
            (4.559538018435397, 10, 120),
            (59.50675453132768, 20, 1),
            (6.467008871355576, 20, 10),
            (5.1259429030139385, 20, 120)],
    000.5: [(2.33738608679169, 3, 1),
            (1.6446890195113466, 3, 10),
            (1.5924063120539134, 3, 120),
            (4.491994152617345, 10, 1),
            (3.1368105218984836, 10, 10),
            (3.033699116937617, 10, 120),
            (5.514467779302668, 20, 1),
            (3.828559872259776, 20, 10),
            (3.698753334121135, 20, 120)],
    000.9: [(1.706958976157801, 10, 1),
            (1.989079109205615, 10, 10),
            (2.083518362913231, 10, 120),
            (2.1666456599090287, 20, 1),
            (2.6251959972375243, 20, 10),
            (2.814728881330585, 20, 120)],
    00.99: [(0.9467459184172438, 10, 1),
            (1.3329441146005874, 10, 10),
            (1.4529450970397833, 10, 120),
            (1.2720720538395054, 20, 1),
            (1.9422724694176192, 20, 10),
            (2.2151122178864724, 20, 120)]}

# combinations that fortran was not able to compute
combinations = {
    .99: [(0.19191582566250495, 3, 1),
         (0.19104171615970045, 3, 10),
         (0.19094499182679212, 3, 120)
         ],
    .9: [(-0.6526254674216354, 3, 1),
         (0.6216476924617348, 3, 10),
         (-0.6183524806284062, 3, 120)
        ]
    }

from mpmath import gamma, pi, erf, exp, sqrt, quad, inf, mpf
from mpmath import npdf as phi
from mpmath import ncdf as Phi
from mpmath import mp

mp.dps = 25
#%%
Fs, Ts = dict(), dict()

# for name in names:
#     try:
#         with open(f"data/{name}_data.txt", 'r') as in_:
#             data = in_.read()
#             f = f'Fs["{name}"] = {data}'
#             exec(f.replace('array', ''))
#     except Exception as e:
#         print(f"[FileError] Data may not be loaded for {name}, errmsg= {e}")
#     try:
#         with open(f"data/{name}_time.txt", 'r') as in_:
#             data = in_.read()
#             f = f'Ts["{name}"] = {data}'
#             exec(f.replace('array', ''))
#     except Exception as e:
#         print(f"[FileError] Time may not be loaded for {name}, errmsg= {e}")
        
        
        
# print(f'data loaded for {len(Fs.keys())}/{len(names)} methods {Fs.keys() if len(Fs.keys()) != len(names) else ""}')
# print(f'time loaded for {len(Ts.keys())}/{len(names)} {Ts.keys() if len(Ts.keys()) != len(names) else ""}')

F_R = [dict() for name in names]
F_T = [dict() for name in names]


def compute_and_time(fun, F, T, q, k, nu, _min=6, _max=26, itr=1):
    dpss = range(_min, _max, itr)
    for dps in dpss:
        
        print(f"dps:{dps}")
        key = f'{q}-{k}-{nu}'
        Ti = time.time()
        try:
            F2, err2 = fun(q, k, nu, dps=dps)
        except Exception as e:
            print(e)
            F2, err2 = 2, 2
        Tf = time.time()
        dt = Tf - Ti
        F[key].append(F2)
        T[key].append(dt)


start_time = time.time()
for p, value in combinations.items():
    print(f"p val: {p} ----------")
    for q, k, nu in value:
        print(f'starting: q: {q:.5}.., k: {k}, nu: {nu}')
        for i in range(len(truths)):
            if truths[i]:
                print(f"running {names[i]}")
                key = f'{q}-{k}-{nu}'
                F_R[i][key], F_T[i][key] = [], []
                compute_and_time(methods[i], F_R[i], F_T[i], q, k, nu)

end_time = time.time()
#%%
print("saving files...")

mp.dps = 25

for i in range(len(truths)):
    if truths[i]:
        fnameData = f"data/{names[i]}_data1.txt"
        fnameTime = f"data/{names[i]}_time1.txt"
        data = str(F_R[i])
        time = str(F_T[i])
        with open(fnameData, 'w+') as out_:
            out_.write(data)
            print(f"wrote to {fnameData}.")
        with open(fnameTime, 'w+') as out_:
            out_.write(time)
            print(f"wrote to {fnameTime}.")

time_elapsed_total = end_time - start_time
print(f"time elapsed: {time_elapsed_total / 60} minutes")
print("done")
