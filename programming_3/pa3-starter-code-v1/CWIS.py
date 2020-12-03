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


############################

# FINISH THESE METHODS

############################

def find_solution(N, k, intervals, show_plot=False, return_weight=False):
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

    TODO: does matrix need to be N+1 by K+1? and then index intervals from 1?

    """

    def print_mat(m):
        for i in m:
            print(i)

    # Changing indexing to be from 1
    for i, (name, start, end, weight) in enumerate(intervals):
        intervals[i][0] = name + 1

    intervals = sorted(intervals, key=lambda x: x[2])
    jobs = [[0]*N for i in range(N + 1)]
    # print(jobs)

    # import matplotlib.pyplot as plt
    # y = 0
    # for i, (name, start, end, weight) in enumerate(intervals):
    #     # print(name, start, end, weight)
    #     plt.hlines(y, xmin=start, xmax=end)
    #     plt.text((start+end)/2+5, y + 0.3, weight)
    #     plt.text((start+end)/2, y + 0.3, str(name - 1) + ")")
    #     y+=1
    # plt.grid()

    p = get_p_table(intervals)

    # for key, v in p.items():
    #     print("name: {0}, index: {1}".format(key, v))


    M = [[None]*(k + 1) for i in range(N + 1)]
    taken = [[False]*(k + 1) for i in range(N + 1)]

    for i in range(k + 1):
        M[0][i] = 0
    for i in range(N + 1):
        M[i][0] = 0


    # for i in range(1, N + 1):
    for i, (name, start, end, weight) in enumerate(intervals):
        # print(i, name, start, end, weight)
        i = i + 1
        for j in range(1, k + 1):
            this_p = p[name] if p[name] is not None else 0
            # print(this_p)
            # print(p)
            # print("i: {0}".format(i))
            not_selected = M[max(i-1, 0)][j]
            selected = M[this_p][max(j-1, 0)] + weight
            # print("i: {0}, j: {1}, select = {2}, nselect = {3}, this_p = {4}".format(i, j, selected, not_selected, this_p))
            # print(p)
            M[i][j] = max(not_selected, selected)

            # TODO this isnt working but idea is when we select it should be whatever p set is plus current selection
            if selected > not_selected:
                taken[i][j] = True
                jobs[i] = jobs[this_p].copy()
                jobs[i][i - 1] = 1
            else:
                jobs[i] = jobs[i-1].copy()

    """
    not working because i am only storing j=k solution at each step!!!
    how do I backtrace?!
    """

    # print_mat(M)
    # print_mat(jobs)
    # print_mat(taken)
    # print(p)

    # schedule = [i for i, e in enumerate(jobs[-1]) if e != 0][-k:]

    # print(schedule)
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

    # print(schedule)


    # real_schedule = []
    # for index in schedule:
    #     real_schedule.append(intervals[index][0] - 1)

    # for i, v in enumerate(intervals):
    #     print(i, v[0] - 1)
    # print(p)

    # print(real_schedule)
    # schedule = real_schedule

    # print(k)
    if show_plot:
        plt.show()

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

