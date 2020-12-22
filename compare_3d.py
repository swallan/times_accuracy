#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 20:06:36 2020

@author: swallan
"""
import numpy as np
from compute_cdf import (cdf_dblquad, cdf_mp_ts, cdf_mp_gl, cdf_fortran,
                         cdf_cplusplus, cdf_statsmodel, cdf_cython)
cdf1 = cdf_cplusplus
cdf2 = cdf_mp_ts


cdf1_vals = dict()
cdf2_vals = {'1-1': 0.9999999999999994,
 '1-6': 0.9999999999999918,
 '1-11': 0.9999999999999994,
 '1-16': 0.9999999999999999,
 '1-21': 1.0000000000000002,
 '1-26': 1.0000000000000058,
 '1-31': 1.000000000000006,
 '1-36': 0.9999999999999979,
 '1-41': 1.0000000000000009,
 '1-46': 0.999999999999996,
 '1-51': 0.9999999999999998,
 '1-56': 1.000000000000009,
 '1-61': 0.9999999999999948,
 '1-66': 0.9999999999999913,
 '1-71': 1.0000000000000009,
 '1-76': 1.0000000000000067,
 '1-81': 0.9999999999999958,
 '1-86': 1.0000000000000004,
 '1-91': 0.9999999999999946,
 '1-96': 0.9999999999999946,
 '1-101': 0.9999999999999917,
 '1-106': 0,
 '1-111': 0,
 '1-116': 0,
 '3-1': 0.6634898016605872,
 '3-6': 0.917897322034067,
 '3-11': 0.9474369976382722,
 '3-16': 0.9580864724187199,
 '3-21': 0.9634779459782356,
 '3-26': 0.9667126070110341,
 '3-31': 0.9688622365024516,
 '3-36': 0.9703918448571385,
 '3-41': 0.9715347855887144,
 '3-46': 0.9724207033481188,
 '3-51': 0.9731272628270153,
 '3-56': 0.9737037749468936,
 '3-61': 0.9741830303494661,
 '3-66': 0.974587671529035,
 '3-71': 0.9749338307474997,
 '3-76': 0.9752333096429271,
 '3-81': 0.9754949391311094,
 '3-86': 0.9757254576950813,
 '3-91': 0.9759300957833494,
 '3-96': 0.9761129748910032,
 '3-101': 0.9762773863872367,
 '3-106': 0,
 '3-111': 0,
 '3-116': 0,
 '5-1': 0.5487536393832501,
 '5-6': 0.8287726871839999,
 '5-11': 0.8769320265146981,
 '5-16': 0.8965828611952357,
 '5-21': 0.9071691919163707,
 '5-26': 0.9137636109406593,
 '5-31': 0.9182578141833719,
 '5-36': 0.9215141048120323,
 '5-41': 0.9239805973290852,
 '5-46': 0.9259128450581758,
 '5-51': 0.9274670846118174,
 '5-56': 0.9287441437125493,
 '5-61': 0.9298119725609624,
 '5-66': 0.9307180187131547,
 '5-71': 0.9314964091632699,
 '5-76': 0.9321723136888861,
 '5-81': 0.9327646999231443,
 '5-86': 0.9332881312419875,
 '5-91': 0.933753973958114,
 '5-96': 0.9341712283476002,
 '5-101': 0.9345471134315831,
 '5-106': 0,
 '5-111': 0,
 '5-116': 0,
 '7-1': 0.484745870370035,
 '7-6': 0.7508273568800958,
 '7-11': 0.8065551765261989,
 '7-16': 0.8312395522189123,
 '7-21': 0.8451483075560057,
 '7-26': 0.8540614050568989,
 '7-31': 0.8602555613145986,
 '7-36': 0.8648080198484462,
 '7-41': 0.8682940017566053,
 '7-46': 0.8710484068720344,
 '7-51': 0.873279349580022,
 '7-56': 0.8751229221841751,
 '7-61': 0.8766718466130664,
 '7-66': 0.8779914641463898,
 '7-71': 0.8791291407337462,
 '7-76': 0.8801200466687503,
 '7-81': 0.8809908420842663,
 '7-86': 0.8817621027477343,
 '7-91': 0.882449961223506,
 '7-96': 0.8830672442318298,
 '7-101': 0.8836242777938211,
 '7-106': 0,
 '7-111': 0,
 '7-116': 0,
 '9-1': 0.4421686976688824,
 '9-6': 0.684766959737139,
 '9-11': 0.7413407274872665,
 '9-16': 0.7678637265798423,
 '9-21': 0.7833190224225135,
 '9-26': 0.7934445791437003,
 '9-31': 0.8005921835759355,
 '9-36': 0.8059068256823961,
 '9-41': 0.8100131641806644,
 '9-46': 0.8132810108932003,
 '9-51': 0.815943270942065,
 '9-56': 0.8181539256640022,
 '9-61': 0.8200188477060222,
 '9-66': 0.821613224811701,
 '9-71': 0.82299192322647,
 '9-76': 0.8241959172525507,
 '9-81': 0.8252564233101181,
 '9-86': 0.8261976408565349,
 '9-91': 0.8270386187040383,
 '9-96': 0.8277945558493494,
 '9-101': 0.8284777270804478,
 '9-106': 0,
 '9-111': 0,
 '9-116': 0,
 '11-1': 0.4110702724832119,
 '11-6': 0.6287904681896236,
 '11-11': 0.6824776024426077,
 '11-16': 0.7086583848837673,
 '11-21': 0.7243045779664855,
 '11-26': 0.7347346843870434,
 '11-31': 0.7421907170851604,
 '11-36': 0.7477879611788469,
 '11-41': 0.7521451766507166,
 '11-46': 0.7556336314735738,
 '11-51': 0.7584897202886838,
 '11-56': 0.7608711574692764,
 '11-61': 0.7628872157221345,
 '11-66': 0.76461600640008,
 '11-71': 0.7661148519115808,
 '11-76': 0.7674267721620693,
 '11-81': 0.7685846843233545,
 '11-86': 0.7696142044947034,
 '11-91': 0.7705355658473348,
 '11-96': 0.7713649621426523,
 '11-101': 0.7721155079408247,
 '11-106': 0,
 '11-111': 0,
 '11-116': 0,
 '13-1': 0.3869888139296891,
 '13-6': 0.5809998192261593,
 '13-11': 0.6298561533877761,
 '13-16': 0.6543157468241259,
 '13-21': 0.6692084640889232,
 '13-26': 0.6792709429389305,
 '13-31': 0.6865371846339516,
 '13-36': 0.6920347914658337,
 '13-41': 0.6963411766019078,
 '13-46': 0.6998064580183748,
 '13-51': 0.7026555274559589,
 '13-56': 0.7050395408009897,
 '13-61': 0.7070638918481007,
 '13-66': 0.7088043321100217,
 '13-71': 0.7103167176335334,
 '13-76': 0.7116431436594813,
 '13-81': 0.7128159394232452,
 '13-86': 0.7138603467289435,
 '13-91': 0.7147963622477205,
 '13-96': 0.7156400332570159,
 '13-101': 0.7164043871763773,
 '13-106': 0,
 '13-111': 0,
 '13-116': 0}

diffs = dict()

q = 3.778
ks = range(1, 15, 2)
nus = range(1, 121, 5)

for k in ks:
    for nu in nus:
        print(f"{q}-{k}-{nu}")
        try:
            p1 = cdf1(q, k, nu, dps=10)[0]
        except Exception as e:
            print(f"{q}-{k}-{nu}: {e}")
            p1 = None
        # try:
        #     p2 = cdf2(q, k, nu, dps=10)[0]
        # except Exception as e:
        #     print(f"{q}-{k}-{nu}: {e}")
        #     p2 = None
        cdf1_vals[f'{k}-{nu}'] = p1
        # cdf2_vals[f'{k}-{nu}'] = p2
        p2 = cdf2_vals[f'{k}-{nu}']
        if p1 is None or p2 is None:
            diffs[f'{k}-{nu}'] = None
        else:
            diffs[f'{k}-{nu}'] = np.abs(p1 - p2)
            
            
#%%
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
fig = plt.figure()
ax = fig.gca(projection='3d')
Z1 = Z + .00000000001
my_col = cm.jet(Z1/np.amax(Z1))
s= ax.scatter(X, Y , Z1,)#facecolors = my_col, )
                        
ax.zaxis.set_major_locator(LinearLocator(10))
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
# ax.set_zscale('log')
# fig.colorbar(s, shrink=0.5, aspect=5)
# ax.set_zlim(-35, -25)

plt.show()
#%%

# # Make data.
# X = np.arange(-5, 5, 0.25)
# Y = np.arange(-5, 5, 0.25)
# X, Y = np.meshgrid(X, Y)
# R = np.sqrt(X**2 + Y**2)
# Z = np.sin(R)

# Plot the surface.
surf = ax.plot_surface(X, Y, Z2, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(0, .00000000001)
ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.000005f'))
# ax.zaxis

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()          
