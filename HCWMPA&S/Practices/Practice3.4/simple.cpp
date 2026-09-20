#include <time.h>
#include "data.h"

#define TEST_FILE "../data/usps.t.txt"
#define TRAINING_FILE "../data/usps.txt"

double calc_dist(double *x1, double *x2)
{
	double sum = 0;
	for (int i = 0; i < DIM; i++)
	{
		sum += ((x1[i] - x2[i]) * (x1[i] - x2[i]));
	}
	return sum;
}

int main()
{
	Data training_data = read_file(TRAINING_FILE);
	Data test_data = read_file(TEST_FILE);
	
	int correct = 0;
	clock_t start = clock();
	for (int i = 0; i < test_data.total; i++)
	{
		double min_dist = 1e+9;
		int best = -1;
		for (int j = 0; j < training_data.total; j++)
		{
			double dist = calc_dist(test_data.x[i], training_data.x[j]);
			if (min_dist > dist)
			{
				min_dist = dist;
				best = j;
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
	
	printf("%d / %d = %f", correct, test_data.total, 
			(float)correct / test_data.total);
	return 0;
}