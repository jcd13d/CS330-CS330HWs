import random
import numpy as np

random.seed(0)

# cant use n and k right away
k = 4
len_A = 15
A = []

for i in range(len_A):
    A.append(random.randint(1, k))

def floors(x):

    max_floor = 0
    for i in range(len(x)):
        if x[i] > max_floor:
            max_floor = x[i]

    flrs = [None]*max_floor
    for i in range(max_floor):
        flrs[i] = []

    for j in range(len(x)):
        flrs[x[j] - 1].append(j)

    return flrs


def floors_hash(x):

    # they use len() in their psuedocode so we should be able to...
    # but is that O(1) or O(n)?

    # Init "linked lists" in "hash table"
    # This iterates through every student when they are repeated... bad
    # runtime n? or n^2 becuase indexing into hash table?
    flrs = {}
    for i in range(len(x)):
        flrs[x[i]] = []

    # append to linked list in hash table index of each student in that group
    # insert is O[n] in hash table - n^2
    for j in range(len(x)):
        flrs[x[j]].append(j)

    return flrs


def assign_students(x):
    n = len(x)

    flrs = floors_hash(x)
    print(flrs)

    # finding max students on 1 floor - this is worst case runtime n
    # n if all students are on different floors
    max_students_per_floor = 0
    for k, v in flrs.items():
        if len(flrs[k]) > max_students_per_floor:
            max_students_per_floor = len(flrs[k])

    # Initialize array
    groups = {}
    for group in range(max_students_per_floor):
        groups[group] = []

    count = 0
    for k, v in flrs.items():
        for student in v:
            groups[count % max_students_per_floor].append(student)
            count += 1

    return groups

# in class - store inverse of list for easy lookup!


print("Floor ids: {0}".format(A))

print(floors_hash(A))

print(assign_students(A))
