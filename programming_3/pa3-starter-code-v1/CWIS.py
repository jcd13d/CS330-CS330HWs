# Hannah Catabia, catabia@bu.edu
# Solution code for PA2, CS330 Fall 2020
# Adapted from:
# Gavin Brown, grbrown@bu.edu
# CS330 Fall 2019, Programming Exercise Solution 



import sys


############################

# DO NOT CHANGE THIS PART!!

############################

def readInput(input_file):
    with open(input_file, 'r') as f:
        raw = [[float(x) for x in s.split(',')] for s in f.read().splitlines()]
        # number of intervals
        N = int(raw[0][0])
        # max number to schedule
        k =  int(raw[1][0])
        # intervals, with name of interval as an int
        intervals = raw[2:]

        for i in range(len(intervals)):
            intervals[i][0] = int(intervals[i][0])
        return N, k, intervals
    

def writeOutput(schedule, output_file):
    with open(output_file, 'w') as f:
        for i in schedule:
            f.write(str(i) + '\n')


def Run(input_file, output_file):
    N, k, intervals = readInput(input_file)
    schedule = find_solution(N, k, intervals)
    assert all(isinstance(n, int) for n in schedule), "All items in schedule array should be type INT, otherwise the autograder will fail."
    writeOutput(schedule, output_file)


############################

# ADD YOUR OWN METHODS HERE
# (IF YOU'D LIKE)

############################


def get_p_table(intervals):
    """
    P gives the first valid interval to the left if interval i is included
    in the solution

    ASSUMES INTERVALS IS SORTED BY END TIME

    TODO this can be improved - dont need to go through whole list in inner loop
    """

    # p = [None]*(len(intervals) + 1)
    p = {i: None for i in range(len(intervals) + 1)}

    for name, start, end, weight in reversed(intervals):
        for i, (name_2, start_2, end_2, weight_2) in enumerate(reversed(intervals)):        # TODO runtime of reversed?
            if end_2 <= start:
                p[name] = len(intervals) - i
                break
    return p


# def new_get_p(end, start):
#     p = {}
#     assert len(end) == len(start)
#     for i, interval in enumerate(reversed(end)):
#         print(i, interval)
#     return p
#
#
############################

# FINISH THESE METHODS

############################

def find_solution(N, k, intervals, return_weight=False):
    # You are given the following variables:
    # N - the total number of intervals
    # k - the max number of intervals you can put on your schedule
    # intervals - a list of lists
    # ---> Each sublist in intervals has 4 items representing one interval:
    # ---> 0) an INT that is the NAME of the interval
    # ---> 1) a float that is the start time of the interval
    # ---> 2) a float that is the end time of the interval
    # ---> 3) a float that is the weight of an interval

    # return a list called schedule
    # each element in schedule should be 
    # an INT representing the NAME of an interval
    # you would like to place on your schedule

    # M is M[interval, num_allowed]
    """

    Recurrance: M[i, j] = max{ M[i, j-1], M[p(i), j-1] + w_i
                                    |                   |
                                    -> not selected     |
                                                        -> selected

    """

    # Changing indexing to be from 1
    for i, (name, start, end, weight) in enumerate(intervals):
        intervals[i][0] = name + 1

    unsorted = intervals
    intervals = sorted(intervals, key=lambda x: x[2])
    start_time_sort = sorted(intervals, key=lambda x: x[2])
    jobs = [[0]*N for i in range(N + 1)]

    p = get_p_table(intervals)
    # p = new_get_p(intervals, start_time_sort)

    M = [[None]*(k + 1) for i in range(N + 1)]
    taken = [[False]*(k + 1) for i in range(N + 1)]

    for i in range(k + 1):
        M[0][i] = 0
    for i in range(N + 1):
        M[i][0] = 0

    for i, (name, start, end, weight) in enumerate(intervals):
        i = i + 1
        for j in range(1, k + 1):
            this_p = p[name] if p[name] is not None else 0
            not_selected = M[max(i-1, 0)][j]
            selected = M[this_p][max(j-1, 0)] + weight
            M[i][j] = max(not_selected, selected)

            if selected > not_selected:
                taken[i][j] = True
                jobs[i] = jobs[this_p].copy()
                jobs[i][i - 1] = 1
            else:
                jobs[i] = jobs[i-1].copy()

    no_jobs = k
    schedule = []
    current_interval = len(M) - 1
    while no_jobs > 0:
        if taken[current_interval][no_jobs]:
            schedule.append(intervals[current_interval - 1][0] - 1)
            # schedule.append(current_interval)
            no_jobs -= 1
            if p[intervals[current_interval - 1][0]] is None:
                break
            else:
                current_interval = p[intervals[current_interval - 1][0]]
        else:
            current_interval -= 1

    if not return_weight:
        return schedule
    else:
        return schedule, M[-1][-1]




############################################

# CHANGE INPUT FILES FOR DEBUGGING HERE

############################################

def main(args=[]):
    # WHEN YOU SUBMIT TO THE AUTOGRADER, 
    # PLEASE MAKE SURE THE FOLLOWING FUNCTION LOOKS LIKE:
    # Run('input', 'output')
    Run('input', 'output')

if __name__ == "__main__":
    main(sys.argv[1:])    

