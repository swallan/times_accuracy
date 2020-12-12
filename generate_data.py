#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 16:36:10 2020

@author: swallan
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from compute_cdf import (cdf_dblquad, cdf_mp_ts, cdf_mp_gl, cdf_fortran,
                         cdf_cplusplus, cdf_statsmodel, cdf_cython)
import time

q_crits = [26.976, 6.825, 4.577]
ks = [3, 5, 10]
nus = [10, 30, 100]

from mpmath import mp
mp.dps = 25
#%%
# indicate which you would like to have data generated for
truths = [False, False, False, False, True, False, False]
methods = [cdf_dblquad, cdf_mp_ts, cdf_mp_gl, cdf_fortran, cdf_cplusplus, cdf_statsmodel, cdf_cython]
names = ['cdf_dblquad', 'cdf_mp_ts', 'cdf_mp_gl', 'cdf_fortran', 'cdf_cplusplus',
         'cdf_statsmodel', 'cdf_cython']


F_R = dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict()
F_T = dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict()


def compute_and_time(fun, F, T, q, k, nu, _min=6, _max=26, itr=1):
    dpss = range(_min, _max, itr)
    for dps in dpss:
        
        print(f"dps:{dps}")
        key = f'{q}-{k}-{nu}'
        Ti = time.time()
        F2, err2 = fun(q, k, nu, dps=dps)
        Tf = time.time()
        dt = Tf - Ti
        F[key].append(F2)
        T[key].append(dt)


start_time = time.time()
for q in q_crits:
    for k in ks:
        for nu in nus:
            print(f'starting: q: {q}, k: {k}, nu: {nu}')
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
        fnameData = f"data/{names[i]}_data.txt"
        fnameTime = f"data/{names[i]}_time.txt"
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
