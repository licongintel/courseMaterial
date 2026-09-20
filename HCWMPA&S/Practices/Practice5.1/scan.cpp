#include <ctime>
#include <stdio.h>
#include <conio.h>
#include <stdlib.h>

// STEPS & SERIES to be varied, but 
//   keeping STEPS * SERIES as a constant  
//   Some typical numbers:
//   1. SERIES      32; STEPS 163840000
//        or 
//      SERIES      16; STEPS 327680000
//        (depending on SIMD, super scalar, 
//           & instruction pipelining)
//   2. SERIES    1024; STEPS   5120000
//   3. SERIES   65536; STEPS     80000
//   4. SERIES  524288; STEPS     10000
//   5. SERIES 2097152; STEPS      2500
#ifndef STEPS
#define STEPS 10000000
#endif
#ifndef SERIES
#define SERIES 1024
#endif
#define ORIGINAL 16

double original[ORIGINAL] = {0.5, 1.0, 1.368, 1.394, 
                     1.399, 1.4008, 1.40108, 1.4114, 
                     1.5, 1.575, 1.58, 1.626, 
                     1.629, 1.74, 1.76, 1.8};
double mu[SERIES];
double x[SERIES] = {0};

int main()
{
    for (int i = 0; i < SERIES; i++)
    {
        mu[i] = original[i % ORIGINAL];
    }

    clock_t start = clock();

    for (int i = 0; i < STEPS; i++)
    {
        for (int j = 0; j < SERIES; j++)
        {
            x[j] = 1 - mu[j] * x[j] * x[j];
        }
    }
    
    clock_t end = clock();
    double elapsed = double(end - start) / CLOCKS_PER_SEC;
    printf("Elapsed: %.3f seconds\n", elapsed);

    
    return 0;
}

