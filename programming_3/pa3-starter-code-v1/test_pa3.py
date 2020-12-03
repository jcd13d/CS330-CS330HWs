from CWIS import Run, readInput, find_solution, writeOutput
import os
import sys


examples_path = '/Users/justindiemmanuele/Documents/school/MS/CS330/programming_3/student_examples'


def run_example(ex_string):
    example = os.path.join(examples_path, "input_student_example_{0}".format(ex_string))
    print(example)
    schedule, weight = Run(example, 'output')

    print_answer(ex_string, weight)
    get_ans_output(ex_string)
    print(schedule)


def get_ans_output(input):
    answers = os.path.join(examples_path, "output_student_example_{0}".format(input))
    with open(answers, 'r') as f:
        ans = f.read()
    print(ans.split("\n")[0:-1])



def print_answer(input, calc_ans):
    answers = os.path.join(examples_path, "cost_student_example_{0}".format(input))
    with open(answers, 'r') as f:
        ans = f.read()

    print("Answer weight: {0}".format(float(ans)))
    print("Calculated weight: {0}".format(float(calc_ans)))


def Run(input_file, output_file):
    N, k, intervals = readInput(input_file)
    schedule, weight = find_solution(N, k, intervals, return_weight=True, show_plot=False)
    assert all(isinstance(n, int) for n in schedule), "All items in schedule array should be type INT, otherwise the autograder will fail."
    writeOutput(schedule, output_file)
    return schedule, weight



if __name__ == "__main__":
    run_example(sys.argv[1])
