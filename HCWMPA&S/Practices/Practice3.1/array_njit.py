import time
import numpy
from numba import njit

@njit(fastmath=True)
def iterate(mu, x, iterations):
    series = len(x)
    for _ in range(iterations):
        for i in range(series):
            x[i] = 1 - mu[i] * x[i] * x[i]
    return x

@njit(fastmath=True)
def iterate_store(mu, x, records, iterations):
    series = len(x)
    for j in range(iterations):
        for i in range(series):
            x[i] = 1 - mu[i] * x[i] * x[i]
            records[j][i] = x[i]
    return x

steps = 10000000
record_num = 256

mu = [0.5, 1.0, 1.368, 1.394, 
      1.399, 1.4008, 1.40108, 1.4114, 
      1.5, 1.575, 1.58, 1.626, 
      1.629, 1.74, 1.76, 1.8]
x = [0.0] * len(mu)
mu = numpy.array(mu, dtype=numpy.float64)
x = numpy.array(x, dtype=numpy.float64)

records = numpy.zeros((record_num, len(mu)))
tmp_x = iterate(mu, x.copy(), 10)
iterate_store(mu, tmp_x, records.copy(), 10)

start = time.perf_counter()

x = iterate(mu, x, steps - record_num)
x = iterate_store(mu, x, records, record_num)

end = time.perf_counter()

print(f"Elapsed: {end - start:.4f} seconds")
input("Press enter to output the latest records ...")
for i in range(len(records)):
    print(f"{i + 1:3d}: ", end="")
    for j in range(len(records[i])):
        print(f"{records[i][j]: .3f} ", end="")
    print()
