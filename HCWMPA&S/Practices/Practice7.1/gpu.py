import time
import numpy
import pyopencl

SERIES = 4096
STEPS = 10000000
RECORD_NUM = 256
ORIGINAL = 16

mu_original = numpy.array([0.5, 1.0, 1.368, 1.394, 
                           1.399, 1.4008, 1.40108, 1.4114, 
                           1.5, 1.575, 1.58, 1.626, 
                           1.629, 1.74, 1.76, 1.8],
                           dtype=numpy.float32)

h_x = numpy.zeros(SERIES, dtype=numpy.float32)
h_mu = numpy.tile(mu_original, SERIES // ORIGINAL)
h_records = numpy.zeros((RECORD_NUM, SERIES), dtype=numpy.float32)

platform = pyopencl.get_platforms()[0]
device = platform.get_devices()[0]

ctx = pyopencl.Context([device])
queue = pyopencl.CommandQueue(ctx, device)

with open("kernel.c", "r") as f:
    kernel_src = f.read()
program = pyopencl.Program(ctx, kernel_src).build()

d_x = pyopencl.Buffer(ctx, pyopencl.mem_flags.READ_WRITE | 
                      pyopencl.mem_flags.COPY_HOST_PTR, hostbuf=h_x)
d_mu = pyopencl.Buffer(ctx, pyopencl.mem_flags.READ_ONLY | 
                       pyopencl.mem_flags.COPY_HOST_PTR, hostbuf=h_mu)
d_records = pyopencl.Buffer(ctx, pyopencl.mem_flags.WRITE_ONLY, 
                            h_records.nbytes)

start = time.perf_counter()

program.iterate(queue, (SERIES,), (128,), 
                d_x, d_mu, d_records, numpy.int32(STEPS), 
                numpy.int32(RECORD_NUM), numpy.int32(SERIES))
queue.finish()
elapsed = time.perf_counter() - start
print(f"Elapsed: {elapsed:.3f} seconds")

pyopencl.enqueue_copy(queue, h_records, d_records)

input("Press enter to output the latest records ...")
for i in range(RECORD_NUM):
    group = numpy.random.randint(SERIES // ORIGINAL)
    print(f"{i:3d}: ", end="")
    for j in range(ORIGINAL):
        print(f"{h_records[i, group * ORIGINAL + j]:6.3f} ", end="")
    print()
