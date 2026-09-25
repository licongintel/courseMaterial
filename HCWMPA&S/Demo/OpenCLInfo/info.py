import pyopencl

platform = pyopencl.get_platforms()[0]
device = platform.get_devices()[0]
ctx = pyopencl.Context([device])

print(f"Platform: {platform.name}")
print(f"Device:   {device.name}\n")

with open("kernel.c", "r") as f:
    kernel_src = f.read()

program = pyopencl.Program(ctx, kernel_src).build()
kernel = program.element_add

print(f"Max work-group size:      {device.max_work_group_size}")
print(f"Preferred size multiple:  {kernel.get_work_group_info(pyopencl.kernel_work_group_info.PREFERRED_WORK_GROUP_SIZE_MULTIPLE, device)}")
print(f"Kernel max WG size:       {kernel.get_work_group_info(pyopencl.kernel_work_group_info.WORK_GROUP_SIZE, device)}")
print(f"Local memory:             {device.local_mem_size // 1024} KB")
print(f"Compute units:            {device.max_compute_units}")
