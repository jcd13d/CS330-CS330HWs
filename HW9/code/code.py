import math

calls = 0
calls_memo = 0


def recursive_moves(board, L, n):
    if L == n - 1:
        return 0
    else:
        min_so_far = math.inf
        for i in range(L + 1, min(L + board[L] + 1, n)):
            global calls
            calls += 1
            moves = recursive_moves(board, i, n)
            if moves + 1 < min_so_far:
                min_so_far = moves + 1
    return min_so_far


def rec_move_dy(board, L, n):
    OPT = [math.inf]*n

    for i in range(n - 1, -1, -1):
        if i == n - 1:
            OPT[i] = 0
        else:
            print(OPT)
            OPT[i] = min(OPT[i: min(i + board[i] + 1, n)]) + 1

    return OPT


def recursive_moves_memo(board, L, n, memo=None):
    if memo is None:
        memo = [None]*n

    if memo[L] is not None:
        print(memo[L])
        return memo[L]

    if L == n - 1:
        return 0
    else:
        min_so_far = math.inf
        for i in range(L + 1, min(L + board[L] + 1, n)):
            global calls_memo
            calls_memo+=1
            moves = recursive_moves_memo(board, i, n, memo)
            if moves + 1 < min_so_far:
                min_so_far = moves + 1

    memo[L] = min_so_far
    return min_so_far



if __name__ == "__main__":
    array = [1, 3, 6, 3, 2, 3, 9, 5]
    n = len(array)
    # result = recursive_moves(array, 0, n)
    # for i in range(0, n):
        # print(recursive_moves(array, i, n))

    print("\n\n")
    result2 = rec_move_dy(array, 0, n)
    print(result2)

    print("\n\n")
    print("memo")
    result3 = recursive_moves_memo(array, 0, n)
    print(result3)

    print("\n\n")
    result = recursive_moves(array, 0, n)
    print(result)

    print("\n\n")
    print(calls)
    print(calls_memo)


