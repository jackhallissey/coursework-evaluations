from random import randint
from time import perf_counter

limits = [2, 10, 100, 150, 1000, 5000]

for limit in limits:
    start = perf_counter()

    for n in range(2, limit+1):
        matrix_a = [None] * n
        matrix_b = [None] * n
        for i in range(n):
            matrix_a[i] = [None] * 2
            matrix_b[i] = [None] * 2
            for j in range(2):
                matrix_a[i][j] = randint(1, 10)
                matrix_b[i][j] = randint(1, 10)

        result = [None] * n
        for i in range(n):
            result[i] = [0] * 2

        for i in range(n):
            for j in range(2):
                result[i][j] = (matrix_a[i][0] * matrix_b[0][j] + matrix_a[i][1] * matrix_b[1][j])

    end = perf_counter()

    execution_time = end - start

    print(f"Execution time with n up to {limit}: {execution_time}")

# print(matrix_a)
# print(matrix_b)
# print(result)