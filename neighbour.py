"""
    Computes the neighbors used in the PFSP problem solving algorithm, following
    several pivoting rules (FIRST_IMPROVEMENT or BEST_IMPROVEMENT) and several
    neighborhood relations (TRANSPOSE, EXCHANGE or INSERT).
"""

import random

FIRST_IMPROVEMENT = "FIRST_IMPROVEMENT"
BEST_IMPROVEMENT = "BEST_IMPROVEMENT"

TRANSPOSE = "TRANSPOSE"
EXCHANGE = "EXCHANGE"
INSERT = "INSERT"


def get_first_improvement_neighbour(instance, solution, initial_wct, neighbourhood_method):
    """
        Returns the first improving neighbour for a certain neighbourhood method for the
        considered instance and intermediate solution.

        :param instance: instance on which we compute the neighbour
        :param solution: actual solution on which we want to find an improving neighbour
        :param initial_wct: Weighed sum of Completion Time of the actual solution (which we want to improve)
        :param neighbourhood_method: TRANSPOSE, EXCHANGE or INSERT.
        :return: the first improving neighbour, or None if no improving neighbour was found
    """
    # Swap a job with the next one (n total iterations)
    if neighbourhood_method == TRANSPOSE:
        for i in range(len(solution)):
            # The last job is swapped with the first one
            if i == len(solution) - 1:
                solution[0], solution[len(
                    solution)-1] = solution[len(solution)-1], solution[0]
            else:
                solution[i], solution[i+1] = solution[i+1], solution[i]
            wct = instance.compute_wct(solution)
            if wct < initial_wct:
                return solution, wct
            if i != len(solution) - 1:
                solution[i], solution[i+1] = solution[i+1], solution[i]
        return None, initial_wct
    # Exchange a job with any job that is following this job in the job list,
    # to avoid duplicates
    if neighbourhood_method == EXCHANGE:
        for i in range(len(solution)-1):
            for j in range(i+1, len(solution)):
                solution[i], solution[j] = solution[j], solution[i]
                wct = instance.compute_wct(solution)
                if wct < initial_wct:
                    return solution, wct
                solution[i], solution[j] = solution[j], solution[i]
        return None, initial_wct
    # Insert a job at any place in the job list. To avoid popping and inserting too frequently,
    # we insert the job at the first position and then swap it with the next one, and so on...
    if neighbourhood_method == INSERT:
        for i in range(len(solution)):
            temp_sol = solution.copy()
            temp_rem = temp_sol.pop(i)
            temp_sol.insert(0, temp_rem)
            for j in range(len(solution)):
                wct = instance.compute_wct(temp_sol)
                if wct < initial_wct:
                    return temp_sol, wct
                if j != len(solution) - 1:
                    temp_sol[j], temp_sol[j+1] = temp_sol[j+1], temp_sol[j]
        return None, initial_wct


def get_random_insert_neighbor(instance, solution):
    """
        Picks and inserts a job randomly in the actual solution.

        :param instance: problem instance
        :param solution: actual solution (job ordering)
        :return: new job oredering with the random insertion
    """
    i, j = random.sample(set(range(len(solution))), 2)
    temp = solution.pop(i)
    solution.insert(j, temp)
    return solution


def get_random_exchange_neighbor(instance, solution):
    """
        Picks and exchanges 2 jobs randomly in the actual solution.

        :param instance: problem instance
        :param solution: actual solution (job ordering)
        :return: new job oredering with the random exchange
    """
    i, j = random.sample(set(range(len(solution))), 2)
    solution[i], solution[j] = solution[i], solution[j]
    return solution


def get_rii_insert_neighbor(instance, solution, initial_wct):
    """
        Return the first improving neighbour using the Insert neighbourhood rule.
        If no improving neighbour is found, the best one is returned.

        :param instance: problem instance
        :param solution: actual solution (job ordering)
        :param initial_wct: WCT corresponding to the actual solution
        :return: new job oredering and the corresponding WCT
    """
    best_non_improving_sol = None
    best_non_improving_wct = float('inf')
    for i in range(len(solution)):
        temp_sol = solution.copy()
        temp_rem = temp_sol.pop(i)
        temp_sol.insert(0, temp_rem)
        for j in range(len(solution)):
            wct = instance.compute_wct(temp_sol)
            if wct < initial_wct:
                return temp_sol, wct
            elif wct < best_non_improving_wct:
                best_non_improving_sol = temp_sol.copy()
                best_non_improving_wct = wct
            if j != len(solution) - 1:
                temp_sol[j], temp_sol[j+1] = temp_sol[j+1], temp_sol[j]
    return best_non_improving_sol, best_non_improving_wct


def get_rii_exchange_neighbor(instance, solution, initial_wct):
    """
        Return the first improving neighbour using the Exchange neighbourhood rule.
        If no improving neighbour is found, the best one is returned.

        :param instance: problem instance
        :param solution: actual solution (job ordering)
        :param initial_wct: WCT corresponding to the actual solution
        :return: new job oredering and the corresponding WCT
    """
    best_non_improving_sol = None
    best_non_improving_wct = float('inf')
    for i in range(len(solution)-1):
        for j in range(i+1, len(solution)):
            solution[i], solution[j] = solution[j], solution[i]
            wct = instance.compute_wct(solution)
            if wct < initial_wct:
                return solution, wct
            elif wct < best_non_improving_wct:
                best_non_improving_sol = solution.copy()
                best_non_improving_wct = wct
            solution[i], solution[j] = solution[j], solution[i]
    return best_non_improving_sol, best_non_improving_wct
