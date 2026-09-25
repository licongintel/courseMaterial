__kernel void element_add
(
    __global float *x1,
    __global float *x2,
    __global float *y
)
{
    int index = get_global_id(0);
    y[index] = x1[index] + x2[index];
}