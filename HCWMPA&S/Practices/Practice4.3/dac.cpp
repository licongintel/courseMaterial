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
    double *x;
    int slice_start, slice_end;
    double min_dist;
    int best;
    HANDLE go_event, done_event;
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
    for (;;)
    {
        WaitForSingleObject(td->go_event, INFINITE);
        td->min_dist = 1e+9;
        td->best = -1;
        for (int j = td->slice_start; j < td->slice_end; j++)
        {
            double dist = calc_dist(td->x, td->training_data->x[j]);
            if (td->min_dist > dist)
            {
                td->min_dist = dist;
                td->best = j;
            }
        }
        SetEvent(td->done_event);
    }
    return 0;
}

int main()
{
    Data training_data = read_file(TRAINING_FILE);
    Data test_data = read_file(TEST_FILE);

    HANDLE threads[THREADS];
    ThreadData td[THREADS];
    HANDLE done_events[THREADS];

    int slice = training_data.total / THREADS;
    for (int t = 0; t < THREADS; t++)
    {
        td[t].thread_id = t;
        td[t].training_data = &training_data;
        td[t].slice_start = t * slice;
        td[t].slice_end = (t == THREADS - 1) ? 
                training_data.total : (t + 1) * slice;
        td[t].go_event = CreateEvent(NULL, FALSE, FALSE, NULL);
        td[t].done_event = CreateEvent(NULL, FALSE, FALSE, NULL);
        done_events[t] = td[t].done_event;
    }

    clock_t start = clock();
    for (int t = 0; t < THREADS; t++) 
    {
        threads[t] = CreateThread(NULL, 0, 
                process_chunk, &td[t], 0, NULL);
    }
    int correct = 0;
    for (int i = 0; i < test_data.total; i++)
    {
        for (int t = 0; t < THREADS; t++)
        {
            td[t].x = test_data.x[i];
            SetEvent(td[t].go_event);
        }
        WaitForMultipleObjects(THREADS, done_events, TRUE, INFINITE);

        double min_dist = 1e+9;
        int best = -1;
        for (int t = 0; t < THREADS; t++)
        {
            if (min_dist > td[t].min_dist)
            {
                min_dist = td[t].min_dist;
                best = td[t].best;
            }
        }
        if (training_data.y[best] == test_data.y[i])
        {
            correct++;
        }
    }

    clock_t end = clock();
    double elapsed = double(end - start) / CLOCKS_PER_SEC;
    printf("Elapsed: %.3f seconds\n", elapsed);
    printf("Average latency: %.4f ms/sample\n", 
            elapsed / test_data.total * 1000);
    printf("Throughput: %.1f samples/s\n", test_data.total / elapsed);
    printf("%d / %d = %f\n", correct, test_data.total, 
            (float)correct / test_data.total);
    return 0;
}
