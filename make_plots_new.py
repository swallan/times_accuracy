import numpy as np
import pickle
from Result import Result
import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import statistics
from tabulate import tabulate
import math

# Ensure folder existance
if not os.path.exists('images'):
    os.makedirs('images')

if not os.path.exists('stats'):
    os.makedirs('stats')

availible_colors = ['c', 'm', 'y', 'k', 'r', 'g', 'b']

reference_func = "mpgl"
data_file_path = "./data.p"
stats_target_dop = 11

results = pickle.load(open(data_file_path, "rb"))

# Step 1: Identify all present functions
function_names = set([res.fname for res in results])

# Check if reference_func is present in the function names at all.
if reference_func not in function_names:
    raise Exception(
        f"Selected reference function '{reference_func}' not found in data! Found {function_names}")

# Find all cases that the reference function has results for.
# Only these cases will be plotted.
f_results = [r for r in results if r.fname == reference_func]
case_uids = set([r.case.uid for r in f_results])

stats_dict = {}
res_dict = {}
seen_funcs = set()

# Sort the data into a 2d dict for more efficient iteration over later.
# Res_dict is 2d, sorted by case UID then function name.
# Stats_dict is also 2d, sorted by [case_set][func_name]
print("Sorting results")

for case_uid in case_uids:
    case_results = [r for r in results if r.case.uid == case_uid]

    function_names = set([res.fname for res in case_results])

    res_dict.setdefault(case_uid, {})

    for func_name in function_names:
        res_dict[case_uid][func_name] = [r for r in results if
                                         r.fname == func_name and r.case.uid == case_uid]
        seen_funcs.add(func_name)

# Calculate statistics for the results
for case_uid, v1 in res_dict.items():
    for func_name, func_results in v1.items():
        case_set = func_results[0].case.case_set

        stats_dict.setdefault(case_set, {})
        stats_dict[case_set].setdefault(func_name, {})

        func_stat_dict = stats_dict[case_set][func_name]
        func_stat_dict.setdefault("total_err", 0)
        func_stat_dict.setdefault("total_results", 0)
        func_stat_dict.setdefault("mode_arr", [])
        func_stat_dict.setdefault("worst_err", -np.inf)
        func_stat_dict.setdefault("best_err", np.inf)


        # The corrosponding results for this function and case, at the statistics DOP
        stats_res = next(
            filter(lambda r: r.dop == stats_target_dop, func_results), None)

        # The max precision result for this case given by the reference function.
        ref_res = max(v1[reference_func], key=lambda r: r.dop)
        if (stats_res and ref_res) and (not math.isnan(stats_res.res)) and (not stats_res.err):
            err = float(abs(stats_res.res - ref_res.res))
            #print(stats_res.res)
            # These two are used to calculate an average eventually.
            func_stat_dict["total_err"] += err
            func_stat_dict["total_results"] += 1

            # An array of raw error values. Used to calculate the mode.
            func_stat_dict["mode_arr"].append(err)

            # The worst seen error.
            if err > stats_dict[case_set][func_name]["worst_err"]:
                stats_dict[case_set][func_name]["worst_err"] = err

            if err < stats_dict[case_set][func_name]["best_err"]:
                stats_dict[case_set][func_name]["best_err"] = err

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
        plt.semilogy(x, y, label=func_name, marker='o', markersize=2, alpha=.7,
                     color=color)

    plt.legend()

    plt.xticks(range(6, ref_dop, 1))
    plt.title(
        f"Magnitude Difference (relative) from {reference_func}@{ref_dop}\n"
        f"{ref_res.case}")
    plt.ylabel('magnitude difference')
    plt.xlabel('degree of precision')

    try:
        plt.savefig(f"images/{case_uid}_DATA.png", dpi=250)
    except ValueError:
        print(f"Value err creating {case_uid}. The graph will not be made.")
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


print("Writing statistics files")
for case_set, function_stat_dict in stats_dict.items():
    f = open(f"stats/{case_set}.txt", "w")
    f.write(f"============STATS FOR {case_set} @ dop={stats_target_dop}============\n")
    f.write(f"(Note: nan/errored results are not included in these statistics)\n")
    table = []
    for function_name, stats_dict in function_stat_dict.items():
        # Don't write anything if no valid results
        if stats_dict['total_results'] > 0:
            np.seterr(divide='ignore')

            res_tbl = [
                function_name,

                # Average Error
                stats_dict['total_err'] / stats_dict['total_results'],

                # Mode
                statistics.mode(np.round(np.log10(stats_dict["mode_arr"]))),

                # Worst seen error.
                stats_dict['worst_err'],

                # Worst seen error.
                stats_dict['best_err']
            ]
            table.append(res_tbl)
    f.write(tabulate(table, headers=["Function", "Avg. Err", "Mode", "Worst Err", "Best Err"]))
    f.close()
