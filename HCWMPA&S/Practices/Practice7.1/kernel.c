__kernel void iterate
(
    __global float* x,
    __global float* mu,
    __global float* records,
    int steps,
    int record_num,
    int series
)
{
    int index = get_global_id(0);
    float local_x = x[index];
    float local_mu = mu[index];
    for (int i = 0; i < steps - record_num; i++)
    {
        local_x = 1 - local_mu * local_x * local_x;
    }
    for (int i = 0; i < record_num; i++)
    {
        local_x = 1 - local_mu * local_x * local_x;
        records[i * series + index] = local_x;
    }
}

