#include <stdio.h>
#include <ctime>
#include <cstdlib>

#ifndef M
#define M 4096
#endif
#ifndef N
#define N 4096
#endif

double data[M][N];

void init()
{
    //data = (double **)malloc(M * sizeof(double *));
    for (int i = 0; i < M; i++)
    {
        //data[i] = (double *)malloc(N * sizeof(double));
        for (int j = 0; j < N; j++)
        {
            data[i][j] = (double)rand() / RAND_MAX; 
        }
    }
}

double slow_add()
{
    double result = 0;
    for (int j = 0; j < N; j++)
    {
        for (int i = 0; i < M; i++)
        {
            result += data[i][j];
        }
    }
    return result;
}


double fast_add()
{
    double result = 0;
    for (int i = 0; i < M; i++)
    {
        for (int j = 0; j < N; j++)
        {
            result += data[i][j];
        }
    }
    return result;
}

int main(int argc, char **argv)
{
    init();

    double (*sum_fn)() = (argc > 1 && argv[1][0] == 's') ? slow_add : fast_add;

    clock_t start = clock();
    double result = sum_fn();
    clock_t end = clock();

    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    printf("result = %.0f  time = %.3f s  (%d x %d)\n", result, elapsed, M, N);

    return 0;
}