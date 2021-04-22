"""
    PFSP instance file
"""

from neighbour import get_best_improvement_neighbour, get_first_improvement_neighbour, get_random_insert_neighbor, get_rii_insert_neighbor
from initial_solution import get_rz_heuristic, get_random_permutation
import time
import random

FIRST_IMPROVEMENT = "FIRST_IMPROVEMENT"
BEST_IMPROVEMENT = "BEST_IMPROVEMENT"

TRANSPOSE = "TRANSPOSE"
EXCHANGE = "EXCHANGE"
INSERT = "INSERT"

FIRST_ORDER = [TRANSPOSE, EXCHANGE, INSERT]
SECOND_ORDER = [TRANSPOSE, INSERT, EXCHANGE]


INSERT = "INSERT"


class Instance:
    """
        Class describing an instance of the PFSP problem.
    """

    def __init__(self):
        self.nb_jobs = 0
        self.nb_machines = 0
        self.processing_times_matrix = []
        self.due_dates = []
        self.priority = []

    def read_data_from_file(self, filename):
        """
            Reads data from a PFSP instance file and stores the content.

            :param filename: name of the instance file
        """
        try:
            with open(filename, "r") as f:
                print("File " + filename + " is now open, start to read...")
                self.nb_jobs, self.nb_machines = tuple(
                    map(int, f.readline().split(" ")))
                print("Number of jobs : " + str(self.nb_jobs))
                print("Number of machines  : " + str(self.nb_machines))
                print("Start to read matrix...")
                for i in range(self.nb_jobs):
                    line = f.readline().strip().split(" ")
                    line = list(map(int, line))
                    self.processing_times_matrix.append(line[1::2])
                f.readline()
                for i in range(self.nb_jobs):
                    line = f.readline().split(" ")
                    self.due_dates.append(int(line[1]))
                    self.priority.append(int(line[-1]))
            return True
        except OSError as e:
            print("Error while opening" + filename)
            return False

    def compute_wct(self, sol):
        """
            Computes the Weighed sum of Completion Times (WCT) for a given solution (ordering of jobs).

            :param sol: job ordering on which the WCT is computed
        """
        previous_machine_end_time = [0 for i in range(len(sol))]

        # First machine
        for j in range(len(sol)):
            job_number = sol[j]
            previous_machine_end_time[j] = previous_machine_end_time[j -
                                                                     1] + self.processing_times_matrix[job_number][0]
        # Following machines
        for m in range(1, self.nb_machines):
            previous_machine_end_time[0] += self.processing_times_matrix[sol[0]][m]
            previous_job_end_time = previous_machine_end_time[0]
            for j in range(1, len(sol)):
                job_number = sol[j]
                previous_machine_end_time[j] = max(
                    previous_job_end_time, previous_machine_end_time[j]) + self.processing_times_matrix[job_number][m]
                previous_job_end_time = previous_machine_end_time[j]
        wct = 0
        for j in range(len(sol)):
            wct += previous_machine_end_time[j] * self.priority[sol[j]]
        return wct

    def get_nb_jobs(self):
        return self.nb_jobs

    def get_weighed_sum(self):
        """
            Computes the weighed sum used for the SRZ Heuristic initial solution.
        """
        weights = {}
        for i in range(self.nb_jobs):
            total_processing_time = sum(self.processing_times_matrix[i])
            weights[i] = total_processing_time / self.priority[i]
        sorted_weighed_sum = dict(
            sorted(weights.items(), key=lambda item: item[1]))
        return sorted_weighed_sum.keys()

    def solve_ii(self, solution, pivoting_rule, neighbourhood_method):
        """
            Solves the PSFP problem using Iterative Improvement and returns the solution.

            :param solution: initial solution used to start the algorithm
            :param pivoting_rule: pivoting rule used during the algorithm (LEAST_IMPROVEMENT or BEST_IMPORVEMENT)
            :param neighborhood_rule: neighborhood rule used during the algorithm (EXCHANGE, TRASPOSE or INSERT)
            :return: the solution and the associated WCT
        """
        initial_wct = self.compute_wct(solution)
        if pivoting_rule == FIRST_IMPROVEMENT:
            sol, wct = solution, initial_wct
            while True:
                temp_sol, temp_wct = get_first_improvement_neighbour(
                    self, sol, wct, neighbourhood_method)
                if not temp_sol:
                    if wct == 0:
                        wct = temp_wct
                    return sol, wct
                sol, wct = temp_sol, temp_wct
        else:
            sol, wct = solution, initial_wct
            while True:
                temp_sol, temp_wct = get_best_improvement_neighbour(
                    self, sol, wct, neighbourhood_method)
                if not temp_sol:
                    if wct == 0:
                        wct = temp_wct
                    return sol, wct
                sol, wct = temp_sol, temp_wct

    def solve_vnd(self, solution, neighbourhood_order):
        """
            Solves the PSFP problem using Variable Neighborhood Descent and returns the solution.

            :param solution: initial solution used to start the algorithm
            :param neighborhood_order: neighborhood order used during the algorithm (FIRST_ORDER or SECOND_ORDER)
            :return: the solution and the associated WCT
        """
        k = 3
        i = 0
        sol = solution.copy()
        wct = self.compute_wct(solution)
        while k > i:
            temp_sol, temp_wct = get_first_improvement_neighbour(
                self, sol.copy(), wct, neighbourhood_order[i])
            if not temp_sol:
                i = i + 1
            else:
                sol = temp_sol.copy()
                wct = temp_wct
                i = 0
        return sol, wct

    def solve_rii(self, probability, time_limit):
        """
            Solves the PFSP problem using Randomised Iterative Improvement and returns the solution.

            :param solution: initial solution used to start the algorithm
            :return: the solution and the WCT
        """
        start = time.process_time()
        sol = get_random_permutation(self.nb_jobs)
        best_solution = sol.copy()
        best_wct = self.compute_wct(sol)
        random_count = 0
        non_random_count = 0
        while time.process_time() < start + time_limit:
            r = random.random()
            if r < probability:
                #random_count += 1
                # Pick random neighbor
                sol = get_random_insert_neighbor(self, sol)
                wct = self.compute_wct(sol)
            else:
                #non_random_count += 1
                # Pick first improving neighbor
                wct = self.compute_wct(sol)
                temp_sol, temp_wct = get_rii_insert_neighbor(
                    self, sol.copy(), wct)
                if temp_sol is not None:
                    sol = temp_sol.copy()
                    wct = temp_wct
            if wct < best_wct:
                # print(best_wct)
                best_solution = sol.copy()
                best_wct = wct

        #print("Random:", random_count)
        #print("Non random:", non_random_count)
        return best_solution, best_wct

    def solve_ils(self, time_limit):
        start = time.process_time()
        # Initial solution
        initial_solution = get_rz_heuristic(self)
        print(initial_solution)
        # Local search
        sol, wct = self.solve_vnd(initial_solution, SECOND_ORDER)
        best_sol = sol.copy()
        best_wct = wct

        while time.process_time() < start + time_limit:
            # Perturbation
            sol = self.perturbation(3, sol)
            # Local search
            sol, wct = self.solve_vnd(sol.copy(), SECOND_ORDER)
            # Accept criterion
            if self.accept(sol, wct, best_sol, best_wct):
                best_sol = sol.copy()
                best_wct = wct

        return best_sol, best_wct

    def perturbation(self, gamma, solution):
        for i in range(gamma):
            i, j = random.sample(set(range(len(solution))), 2)
            temp = solution.pop(i)
            solution.insert(j, temp)
        return solution

    def accept(self, sol, wct, best_sol, best_wct):
        if wct < best_wct:
            return True
        return False
