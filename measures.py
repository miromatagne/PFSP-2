import time
from initial_solution import get_random_permutation, get_rz_heuristic
from instance import Instance
import os

FIRST_IMPROVEMENT = "FIRST_IMPROVEMENT"
BEST_IMPROVEMENT = "BEST_IMPROVEMENT"

TRANSPOSE = "TRANSPOSE"
EXCHANGE = "EXCHANGE"
INSERT = "INSERT"

SRZ = "SRZ"
RANDOM_INIT = "RANDOM_INIT"

FIRST_ORDER = [TRANSPOSE, EXCHANGE, INSERT]
SECOND_ORDER = [TRANSPOSE, INSERT, EXCHANGE]


def measure_rii(i, p, f, time_limit):
    """
        Measures results obtained with Randomized Iterative Improvement and stores them in files.

        :param i: index useful when computing measures several times on the same instance
        :param p: walk probability
        :param f: problem instance name
        :param time_limit: termination criterion
    """
    if "." not in f and f != "Measures":
        output_file = open("../Statistics/Measures/RII/SRZ/Exchange/" + str(p) + "/Raw/" +
                           f + "_" + str(i) + ".txt", "w")
        instance = Instance()
        instance.read_data_from_file(f)
        solution, wct = instance.solve_rii(p, time_limit, srz=True)
        output_file.write(str(wct) + "\n")

        print("Final job permutation : ", solution)
        print("Weighted sum of Completion Times : ", wct)
        output_file.close()
    else:
        print(f)
    return None


def measure_ils(i, gamma, lam, f, time_limit):
    """
        Measures results obtained with Iterated Local Search and stores them in files.

        :param i: index useful when computing measures several times on the same instance
        :param gamma: gamma parameter of the ILS algorithm
        :param lam: lambda parameter of the ILS algorithm
        :param f: problem instance name
        :param time_limit: termination criterion
    """
    if "." not in f and f != "Measures":
        output_file = open("../Statistics/Measures/ILS/" + str(gamma) + "/" + str(lam) + "/Raw/" +
                           f + "_" + str(i) + ".txt", "w")
        instance = Instance()
        instance.read_data_from_file(f)
        solution, wct = instance.solve_ils(gamma, lam, time_limit)
        output_file.write(str(wct) + "\n")

        print("Final job permutation : ", solution)
        print("Weighted sum of Completion Times : ", wct)
        output_file.close()
    else:
        print(f)
    return None


def arrange_rii_files():
    """
        Groups several RII result files together to have better exploitable data for 
        the statistical measures and tests.
    """
    probabilities = [0.1, 0.2, 0.3]
    os.chdir("Statistics/Measures/RII/SRZ/Exchange/0.1/Raw")
    for p in probabilities:
        os.chdir("../../" + str(p) + "/Raw")
        files = os.listdir()
        files.sort()
        result_files = []
        for f in files:
            if "DS" not in f:
                if f[:-6] not in result_files:
                    indiv_file = open(f, "r")
                    indiv_line = indiv_file.readlines()
                    indiv_line = indiv_line[0]
                    res_file = open("../Grouped/" + f[:-6] + ".txt", "w")
                    res_file.write(indiv_line)
                    result_files.append(f[:-6])
                    indiv_file.close()
                    res_file.close()
                else:
                    print(f)
                    indiv_file = open(f, "r")
                    indiv_line = indiv_file.readlines()
                    indiv_line = indiv_line[0]
                    res_file = open("../Grouped/" + f[:-6] + ".txt", "a+")
                    res_file.write(indiv_line)
                    indiv_file.close()
                    res_file.close()


def compute_rii_averages():
    """
        Computes the average execution times of measures done of the RII algorithm.
    """
    probabilities = [0.1, 0.2, 0.3]
    os.chdir("Statistics/Measures/RII/SRZ/Exchange/0.1/Grouped")
    for p in probabilities:
        os.chdir("../../" + str(p))
        average_file = open("average_" + str(p) + ".csv", "w")
        average_file.write("instance,solution\n")
        os.chdir("./Grouped")
        files = os.listdir()
        files.sort()
        result_files = []
        for file_name in files:
            if "DS" not in file_name:
                f = open(file_name, "r")
                lines = f.readlines()
                total = 0
                for line in lines:
                    total += int(line)
                average = total/len(lines)
                average_file.write(file_name[:-4] + "," + str(average) + "\n")
                f.close()
        average_file.close()


def arrange_ils_files():
    """
        Groups several ILS result files together to have better exploitable data for 
        the statistical measures and tests.
    """
    lambdas = [40, 50, 60]
    gammas = [1]
    os.chdir("Statistics/Measures/ILS/3/10/Raw")
    for l in lambdas:
        for g in gammas:
            os.chdir("../../../" + str(g) + "/" + str(l) + "/Raw")
            files = os.listdir()
            files.sort()
            result_files = []
            for f in files:
                if "DS" not in f:
                    if f[:-6] not in result_files:
                        indiv_file = open(f, "r")
                        indiv_line = indiv_file.readlines()
                        indiv_line = indiv_line[0]
                        res_file = open("../Grouped/" + f[:-6] + ".txt", "w")
                        res_file.write(indiv_line)
                        result_files.append(f[:-6])
                        indiv_file.close()
                        res_file.close()
                    else:
                        print(f)
                        indiv_file = open(f, "r")
                        indiv_line = indiv_file.readlines()
                        indiv_line = indiv_line[0]
                        res_file = open("../Grouped/" + f[:-6] + ".txt", "a+")
                        res_file.write(indiv_line)
                        indiv_file.close()
                        res_file.close()


def compute_ils_averages():
    """
        Computes the average execution times of measures done of the ILS algorithm.
    """
    lambdas = [40, 50, 60]
    gammas = [1]
    os.chdir("Statistics/Measures/ILS/1/30/Grouped")
    for l in lambdas:
        for g in gammas:
            os.chdir("../../../" + str(g) + "/" + str(l))
            average_file = open("average_" + str(g) +
                                "_" + str(l) + ".csv", "w")
            average_file.write("instance,solution\n")
            os.chdir("./Grouped")
            files = os.listdir()
            files.sort()
            result_files = []
            for file_name in files:
                if "DS" not in file_name:
                    f = open(file_name, "r")
                    lines = f.readlines()
                    total = 0
                    for line in lines:
                        total += int(line)
                    average = total/len(lines)
                    average_file.write(
                        file_name[:-4] + "," + str(average) + "\n")
                    f.close()
            average_file.close()


def measure_rii_rtd(i, f, p, time_limit):
    """
        Creates the necessary data to establish a QRTD using RII.

        :param i: index useful when computing measures several times on the same instance
        :param p: walk probability
        :param f: problem instance name
        :param time_limit: termination criterion
    """
    instance = Instance()
    instance.read_data_from_file(f)
    solution, wct = instance.solve_rii(
        p, time_limit, srz=True, rtd_file="rtd_rii_" + f[12:] + "_" + str(i) + ".csv")

    print("Final job permutation : ", solution)
    print("Weighted sum of Completion Times : ", wct)


def measure_ils_rtd(i, f, gamma, lam, time_limit):
    """
        Creates the necessary data to establish a QRTD using ILS.

        :param i: index useful when computing measures several times on the same instance
        :param gamma: gamma parameter of the ILS algorithm
        :param lam: lambda parameter of the ILS algorithm
        :param f: problem instance name
        :param time_limit: termination criterion
    """
    instance = Instance()
    instance.read_data_from_file(f)
    solution, wct = instance.solve_ils(
        gamma, lam, time_limit, rtd_file="rtd_ils_" + f[12:] + "_" + str(i) + ".csv")

    print("Final job permutation : ", solution)
    print("Weighted sum of Completion Times : ", wct)
