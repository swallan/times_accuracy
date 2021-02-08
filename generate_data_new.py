import generators as gens
import argparse
import itertools
import time
import pickle
import os
from Result import Result
from multiprocessing import Pool
import sys
import numpy as np


def dispatcher(process):
    f, case, dop, verbose = process
    err, res, dt = None, -1, -1  # Assign some defaults in case of an error.
    try:
        s = time.time()
        res = f.process(case, dop)
        dt = time.time() - s

        # Process can return tuple in form of (result, time)
        if type(res) is tuple:
            dt = res[1]
            res = res[0]
        result = Result(res, dop=dop, src_case=case, fname=f.display_name,
                        dt=dt,
                        err=err)
    except:
        err = sys.exc_info()[0]
        result = Result(np.nan, dop=dop, src_case=case, fname=f.display_name,
                        dt=dt,
                        err=err)

    if verbose:
        print(result)
    else:
        print('.', end='', flush=True)

    return result


if __name__ == '__main__':
    allStart = time.time()
    dops = range(6, 26)

    # Initialize the parser. Each gen + case can add custom flags in this stage.
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument('--file', help='The output file for data',
                        default="./data.p", required=False)
    parser.add_argument('--pool', "-p", help='Number of pool processes',
                        default=5, type=int, required=False)
    genContainers = [gen.GenContainer for gen in gens.__all__]

    print("Initing arg-parser")
    for gc in genContainers:
        gc.init_parser(parser)

    arg = parser.parse_args()
    print(arg)
    pool_size = arg.pool

    data_file_path = arg.file

    # Pass cmd line args to all generator modules, to allow initialization.
    print("Initing generators")
    for gc in genContainers:
        gc.init_args(arg)

    print("Collecting cases")
    processes = [gen.collect_processes() for gen in genContainers]
    processes = [proc for proc in processes if proc is not None]  # Filter None
    # print(processes)

    # Collapse the passed lists into a 1-d array of operations.
    processes = list(itertools.chain.from_iterable(processes))

    print("Generating processes")

    # Add a process for each DOP, as well as misc. things to pass to dispatcher
    # (mama mia, three dimensions)
    processes = [(*p, dop, arg.verbose)
                 for p in processes
                 for dop in dops]

    print(
        f"Running {len(processes)} cases with a pool of {pool_size} (This will take a while, to say the least)")
    # Multiprocess that shiz

    with Pool(pool_size) as p:
        results = p.map(dispatcher, processes)
    print('', flush=True)

    # Once processing is done, write the results.
    all_results = results
    if os.path.exists(data_file_path):
        print(f"Merging with existing data in {data_file_path}")
        prev_results = pickle.load(open(data_file_path, "rb"))

        new_res_uids = [res.uid for res in results]

        # Only carry previous results if they don't have a uid being
        # overwritten by the new data.
        carried_results = list(filter(lambda r: r.uid not in new_res_uids,
                                      prev_results))

        # Combine the results
        all_results = results + carried_results
        print(
            f"Carried {len(carried_results)}/{len(prev_results)} old results.")

    print(f"Pickling to {data_file_path}")
    pickle.dump(all_results, open(data_file_path, "wb"))

    print(f"Done in {time.time() - allStart} seconds!")

