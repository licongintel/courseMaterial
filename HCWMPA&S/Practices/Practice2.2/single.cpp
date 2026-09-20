#include <ctime>
#include <stdio.h>
#include <conio.h>

#define STEPS 10000000
#define RECORD_NUM 256

double mu = 0.5;
double x = 0;

double records[RECORD_NUM] = {0};

int main()
{
    clock_t start = clock();
    for (int i = 0; i < STEPS - RECORD_NUM; i++)
    {
        x = 1 - mu * x * x;
    }

    for (int i = 0; i < RECORD_NUM; i++)
    {
        x = 1 - mu * x * x;
        records[i] = x;
    }
    clock_t end = clock();
    double elapsed = double(end - start) / CLOCKS_PER_SEC;
    printf("Elapsed: %.3f seconds\n", elapsed);

    printf("Press enter to output the latest records ...\n");
    getch();

    for (int i = 0; i < RECORD_NUM; i++)
    {
        printf("%3d: %6.3lf\n", i, records[i]);
    }
    
    return 0;
}

