#include <ctime>
#include <stdio.h>
#include <conio.h>
#include <stdlib.h>

#ifndef STEPS
#define STEPS 80000
#endif
#ifndef SERIES
#define SERIES 65536
#endif

// Set TILES to 64 for good locality fitting to L1
// Set TILES to 2048 for extreme locality fitting to registers
#ifndef TILES
#define TILES 1
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

    for (int tile = 0; tile < TILES; tile++)
    {
        int t_start = tile * (SERIES / TILES);
        int t_end = (tile + 1) * (SERIES / TILES);
        for (int i = 0; i < STEPS; i++)
        {
            for (int j = t_start; j < t_end; j++)
            {
                x[j] = 1 - mu[j] * x[j] * x[j];
            }
        }
    }
    clock_t end = clock();

    double elapsed = double(end - start) / CLOCKS_PER_SEC;
    printf("Elapsed: %.3f seconds\n", elapsed);

    return 0;
}

