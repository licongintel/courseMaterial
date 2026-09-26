
#define DIMS     256

/* training vectors per local tile   */
/* tune: 8-32 depending on iGPU     */

#define TILE     16      

#define LOCAL_SZ 128

__kernel __attribute__((reqd_work_group_size(LOCAL_SZ, 1, 1))) 
        void classify
(
    __global const float* restrict training_x,                  /* [n_train x DIMS] */
    __global const int*   restrict training_y,                  /* [n_train]        */
    __global const float* restrict test_x,                      /* [n_test  x DIMS] */
    __global       int*            out_labels,                  /* [n_test]         */
    const int n_train,
    const int n_test
)
{
    const int gid = get_global_id(0);   /* 0 ... n_test rounded w/ LOCAL_SZ     */
    const int lid = get_local_id(0);    /* 0 ... LOCAL_SZ                       */

    /* ---- cache this work-item's test vector in __private ---- */
    float q[DIMS];
    if (gid < n_test) 
    {
        for (int d = 0; d < DIMS; d++)
            q[d] = test_x[gid * DIMS + d];
    }

    float min_dist  = FLT_MAX;
    int   best      = -1;

    /* ---- local tile: holds TILE training vectors ---------- */
    __local float ltrain[TILE][DIMS];   /* 16 x 256 x 4 = 16 KB */

    /* ---- stream training data in tiles ---------------------- */
    for (int tile_start = 0; tile_start < n_train; tile_start += TILE)
    {
        /* Cooperatively load TILE training vectors.
         * 128 work-items load (TILE x DIMS) = 4096 floats.
         * Each work-item loads 4096/128 = 32 floats. */
        for (int i = lid; i < TILE * DIMS; i += LOCAL_SZ)
        {
            int train_idx  = tile_start + i / DIMS;
            int dim_idx    = i % DIMS;
            float v = train_idx < n_train ? 
                    training_x[train_idx * DIMS + dim_idx] : 0;
            ltrain[i / DIMS][dim_idx] = v;                      /* row-major layout in local mem for clean access */
        }

        barrier(CLK_LOCAL_MEM_FENCE);

        /* ---- compute distances to all vectors in this tile -- */
        if (gid < n_test)
        {
            int count = min(TILE, n_train - tile_start);
            for (int i = 0; i < count; i++)
            {
                float dist = 0.0f;
                for (int j = 0; j < DIMS; j++)
                {
                    dist += (q[j] - ltrain[i][j]) * 
                            (q[j] - ltrain[i][j]);
                }

                if (min_dist > dist) 
                {
                    min_dist  = dist;
                    best = training_y[tile_start + i];
                }
            }
        }
        barrier(CLK_LOCAL_MEM_FENCE);                        /* before next tile load */
    }

    /* ---- write result (sqrt optional -- ordering is preserved) */
    if (gid < n_test) 
    {
        out_labels[gid] = best;
    }
}