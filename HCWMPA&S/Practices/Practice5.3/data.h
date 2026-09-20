#include <stdio.h>
#include <immintrin.h>
#include <stddef.h>

#define DIM 256

typedef struct 
{
    int total;
    double **x;
    int *y;
} Data;

typedef struct 
{
    int total;
    float **x;
    int *y;
} DataF;

Data read_file(const char *filename);
void flush_data(Data data);
void flush_array(void* ptr, size_t size);
DataF read_file_f(const char *filename);
void flush_data_f(DataF data);
