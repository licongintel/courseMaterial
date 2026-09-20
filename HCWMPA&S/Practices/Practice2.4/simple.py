import time

steps = 10000000
record_num = 256

mu = [0.5, 1.0, 1.368, 1.394, 
      1.399, 1.4008, 1.40108, 1.4114, 
      1.5, 1.575, 1.58, 1.626, 
      1.629, 1.74, 1.76, 1.8]
x = [0.0] * len(mu)

records = [None] * record_num
for i in range(record_num):
    records[i] = [0] * len(mu)

start = time.perf_counter()

for j in range(len(mu)):
    for _ in range(steps - record_num):
        x[j] = 1 - mu[j] * x[j] * x[j]
    for i in range(record_num):
        x[j] = 1 - mu[j] * x[j] * x[j]
        records[i][j] = x[j]

end = time.perf_counter()

print(f"Elapsed: {end - start:.4f} seconds")
input("Press enter to output the latest records ...")
for i in range(len(records)):
    print(f"{i + 1:3d}: ", end="")
    for j in range(len(records[i])):
        print(f"{records[i][j]: .3f} ", end="")
    print()
