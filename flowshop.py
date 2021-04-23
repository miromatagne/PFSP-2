"""
    Main file

    Usage : python flowshop.py instance [options]

    Options :   --vnd for Variable Neighbourhood Descent (Iterative Improvement by default)
                --first or --best for First or best improvement pivoting rule
                --transpose --exchange or --insert for the neighbourhood rule
                --random-init or --srz for the initial solution
                --tei or --tie for the neighbourhood order (VND)

"""

import sys
import random
import argparse
from instance import Instance
from initial_solution import get_random_permutation, get_rz_heuristic
from measures import measure_vnd_times, measure_ii_times, get_experimental_results_vnd, measure_rii, arrange_rii_files
import time
import os
import multiprocessing

FIRST_IMPROVEMENT = "FIRST_IMPROVEMENT"
BEST_IMPROVEMENT = "BEST_IMPROVEMENT"

TRANSPOSE = "TRANSPOSE"
EXCHANGE = "EXCHANGE"
INSERT = "INSERT"

SRZ = "SRZ"
RANDOM_INIT = "RANDOM_INIT"

FIRST_ORDER = [TRANSPOSE, EXCHANGE, INSERT]
SECOND_ORDER = [TRANSPOSE, INSERT, EXCHANGE]


def parse_args():
    """
        Parses the arguments.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("instance", help="Instance file name")
    parser.add_argument("--measure", help="Measure mode", action="store_true")
    parser.add_argument(
        "--vnd", help="Variable Neighbourhood Descend", action="store_true")
    pivoting_group = parser.add_mutually_exclusive_group()
    pivoting_group.add_argument(
        "--first", help="first-improvement pivoting rule", action="store_true")
    pivoting_group.add_argument(
        "--best", help="best-improvement pivoting rule", action="store_true")
    neighbourhood_group = parser.add_mutually_exclusive_group()
    neighbourhood_group.add_argument(
        "--transpose", help="transpose neighborhood", action="store_true")
    neighbourhood_group.add_argument(
        "--exchange", help="exchange neighborhood", action="store_true")
    neighbourhood_group.add_argument(
        "--insert", help="instert neighborhood", action="store_true")
    initial_solution_group = parser.add_mutually_exclusive_group()
    initial_solution_group.add_argument(
        "--random-init", help="randomly generated initial solution", action="store_true")
    initial_solution_group.add_argument(
        "--srz", help="simplified RZ heuristic initial solution", action="store_true")
    neighbourhood_order_group = parser.add_mutually_exclusive_group()
    neighbourhood_order_group.add_argument(
        "--tei", help="transpose, exchange, insert neighborhood order", action="store_true")
    neighbourhood_order_group.add_argument(
        "--tie", help="transpose, insert, exchange neighborhood order", action="store_true")

    args = parser.parse_args()

    pivoting = FIRST_IMPROVEMENT
    neighbourhood = TRANSPOSE
    initial_solution = RANDOM_INIT
    if args.best:
        pivoting = BEST_IMPROVEMENT
    if args.exchange:
        neighbourhood = EXCHANGE
    elif args.insert:
        neighbourhood = INSERT
    if args.srz:
        initial_solution = SRZ
    if args.tei:
        neighbourhood_order = FIRST_ORDER
    elif args.tie:
        neighbourhood_order = SECOND_ORDER
    else:
        neighbourhood_order = FIRST_ORDER

    return args.vnd, args.instance, pivoting, neighbourhood, initial_solution, args.measure, neighbourhood_order


if __name__ == '__main__':
    # vnd, filename, pivoting_arg, neighbourhood_arg, initial_solution_arg, measure, neighbourhood_order = parse_args()
    # if measure:
    #     if vnd:
    #         measure_vnd_times()
    #     else:
    #         measure_ii_times()
    # else:
    #     instance = Instance()
    #     instance.read_data_from_file(filename)
    #     if initial_solution_arg == RANDOM_INIT:
    #         initial_solution = get_random_permutation(instance.get_nb_jobs())
    #     else:
    #         initial_solution = get_rz_heuristic(instance)
    #     print("Initial solution : ", initial_solution)
    #     start_time = time.time()

    #     if vnd:
    #         solution, wct = instance.solve_vnd(
    #             initial_solution, neighbourhood_order)
    #     else:
    #         solution, wct = instance.solve_ii(
    #             initial_solution, pivoting_arg, neighbourhood_arg)
    #     print("Final job permutation : ", solution)
    #     print("Weighted sum of Completion Times : ", wct)
    #     print("Execution time : %s seconds" % (time.time() - start_time))
    # arrange_rii_files()

    # instance = Instance()
    # instance.read_data_from_file("./instances/100_20_01")
    #a = instance.compute_temperature(4)
    # print(a)
    #sol, wct = instance.solve_ils(200, 4, 20)
    # print(wct)
    #initial_solution = get_random_permutation(instance)
    #sol, wct = instance.solve_rii(0.2, 20)

    # print(wct)

    t = time.time()
    os.chdir("instances")
    files = os.listdir()
    files.sort()
    probabilities = [0.1, 0.2, 0.3, 0.4, 0.5]
    for f in files:
        processes = []
        if "." not in f and f != "measures" and "100" in f:
            for proba in probabilities:
                for i in range(5):
                    p = multiprocessing.Process(
                        target=measure_rii, args=(i, proba, f, 350,))
                    processes.append(p)
                    p.start()
        if "." not in f and f != "measures" and "50" in f:
            for proba in probabilities:
                for i in range(5):
                    p = multiprocessing.Process(
                        target=measure_rii, args=(i, proba, f, 150,))
                    processes.append(p)
                    p.start()

        for process in processes:
            process.join()

    # arrange_rii_files()

    # instance = Instance()
    # instance.read_data_from_file("./instances/50_20_01")
    # initial_solution = get_random_permutation(instance.get_nb_jobs())
    # print("Initial solution : ", initial_solution)
    # solution, wct = instance.solve_rii(initial_solution, 0.2, 10)
    # print(wct)

    print(time.time() - t)
