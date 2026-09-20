import time

steps = 10000000
record_num = 256

mu = 0.5
x = 0.0

records = [0] * record_num

start = time.perf_counter()
for i in range(steps - record_num):
    x = 1 - mu * x * x
for i in range(record_num):
    x = 1 - mu * x * x
    records[i] = x
end = time.perf_counter()

print(f"Elapsed: {end - start:.4f} seconds")
input("Press enter to output the latest records ...")
for i in range(len(records)):
    print(f"{i + 1:3d}: {records[i]: .3f}")
