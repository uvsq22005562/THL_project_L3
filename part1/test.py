from random import randint
from time import perf_counter

def cmat(n):
    mat = []
    for i in range(n):
        ligne = []
        for j in range(n):
            ligne.append(randint(0, 20))
        mat.append(ligne)
    return mat


def multiply(m1, m2):
    n = len(m1)
    res = [[0 for _ in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                res[i][j] += m1[i][k] * m2[k][j]
    return res



m1 = cmat(1000)
m2 = cmat(1000)
start = perf_counter()
multiply(m1, m2)
stop = perf_counter()
print(stop - start)