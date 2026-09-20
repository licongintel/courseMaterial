#include <time.h>
#include "data.h"

#define TEST_FILE "../data/usps.t.txt"
#define TRAINING_FILE "../data/usps.dup4.txt"

// Usage: mingw32-make SRC=tile.cpp EXTRA_CXXFLAGS="-DTEST_TILE=50 -DTRAIN_TILE=100" run
//        TEST_TILE / TRAIN_TILE default to -1 = use the entire test/training data

#ifndef TEST_TILE
#define TEST_TILE -1
#endif

#ifndef TRAIN_TILE
#define TRAIN_TILE -1
#endif

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

int main()
{
	Data training_data = read_file(TRAINING_FILE);
	Data test_data = read_file(TEST_FILE);

	int test_tile = TEST_TILE < 1 ? test_data.total : TEST_TILE;
	int train_tile = TRAIN_TILE < 1 ? training_data.total : TRAIN_TILE;

	double *min_dist = new double[test_data.total];
	int *best = new int[test_data.total];
	for (int i = 0; i < test_data.total; i++)
	{
		best[i] = -1;
		min_dist[i] = 1e+9;
	}

	flush_data(training_data);
	flush_data(test_data);
	flush_array((void*)min_dist, test_data.total * sizeof(double));
	flush_array((void*)best, test_data.total * sizeof(int));

	printf("Run with tile size %d, %d ... ", test_tile, train_tile);
	clock_t start = clock();
	for (int i = 0; i < test_data.total; i += test_tile)
	{
		for (int j = 0; j < training_data.total; j += train_tile)
		{
			for (int tile_i = 0; tile_i < test_tile; tile_i++)
			{
				int real_i = i + tile_i;
				if (real_i >= test_data.total)
				{
					break;
				}
				for (int tile_j = 0; tile_j < train_tile; tile_j++)
				{
					int real_j = j + tile_j;
					if (real_j >= training_data.total)
					{
						break;
					}
					double dist = calc_dist(test_data.x[real_i], 
							training_data.x[real_j]);
					if (min_dist[real_i] > dist)
					{
						min_dist[real_i] = dist;
						best[real_i] = real_j;
					}
				}
			}
		}
	}
    clock_t end = clock();
    printf("Done\n");

    double elapsed = double(end - start) / CLOCKS_PER_SEC;
    printf("Elapsed: %.3f seconds\n", elapsed);
    printf("Average latency: %.4f ms/sample\n", 
            elapsed / test_data.total * 1000);
    printf("Throughput: %.1f samples/s\n", test_data.total / elapsed);
	
	int correct = 0;
	for (int i = 0; i < test_data.total; i++)
	{
		if (training_data.y[best[i]] == test_data.y[i])
		{
			correct++;
		}
	}
	printf("%d / %d = %f\n", correct, test_data.total, 
			(float)correct / test_data.total);
	return 0;
}

