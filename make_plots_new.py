import numpy as np
import pickle
from Result import Result
import argparse
import matplotlib.pyplot as plt

availible_colors = ['c', 'm', 'y', 'k', 'r', 'g', 'b']


reference_func = "mpgl"
data_file_path = "./data.p"

results = pickle.load(open(data_file_path, "rb"))

# Step 1: Identify all present functions
# The function results for this set
function_names = set([res.fname for res in results])

if reference_func not in function_names:
    raise Exception(
        f"Selected reference function '{reference_func}' not found in data! Found {function_names}")




# Step 2: Identify the maximum precision in the reference function.
# Will warn if this is too small.
f_results = [r for r in results if r.fname == reference_func]

# Cases the reference function has been run against.
case_uids = set([r.case.uid for r in f_results])

res_dict = {}
seen_funcs = set()

# Sort the data into a 2d dict for more efficient iteration over later.
print("Sorting results")

for case_uid in case_uids:
    case_results = [r for r in results if r.case.uid == case_uid]
    function_names = set([res.fname for res in case_results])

    res_dict[case_uid] = {}
    for func_name in function_names:
        res_dict[case_uid][func_name] = [r for r in results if
                                         r.fname == func_name and r.case.uid == case_uid]
        seen_funcs.add(func_name)


# Assign a color to each function name, for consistancy across graphs
func_colors = {func: availible_colors.pop() for func in seen_funcs}


print("Creating graphs")
# For each unique case...
for case_uid, v1 in res_dict.items():
    # The max-DOP result for the reference function
    ref_res = max(v1[reference_func], key=lambda r: r.dop)

    ref_y = ref_res.res
    ref_dop = ref_res.dop

    print(f"Creating: {ref_res.case.uid}")
    plt.figure(figsize=(9, 6), dpi=250)

    for func_name, func_results in v1.items():
        color = func_colors[func_name]
        x = [r.dop for r in func_results]
        y = [abs(r.res - ref_y) for r in func_results]
        print(x)
        print(y)
        plt.semilogy(x, y, label=func_name, marker='o', markersize=2, alpha=.7,
                     color=color)
    plt.legend()

    plt.xticks(range(6, ref_dop, 1))
    plt.title(
        f"Magnitude Difference from {reference_func}@{ref_dop}: p={ref_res.case.p}\n"
        f"{ref_res.case}")
    plt.ylabel('magnitude difference')
    plt.xlabel('degree of precision')

    plt.savefig(f"images/{case_uid}_DATA.png", dpi=250)
    plt.clf()
    plt.close()

    plt.figure(figsize=(9, 6), dpi=250)
    for func_name, func_results in v1.items():
        color = func_colors[func_name]
        x = [r.dop for r in func_results]
        t = [r.dt for r in func_results]
        plt.semilogy(x, t, label=func_name, marker='o', markersize=2, alpha=.7,
                     color=color)
    plt.legend()

    plt.xticks(range(6, ref_dop, 1))
    plt.title(
        f"Time for {reference_func}@{ref_res.case}")
    plt.ylabel('Time (s)')
    plt.xlabel('degree of precision')

    plt.savefig(f"images/time/{case_uid}_TIME.png", dpi=250)
    plt.clf()
    plt.close()