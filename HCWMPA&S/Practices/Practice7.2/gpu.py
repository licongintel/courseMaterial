import time
import numpy
import pyopencl
from data import read_data

training_data = read_data("../data/usps.txt")
test_data = read_data("../data/usps.t.txt")

training_x = numpy.ascontiguousarray(training_data.x.reshape(-1), 
        dtype=numpy.float32)
training_y = numpy.ascontiguousarray(training_data.y, 
        dtype=numpy.int32)
test_x = numpy.ascontiguousarray(test_data.x.reshape(-1), 
        dtype=numpy.float32)
out_labels = numpy.empty(test_data.total, dtype=numpy.int32)

platform = pyopencl.get_platforms()[0]
device = platform.get_devices()[0]
ctx = pyopencl.Context(devices=[device])
queue = pyopencl.CommandQueue(ctx, device)

with open("kernel.c", "r") as f:
    kernel_src = f.read()
program = pyopencl.Program(ctx, kernel_src).build()

d_training_x = pyopencl.Buffer(ctx, pyopencl.mem_flags.READ_ONLY | 
        pyopencl.mem_flags.COPY_HOST_PTR, hostbuf=training_x)
d_training_y = pyopencl.Buffer(ctx, pyopencl.mem_flags.READ_ONLY | 
        pyopencl.mem_flags.COPY_HOST_PTR, hostbuf=training_y)
d_test_x = pyopencl.Buffer(ctx, pyopencl.mem_flags.READ_ONLY | 
        pyopencl.mem_flags.COPY_HOST_PTR, hostbuf=test_x)
d_out = pyopencl.Buffer(ctx, pyopencl.mem_flags.WRITE_ONLY, 
        out_labels.nbytes)

LOCAL_SZ = 128
global_size = (test_data.total + LOCAL_SZ - 1) // LOCAL_SZ * LOCAL_SZ

start = time.perf_counter()
program.classify(queue, (global_size,), (LOCAL_SZ,),
        d_training_x, d_training_y, d_test_x, d_out, 
        numpy.int32(training_data.total), numpy.int32(test_data.total))
queue.finish()
end = time.perf_counter()
print(f"Elapsed: {end - start:.4f} seconds")

pyopencl.enqueue_copy(queue, out_labels, d_out).wait()
correct = 0
for i in range(test_data.total):
    if out_labels[i] == test_data.y[i]:
        correct += 1
print(f"{correct} / {test_data.total} = {correct / test_data.total}")

