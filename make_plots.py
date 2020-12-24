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

mp.dps = 30

# read in data and times from string.

Fs, Ts = dict(), dict()
names = ['cdf_dblquad', 'cdf_mp_ts', 'cdf_mp_gl', 'cdf_fortran',
           'cdf_statsmodel','cdf_cython_old','cdf_cython'] #,


for name in names:
    try:
        with open(f"data/{name}_data1.txt", 'r') as in_:
            data = in_.read()
            data = data.replace('nan', '2')
            f = f'Fs["{name}"] = {data}'
            exec(f.replace('array', ''))
    except Exception as e:
        print(f"[FileError] Data may not be loaded for {name}, errmsg= {e}")
    try:
        with open(f"data/{name}_time1.txt", 'r') as in_:
            data = in_.read()
            f = f'Ts["{name}"] = {data}'
            exec(f.replace('array', ''))
    except Exception as e:
        print(f"[FileError] Time may not be loaded for {name}, errmsg= {e}")
        
        
        
print(f'data loaded for {len(Fs.keys())}/{len(names)} {Fs.keys() if len(Fs.keys()) != len(names) else ""}')
print(f'time loaded for {len(Ts.keys())}/{len(names)} {Ts.keys() if len(Ts.keys()) != len(names) else ""}')

#%%

# make sure these match how the data was generated
_min=6
_max=26
itr=1
dpss = np.array(range(_min, _max, itr))





err = []
for key_comp in Fs['cdf_mp_ts']:
    strip = key_comp.split("-")
    if len(strip) == 4:
        q, k, nu = strip[1:]
        q = '-' + q
    else:
        q, k, nu = strip
    print(key_comp)
    
    failed = []
    
    
    

    gt = Fs["cdf_mp_ts"][key_comp][-1]    
    err = [np.abs([x - gt for x in np.ravel(Fs[key_name][key_comp])])
                   for key_name in Fs.keys()]

    for key_name in Fs.keys():
        l = np.abs([x - gt for x in np.ravel(Fs[key_name][key_comp])])
        if np.any(l > .5):
            failed.append(key_name)
    # make a plot for each calcualtion (DATA)
    #%%
   
    plt.figure(figsize=(9,6), dpi=250)
    plt.semilogy(*[x for y in zip([dpss]*len(err), err) for x in y], marker='o', markersize=2, alpha=.7)
    legend_nice_label = [key[4:] for key in Fs.keys()]
    plt.legend(legend_nice_label)
    plt.xticks(range(6, 26, 1))
    plt.title(f'Magnitude Difference from \'mp-ts\'@{_max-1}: alpha={1-float(gt):.3f} \n'
              f'q: {q}, k: {k}, nu: {nu}, ')
    plt.ylabel('magnitude difference')
    plt.xlabel('degree of precision')
    #%%
    if len(failed) > 0:
        plt.figtext(0.99, 0.01, f'possible failures: {failed}, meaning the error was over .5', horizontalalignment='right')
    plt.savefig(f"images/data/alpha{1-float(gt):.3f}-q{float(q)}-k{int(k)}-nu{int(nu)}_DATA.png", dpi=250)
    plt.clf()
    plt.close()
    
    
    
    # plt.figure(figsize=(9,6), dpi=250)
    # times = [Ts[key_name][key_comp] for key_name in Ts.keys()]
    # plt.semilogy(*[x for y in zip([dpss]*len(err), times) for x in y], marker='o', markersize=2)
    # legend_nice_label = [key[4:] for key in Fs.keys()]
    # plt.legend(legend_nice_label)
    # plt.xticks(range(6, 26, 1))
    # plt.title(f'Execution Time @ Degree Precision \'mp-ts\'@{_max-1}: alpha={1-float(gt):.3f}\n'
    #           f'q: {q}, k: {k}, nu: {nu}')
    # plt.ylabel('time (seconds)')
    # plt.xlabel('degree of precision')
    # plt.figtext(0.99, 0.01, '* `mp-ts`, `mp-gl`, and `dblquad` were run on a different system', horizontalalignment='right')
    # #%%
    
    # plt.savefig(f"images/time/q{str(q).strip('.')}-k{int(k)}-nu{int(nu)}_TIME.png", dpi=250)
    # plt.clf()
    # plt.close()
    
    
    

# for T_key in Ts.keys():
#     q, k, nu = T_key.split("-")
#     T = Ts[T_key]
#     # make plot for times
#     plt.semilogy(dpss, T["dblquad"], dpss, T["mp-ts"], dpss, T["ft"], dpss, T["dom"], dpss, T["psturng"])
#     plt.legend(("dblquad", "mp-ts", "Fortran", "C", "psturng"))
#     plt.title(f'Computation Time at Different Levels of Accuracy'
#               f'\nq: {q}, k: {k}, nu: {nu}')
#     plt.ylabel('time (seconds)')
#     plt.xlabel('degree of precision')
#     plt.savefig(f"images/q{str(q).strip('.')}-k{int(k)}-nu{int(nu)}_TIME.png", dpi=250)
#     plt.clf()

