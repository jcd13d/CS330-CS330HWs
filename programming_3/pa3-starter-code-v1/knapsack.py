""" Implementation of dynamic programming algorithm for the knapsack problem.
Written by Adam Smith, 2020.
Tested with Python 3.x

Some sample code you can type in the Python interpreter:
import knapsack
import numpy as np
np.core.arrayprint._line_width = 160 # This makes the printing look better
w = [1,2,5,6,7]
v = [1,6,18,22,28]
capacity = 11
m = knapsack.knapsack_table(v, w, capacity)
solution = knapsack_solution(v, w, capacity, m)
print solution
"""

import numpy as np


def knapsack_table(v, w, capacity):
    n = len(v)  # Assume: len(v) == len(w)
    # initialize array of memoized values
    m = np.empty((n + 1, capacity + 1))
    m.fill(np.inf)
    m[0][:] = 0
    for i in range(n + 1):
        m[i][0] = 0
    w = [0] + w
    v = [0] + v
    for i in range(1, n + 1):
        for k in range(1, capacity + 1):
            if (w[i] > k):
                m[i][k] = m[i - 1][k]
            else:
                m[i][k] = max(v[i] + m[i - 1][k - w[i]], m[i - 1][k])
            print("==================")
            print("m[", i, k, "] is now", m[i][k])
            print(m)
            input("proceed?")
    return m


def knapsack_solution_w_recursion(v, w, capacity, m):
    n = len(v)
    w = [0] + w
    v = [0] + v

    def recursive_knapsack(i, k):
        print("Running recursive knapsack with (i, k) = ", i, k)
        if (i <= 0):
            return []
        elif (w[i] > k):
            return recursive_knapsack(i - 1, k)
        elif (v[i] + m[i - 1][k - w[i]] > m[i - 1][k]):
            solution = recursive_knapsack(i - 1, k - w[i])
            solution.append(i)  # This operation takes constant time
            print("Adding ", i, " to solution")
            return solution
        else:
            return recursive_knapsack(i - 1, k)

    return recursive_knapsack(n, capacity)


def knapsack_solution_no_recursion(v, w, capacity, m):
    n = len(v)
    w = [0] + w
    v = [0] + v

    i = n
    k = capacity

    solution = []
    while i > 0:
        print("Building solution with (i, k) = ", i, k)
        if (w[i] > k):
            i = i - 1
            # k stays the same
        elif (v[i] + m[i - 1][k - w[i]] > m[i - 1][k]):
            solution.append(i)  # This operation takes constant time
            print("Adding ", i, " to solution with weight ", w[i])
            k = k - w[i]
            i = i - 1
        else:
            i = i - 1
            # k stays the same

    return solution


if __name__ == "__main__":

    import knapsack
    import numpy as np
    np.core.arrayprint._line_width = 160 # This makes the printing look better
    w = [1,2,5,6,7]
    v = [1,6,18,22,28]
    capacity = 11
    m = knapsack.knapsack_table(v, w, capacity)
    solution = knapsack_solution_no_recursion(v, w, capacity, m)
    print(solution)
