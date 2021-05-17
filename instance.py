"""
    PFSP instance file
"""

from neighbour import get_first_improvement_neighbour, get_random_insert_neighbor, get_rii_insert_neighbor, get_random_exchange_neighbor, get_rii_exchange_neighbor
from initial_solution import get_rz_heuristic, get_random_permutation
import time
import random
import math

TRANSPOSE = "TRANSPOSE"
EXCHANGE = "EXCHANGE"
INSERT = "INSERT"

FIRST_ORDER = [TRANSPOSE, EXCHANGE, INSERT]
SECOND_ORDER = [TRANSPOSE, INSERT, EXCHANGE]


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

    def solve_rii(self, probability, time_limit, srz=True, rtd_file=None):
        """
            Solves the PFSP problem using Randomised Iterative Improvement and returns the solution.

            :param probability: walk probability wp
            :param time_limit: execution time termination criterion
            :param srz: True if the initial solutuon to use is SRZ
            :param rtd_file: name of the file where we want to store data related to the construction of a
                             Qualified Runtime Distribution (optional)
            :return: the solution and the WCT
        """
        # Start counting the time for the termination criterion
        start = time.process_time()
        if srz:
            sol = get_rz_heuristic(self)
        else:
            sol = get_random_permutation(self.nb_jobs)
        best_solution = sol.copy()
        best_wct = self.compute_wct(sol)
        # Write data useful for the QRTD
        if rtd_file:
            output_file = open(rtd_file, "w")
            output_file.write("time,solution\n")
            output_file.write(
                str(time.process_time()-start) + "," + str(best_wct) + "\n")
        # While the termination criterion is not met
        while time.process_time() < start + time_limit:
            r = random.random()
            if r < probability:
                # Pick random neighbor with probability wp
                sol = get_random_insert_neighbor(self, sol)
                wct = self.compute_wct(sol)
            else:
                # Pick first improving neighbor
                wct = self.compute_wct(sol)
                temp_sol, temp_wct = get_rii_exchange_neighbor(
                    self, sol.copy(), wct)
                if temp_sol is not None:
                    sol = temp_sol.copy()
                    wct = temp_wct
            # Keep track of the best solution
            if wct < best_wct:
                best_solution = sol.copy()
                best_wct = wct
                if rtd_file:
                    output_file.write(
                        str(time.process_time()-start) + "," + str(best_wct) + "\n")
        if rtd_file:
            output_file.close()
        return best_solution, best_wct

    def solve_ils(self, gamma, lam, time_limit, rtd_file=None):
        """
            Solves the PFSP problem using Iterated Local Search and returns the solution.

            :param gamma: gamma parameter of the ILS
            :param lam: lambda parameter of the ILS
            :param time_limit: execution time termination criterion
            :param rtd_file: name of the file where we want to store data related to the construction of a
                             Qualified Runtime Distribution (optional)
            :return: the solution and the WCT
        """
        # Start counting the time for the termination criterion
        start = time.process_time()
        # Compute the temperature
        temperature = self.compute_temperature(lam)
        print("Temperature :", temperature)
        # SRZ initial solution
        initial_solution = get_rz_heuristic(self)
        # Local search
        sol, wct = self.solve_vnd(initial_solution, SECOND_ORDER)
        best_sol = sol.copy()
        best_wct = wct
        if rtd_file:
            output_file = open(rtd_file, "w")
            output_file.write("time,solution\n")
            output_file.write(
                str(time.process_time()-start) + "," + str(best_wct) + "\n")
        # While the termination criterion is not met
        while time.process_time() < start + time_limit:
            # Perturbation
            sol_prime = self.perturbation(gamma, sol)
            # Local search
            sol_vnd, wct_vnd = self.solve_vnd(sol_prime.copy(), SECOND_ORDER)
            if wct_vnd < wct:
                sol = sol_vnd.copy()
                wct = wct_vnd
            # Acceptance criterion
                if wct < best_wct:
                    best_sol = sol_vnd.copy()
                    best_wct = wct_vnd
                    if rtd_file:
                        output_file.write(
                            str(time.process_time()-start) + "," + str(best_wct) + "\n")
            elif random.random() < math.exp((wct-wct_vnd)/temperature):
                sol = sol_vnd.copy()
        if rtd_file:
            output_file.close()
        return best_sol, best_wct

    def perturbation(self, gamma, solution):
        """
            Applies a perturbation in the case of the ILS algorithm. It just picks a random job
            and insterts it at a random position in the solution, gamma times.

            :param gamma: gamma parameter of the ILS
            :param solution: actual job ordering
            :return: the modified solution, after applying the perturbation
        """
        for i in range(gamma):
            i, j = random.sample(set(range(len(solution))), 2)
            temp = solution.pop(i)
            solution.insert(j, temp)
        return solution

    def compute_temperature(self, lam):
        """
            Computes the temerature used in the ILS algorithm. 

            :param lam: lambda parameter of the ILS
            :return: the temperature
        """
        return lam*(sum(sum(self.processing_times_matrix[j][i] for i in range(self.nb_machines))*self.priority[j] for j in range(self.nb_jobs))/(10*self.nb_jobs*self.nb_machines))
