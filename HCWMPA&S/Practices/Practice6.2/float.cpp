#include <time.h>
#include "data.h"

#define TEST_FILE "../data/usps.t.txt"
#define TRAINING_FILE "../data/usps.txt"

float calc_dist(float *x1, float *x2)
{
	float sum = 0;
	#pragma clang loop interleave(enable)
	for (int i = 0; i < DIM; i++)
	{
		sum += ((x1[i] - x2[i]) * (x1[i] - x2[i]));
	}
	return sum;
}

int main()
{
	DataF training_data = read_file_f(TRAINING_FILE);
	DataF test_data = read_file_f(TEST_FILE);
	
	int correct = 0;
	clock_t start = clock();
	for (int i = 0; i < test_data.total; i++)
	{
		float min_dist = 1e+9;
		int best = -1;
		for (int j = 0; j < training_data.total; j++)
		{
			float dist = calc_dist(test_data.x[i], training_data.x[j]);
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