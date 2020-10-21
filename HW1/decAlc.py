
A = [4, 3, 2, 5, 1]

def decAlg(x):
    dec = 0
    n = len(x)
    for i in range(1, n+1):       # what I think is correct version - affirmed
        j = i - 1
        while (j > 0) and x[j - 1] > x[j]:
            temp = x[j - 1]
            x[j - 1] = x[j]
            x[j] = temp
            j = j - 1
            dec = dec + 1
    return x, dec


def swapAlg(x):
    n = len(x)
    swaps = 0
    for i in range(n):
        for j in range(n - i - 1):
            # print("i ", i, " j ", j)
            if x[j] > x[j + 1]:
                x[j] = x[j] + x[j + 1]
                x[j + 1] = x[j] - x[j + 1]
                x[j] = x[j] - x[j + 1]
                swaps = swaps + 1
    return x, swaps


def CountAlg(x):
    n = len(x)
    count = 0
    for i in range(n):
        j_init = i + 1
        for j in range(j_init, n):
            if i < j and x[i] > x[j]:
                count += 1
    return count


def bubsort(x):
    n = len(x)
    for i in range(n):
        j_init = i + 1
        for j in range(j_init, n):
            print(i, " ", j)
            if x[i] > x[j]:
                tmp = x[i]
                x[i] = x[j]
                x[j] = tmp
        print(x)
    return x



print("orig A: {0}".format(A))

dec_A, dec = decAlg(A.copy())
swap_A, swaps = swapAlg(A.copy())

print("dec A: {0}".format(dec_A))
print("decs: {0}".format(dec))

print("swap A: {0}".format(swap_A))
print("swaps: {0}".format(swaps))

print("CountAlg: {0}".format(CountAlg(A.copy())))

print("bubsort: {0}".format(bubsort(A.copy())))

