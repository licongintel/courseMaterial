import time
import numpy
import pyopencl
from data import read_data

WARM_UP_FILES = ["../data/usps.t.txt", "../data/usps.t.txt"]
TEST_FILES = ["../data/usps.t.txt", "../data/usps.t.1.txt",
              "../data/usps.t.2.txt", "../data/usps.t.3.txt",
              "../data/usps.t.4.txt", "../data/usps.t.5.txt"]

platform = pyopencl.get_platforms()[0]
device = platform.get_devices()[0]
ctx = pyopencl.Context(devices=[device])
queue = pyopencl.CommandQueue(ctx)

with open("kernel.c", "r") as f:
    kernel_src = f.read()
program = pyopencl.Program(ctx, kernel_src).build()

kernel = program.classify

training_data = read_data("../data/usps.txt")
training_x = numpy.ascontiguousarray(training_data.x.reshape(-1), 
        dtype=numpy.float32)
training_y = numpy.ascontiguousarray(training_data.y, 
        dtype=numpy.int32)

d_training_x = pyopencl.Buffer(ctx, pyopencl.mem_flags.READ_ONLY | 
        pyopencl.mem_flags.COPY_HOST_PTR, hostbuf=training_x)
d_training_y = pyopencl.Buffer(ctx, pyopencl.mem_flags.READ_ONLY | 
        pyopencl.mem_flags.COPY_HOST_PTR, hostbuf=training_y)

for k in range(2):
    files = WARM_UP_FILES if k == 0 else TEST_FILES

    test_datas = []
    host_outs = []

    starts = []
    mids = []
    ends = []

    total_start = time.perf_counter()
    for i in range(len(files)):

        starts.append(time.perf_counter())
        test_data = read_data(files[i])
        test_datas.append(test_data)
        host_outs.append(numpy.empty(test_datas[i].total, 
                dtype=numpy.int32))
        test_x = numpy.ascontiguousarray(test_data.x.reshape(-1), 
                dtype=numpy.float32)

        if k == 0 and i == 0:
            d_test_x = pyopencl.Buffer(ctx, 
                    pyopencl.mem_flags.READ_ONLY, test_x.nbytes)
            d_out = pyopencl.Buffer(ctx, pyopencl.mem_flags.WRITE_ONLY, 
                    host_outs[i].nbytes)

        mids.append(time.perf_counter())

        pyopencl.enqueue_copy(queue, d_test_x, test_x)

        LOCAL_SZ = 128
        global_size = (test_datas[i].total + LOCAL_SZ - 1) // \
                LOCAL_SZ * LOCAL_SZ
        kernel(queue, (global_size,), (LOCAL_SZ,), d_training_x, 
                d_training_y, d_test_x, d_out, 
                numpy.int32(training_data.total), 
                numpy.int32(test_data.total))

        pyopencl.enqueue_copy(queue, host_outs[i], d_out, 
                is_blocking=True)

        ends.append(time.perf_counter())

    total_end = time.perf_counter()

    if k == 0:
        print("Warm-up completed")
        continue

    for i in range(len(files)):
        print(f"Preparation time: {mids[i] - starts[i]:.4f}s")
        print(f"Execution time: {ends[i] - mids[i]:.4f}s")

    print(f"Total time: {total_end - total_start:.4f}s")

    for i in range(len(files)):
        correct = 0
        for j in range(test_datas[i].total):
            if host_outs[i][j] == test_datas[i].y[j]:
                correct += 1
        accuracy = correct / test_datas[i].total
        print(f"{correct} / {test_datas[i].total} = {accuracy}")
