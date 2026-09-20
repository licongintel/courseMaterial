#include <stdio.h>
#include <ctime>
#include <conio.h>
#include <windows.h>

#define STEPS 10000000
#define RECORD_NUM 256

#define ORIGINAL 16
double original[ORIGINAL] = {0.5, 1.0, 1.368, 1.394, 
                             1.399, 1.4008, 1.40108, 1.4114, 
                             1.5, 1.575, 1.58, 1.626, 
                             1.629, 1.74, 1.76, 1.8};

#define SERIES 4096
#define THREADS 4
#define SERIES_T (SERIES / THREADS)

typedef struct 
{
    int thread_id;
    double *mu;
    double *x;
    double **records;
} ThreadData;

DWORD WINAPI process_chunk(LPVOID arg) 
{
    ThreadData *td = (ThreadData *)arg;
    for (int j = 0; j < STEPS - RECORD_NUM; j++)
    {
        for (int i = 0; i < SERIES_T; i++)
        {
            td->x[i] = 1 - td->mu[i] * td->x[i] * td->x[i];
        }
    }
    for (int j = 0; j < RECORD_NUM; j++)
    {
        for (int i = 0; i < SERIES_T; i++)
        {
            td->x[i] = 1 - td->mu[i] * td->x[i] * td->x[i];
            td->records[j][i] = td->x[i];
        }
    }
    return 0;
}

int main()
{
    HANDLE threads[THREADS];
    ThreadData td[THREADS];
    for (int t = 0; t < THREADS; t++)
    {
        td[t].thread_id = t;
        td[t].x = new double[SERIES_T];
        td[t].mu = new double[SERIES_T];
        for (int i = 0; i < SERIES_T; i++)
        {
            td[t].x[i] = 0;
            td[t].mu[i] = original[(SERIES_T * t + i) % ORIGINAL];
        }

        td[t].records = new double*[RECORD_NUM];
        for (int i = 0; i < RECORD_NUM; i++)
        {
            td[t].records[i] = new double[SERIES_T];
        }
    }
    
    clock_t start = clock();
    for (int t = 0; t < THREADS; t++) 
    {
        td[t].thread_id = t;
        threads[t] = CreateThread(NULL, 0, process_chunk, 
                                  &td[t], 0, NULL);
    }

    WaitForMultipleObjects(THREADS, threads, TRUE, INFINITE);
    clock_t end = clock();
    

    double elapsed = double(end - start) / CLOCKS_PER_SEC;
    printf("Elapsed: %.3f seconds\n", elapsed);
    printf("Press enter to output the latest records ...\n");
    getch();

    int t = rand() % THREADS;
    int group = rand() % (SERIES_T / ORIGINAL);
    for (int i = 0; i < RECORD_NUM; i++)
    {
        printf("%3d: ", i);
        for (int j = 0; j < ORIGINAL; j++)
        {
            printf("%6.3lf ", td[t].records[i][group * ORIGINAL + j]);
        }
        printf("\n");
    }
    return 0;
}

