#include <ctime>
#include <stdio.h>
#include <conio.h>
#include <stdlib.h>

#define STEPS 10000000
#define RECORD_NUM 256
// SERIES to be varied, e.g., from 4 to 64, 
//   to see how execution time varies 
//   w.r.t. the number of series
#ifndef SERIES
#define SERIES 16
#endif
#define ORIGINAL 16

double original[ORIGINAL] = {0.5, 1.0, 1.368, 1.394, 
                     1.399, 1.4008, 1.40108, 1.4114, 
                     1.5, 1.575, 1.58, 1.626, 
                     1.629, 1.74, 1.76, 1.8};
double mu[SERIES];
double x[SERIES] = {0};
double records[RECORD_NUM][SERIES];

int main()
{
    for (int i = 0; i < SERIES; i++)
    {
        mu[i] = original[i % ORIGINAL];
    }

    clock_t start = clock();

    for (int i = 0; i < STEPS - RECORD_NUM; i++)
    {
        for (int j = 0; j < SERIES; j++)
        {
            x[j] = 1 - mu[j] * x[j] * x[j];
        }
    }
    for (int i = 0; i < RECORD_NUM; i++)
    {
        for (int j = 0; j < SERIES; j++)
        {
            x[j] = 1 - mu[j] * x[j] * x[j];
            records[i][j] = x[j];
        }
    }
    
    clock_t end = clock();
    double elapsed = double(end - start) / CLOCKS_PER_SEC;
    printf("Elapsed: %.3f seconds\n", elapsed);

    printf("Press enter to output the latest records ...\n");
    getch();
    int group = (int)(rand() % ((SERIES - 1) / ORIGINAL + 1));
    int offset = group * ORIGINAL;
    int len = (SERIES - offset) < ORIGINAL ? 
              (SERIES - offset) : ORIGINAL;
    for (int i = 0; i < RECORD_NUM; i++)
    {
        printf("%3d: ", i);
        for (int j = 0; j < len; j++)
        {
            printf("%6.3lf ", records[i][offset + j]);
        }
        printf("\n");
    }
    
    return 0;
}

