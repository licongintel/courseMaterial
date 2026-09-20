#include "data.h"

Data read_file(const char *filename)
{
	Data data;
	FILE *f = fopen(filename, "r");
	fscanf(f, "%d", &(data.total));
	data.x = new double*[data.total];
	data.y = new int[data.total];
	for (int i = 0; i < data.total; i++)
	{
		fscanf(f, "%d", &(data.y[i]));
		data.x[i] = new double[DIM];
		for (int j = 0; j < DIM; j++)
		{
			fscanf(f, "%lf", &(data.x[i][j]));
		}
	}
	fclose(f);
	return data;
}

void flush_data(Data data)
{
	for (int i = 0; i < data.total; i++)
	{
		flush_array((void*)(data.x[i]), DIM * sizeof(double));
	}
	flush_array((void*)(data.x), data.total * sizeof(double*));
}

void flush_array(void* ptr, size_t size)
{
    char* p = (char*)ptr;
    for (size_t i = 0; i < size; i += 64)
        _mm_clflush(p + i);
}

DataF read_file_f(const char *filename)
{
	DataF data;
	FILE *f = fopen(filename, "r");
	fscanf(f, "%d", &(data.total));
	data.x = new float*[data.total];
	data.y = new int[data.total];
	for (int i = 0; i < data.total; i++)
	{
		fscanf(f, "%d", &(data.y[i]));
		data.x[i] = new float[DIM];
		for (int j = 0; j < DIM; j++)
		{
			fscanf(f, "%f", &(data.x[i][j]));
		}
	}
	fclose(f);
	return data;
}

void flush_data_f(DataF data)
{
	for (int i = 0; i < data.total; i++)
	{
		flush_array((void*)(data.x[i]), DIM * sizeof(float));
	}
	flush_array((void*)(data.x), data.total * sizeof(float*));
}
