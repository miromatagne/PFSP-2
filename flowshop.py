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
from measures import arrange_rii_files, compute_rii_averages, measure_ils, arrange_ils_files, compute_ils_averages, measure_rii_rtd, measure_ils_rtd
import time
import os
import multiprocessing

RII = "RII"
ILS = "ILS"


def parse_args():
    """
        Parses the arguments.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("instance", help="Instance file name")
    parser.add_argument(
        "--rii", help="Randomized Iterative Improvement", action="store_true")
    parser.add_argument(
        "--ils", help="Iterated Local Search", action="store_true")

    args = parser.parse_args()

    if args.rii:
        method = RII
    elif args.ils:
        method = ILS

    return args.instance, method


if __name__ == '__main__':
    instance_name, method = parse_args()
    instance = Instance()
    instance.read_data_from_file(instance_name)
    if method == RII:
        if instance.get_nb_jobs() == 50:
            sol, wct = instance.solve_rii(0.04, 150)
        else:
            sol, wct = instance.solve_rii(0.02, 350)

    else:
        if instance.get_nb_jobs() == 50:
            sol, wct = instance.solve_ils(1, 30, 150)
        else:
            sol, wct = instance.solve_rii(6, 10, 350)

    print("Solution :", sol)
    print("Best WCT : ", wct)
