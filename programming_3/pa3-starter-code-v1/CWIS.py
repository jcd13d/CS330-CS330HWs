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

    p = [None]*len(intervals)
    for name, start, end, weight in reversed(intervals):
        for name_2, start_2, end_2, weight_2 in reversed(intervals):        # TODO runtime of reversed?
            if end_2 < start:
                p[name] = name_2
                break

    return p


############################

# FINISH THESE METHODS

############################

def find_solution(N, k, intervals):
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

    intervals = sorted(intervals, key=lambda x: x[2])
    for name, start, end, weight in intervals:
        print(name, start, end, weight)

    p = get_p_table(intervals)
    M = [[None]*k for i in range(N)]

    for i in range(k):
        M[0][i] = 0
    for i in range(N):
        M[i][0] = 0

    for i in range(N):
        for j in range(k):
            this_p = p[i] if p[i] is not None else 0
            not_selected = M[i][max(j-1, 0)]
            selected = M[this_p][max(j-1, 0)]
            M[i][j] = max(not_selected, selected)




    schedule =[]
    
    return schedule




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

