#include <time.h>
#include <windows.h>
#include "data.h"

#define TEST_FILE "../data/usps.t.txt"
#define TRAINING_FILE "../data/usps.txt"

#ifndef THREADS
#define THREADS 2
#endif

typedef struct 
{
    int thread_id;
    Data *training_data;
    Data *test_data;
    int test_start, test_end;
    int correct;
    double elapsed;
} ThreadData;

double calc_dist(double *x1, double *x2)
{
    double sum = 0;
    #pragma clang loop interleave(enable)
    for (int i = 0; i < DIM; i++)
    {
        sum += ((x1[i] - x2[i]) * (x1[i] - x2[i]));
    }
    return sum;
}

DWORD WINAPI process_chunk(LPVOID arg) 
{
    ThreadData *td = (ThreadData *)arg;
    clock_t start = clock();
    td->correct = 0;
    for (int i = td->test_start; i < td->test_end; i++)
    {
        double min_dist = 1e+9;
        int best = -1;
        for (int j = 0; j < td->training_data->total; j++)
        {
            double dist = calc_dist(td->test_data->x[i], 
                    td->training_data->x[j]);
            if (min_dist > dist)
            {
                min_dist = dist;
                best = j;
            }
        }
        if (td->training_data->y[best] == td->test_data->y[i])
        {
            td->correct++;
        }
    }
    clock_t end = clock();
    td->elapsed = double(end - start) / CLOCKS_PER_SEC;
    return 0;
}

int main()
{
    Data training_data = read_file(TRAINING_FILE);
    Data test_data = read_file(TEST_FILE);

    HANDLE threads[THREADS];
    ThreadData td[THREADS];

    int chunk = test_data.total / THREADS;
    for (int t = 0; t < THREADS; t++)
    {
        td[t].thread_id = t;
        td[t].training_data = &training_data;
        td[t].test_data = &test_data;
        td[t].test_start = t * chunk;
        td[t].test_end = (t == THREADS - 1) ? 
                test_data.total : (t + 1) * chunk;
    }

    clock_t start = clock();
    for (int t = 0; t < THREADS; t++) 
    {
        threads[t] = CreateThread(NULL, 0, 
                process_chunk, &td[t], 0, NULL);
    }
    WaitForMultipleObjects(THREADS, threads, TRUE, INFINITE);
    clock_t end = clock();

    int correct = 0;
    for (int t = 0; t < THREADS; t++)
    {
        correct += td[t].correct;
    }

    double elapsed = double(end - start) / CLOCKS_PER_SEC;
    printf("Elapsed: %.3f seconds\n", elapsed);
    for (int t = 0; t < THREADS; t++)
    {
        int samples = td[t].test_end - td[t].test_start;
        printf("Worker %d: average latency %.4f ms/sample\n", 
                t, td[t].elapsed / samples * 1000);
    }
    printf("Throughput: %.1f samples/s\n", test_data.total / elapsed);
    printf("%d / %d = %f\n", correct, test_data.total, 
            (float)correct / test_data.total);
    return 0;
}
