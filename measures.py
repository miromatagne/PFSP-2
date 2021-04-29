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


def measure_vnd_times():
    """
        Measures the execution times as well as the solutions to the PFSP instance
        by applying Variable Neighbourhood Descend to all instances (with all combinations 
        of initial solutions and neighbourhood orders).
    """
    os.chdir("instances")
    files = os.listdir()
    files.sort()
    files = [files[31]]
    print(files)
    initial_solutions = [RANDOM_INIT, SRZ]
    neighbourhood_orders = [FIRST_ORDER, SECOND_ORDER]
    for f in files:
        if "." not in f and f != "measures":
            output_file = open("./measures/VND/" + f + ".txt", "w")
            instance = Instance()
            instance.read_data_from_file(f)
            for initial_sol_arg in initial_solutions:
                for neighbourhood_order in neighbourhood_orders:
                    start_time = time.time()
                    if initial_sol_arg == RANDOM_INIT:
                        initial_solution = get_random_permutation(
                            instance.get_nb_jobs())
                    else:
                        initial_solution = get_rz_heuristic(instance)
                    print("Initial solution : ", initial_solution)
                    solution, wct = instance.solve_vnd(
                        initial_solution, neighbourhood_order)
                    output_file.write(initial_sol_arg + " " +
                                      "_".join(neighbourhood_order) + " " + str(wct) + " " + str(time.time() - start_time) + "\n")

                    print("Final job permutation : ", solution)
                    print("Weighted sum of Completion Times : ", wct)
                    print("Execution time : %s seconds" %
                          (time.time() - start_time))
            output_file.close()
    return None


def measure_ii_times():
    """
        Measures the execution times as well as the solutions to the PFSP instance
        by applying Iterative Improvement to all instances (with all combinations 
        of initial solutions, pivoting rules and neighbourhood methods).
    """
    os.chdir("instances")
    files = os.listdir()
    files.sort()
    initial_solutions = [RANDOM_INIT, SRZ]
    pivoting_args = [FIRST_IMPROVEMENT, BEST_IMPROVEMENT]
    neighbourhood_args = [TRANSPOSE, EXCHANGE, INSERT]
    for f in files:
        if "." not in f and f != "measures":
            output_file = open("./measures/" + f + ".txt", "w")
            instance = Instance()
            instance.read_data_from_file(f)
            for initial_sol_arg in initial_solutions:
                for pivoting_arg in pivoting_args:
                    for neighbourhood_arg in neighbourhood_args:
                        start_time = time.time()
                        if initial_sol_arg == RANDOM_INIT:
                            initial_solution = get_random_permutation(
                                instance.get_nb_jobs())
                        else:
                            initial_solution = get_rz_heuristic(instance)
                        print("Initial solution : ", initial_solution)
                        solution, wct = instance.solve_ii(
                            initial_solution, pivoting_arg, neighbourhood_arg)
                        output_file.write(initial_sol_arg + " " + pivoting_arg + " " +
                                          neighbourhood_arg + " " + str(wct) + " " + str(time.time() - start_time) + "\n")

                        print("Final job permutation : ", solution)
                        print("Weighted sum of Completion Times : ", wct)
                        print("Execution time : %s seconds" %
                              (time.time() - start_time))
            output_file.close()
    return None


def measure_rii(i, p, f, time_limit):
    """
    """
    if "." not in f and f != "Measures":
        output_file = open("../Statistics/Measures/RII/SRZ/" + str(p) + "/Raw/" +
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


def get_experimental_results_vnd():
    """
        Measure execution times and solutions for all instances, and group the results
        by the combinations used for resolution.
    """
    os.chdir("instances/measures/VND")
    initial_solutions = [RANDOM_INIT, SRZ]
    neighbourhood_orders = [FIRST_ORDER, SECOND_ORDER]
    files = []
    for init in initial_solutions:
        for n in neighbourhood_orders:
            filename = init + "_" + "_".join(n) + ".csv"
            f = open(filename, "w")
            f.write("instance,solution,execution_time" + "\n")
            files.append(f)
    result_files = os.listdir()
    result_files.sort()
    print(result_files)
    for file_name in result_files:
        if ".D" not in file_name and file_name != "measures":
            f = open(file_name)
            lines = f.readlines()
            for i in range(len(lines)):
                line = lines[i].split()
                solution, time = line[2], line[3]
                files[i].write(file_name.split(".")[0] + "," +
                               solution + "," + time + "\n")
            f.close()
    for f in files:
        f.close()


def get_experimental_results_ii():
    """
        Measure execution times and solutions for all instances, and group the results
        by the combinations used for resolution.
    """
    os.chdir("instances/measures")
    initial_solutions = [RANDOM_INIT, SRZ]
    pivoting_args = [FIRST_IMPROVEMENT, BEST_IMPROVEMENT]
    neighbourhood_args = [TRANSPOSE, EXCHANGE, INSERT]
    files = []
    for init in initial_solutions:
        for piv in pivoting_args:
            for n in neighbourhood_args:
                filename = init + "_" + piv + "_" + n + ".csv"
                f = open(filename, "w")
                f.write("instance,solution,execution_time" + "\n")
                files.append(f)
    result_files = os.listdir()
    result_files.sort()
    print(result_files)
    for file_name in result_files:
        if ".D" not in file_name and file_name != "measures":
            f = open(file_name)
            lines = f.readlines()
            for i in range(len(lines)):
                line = lines[i].split()
                solution, time = line[3], line[4]
                files[i].write(file_name.split(".")[0] + "," +
                               solution + "," + time + "\n")
            f.close()
    for f in files:
        f.close()


def arrange_rii_files():
    probabilities = [0.02, 0.04, 0.06, 0.08]
    os.chdir("Statistics/Measures/RII/SRZ/0.1/Raw")
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
    probabilities = [0.02, 0.04, 0.06, 0.08]
    os.chdir("Statistics/Measures/RII/SRZ/0.1/Grouped")
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

    def measure_rii_rtd(f, p, time_limit):
        instance = Instance()
        instance.read_data_from_file(f)
        solution, wct = instance.solve_rii(p, time_limit, srz=True)

        print("Final job permutation : ", solution)
        print("Weighted sum of Completion Times : ", wct)
