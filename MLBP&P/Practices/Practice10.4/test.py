import argparse
import random
import numpy
import classificationData

import tester
import perceptron
import kernels

def generate_data():
    x1 = random.random() * 4 - 2
    x2 = random.random() * 4 - 2
    x = []
    x.append(x1)
    x.append(x2)
    y = 1
    if -0.1 * x1 + x1 * x2 + 0.1 * x2 < 0:
        y = -1
    return (numpy.array(x), y)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("training_size", type = int,
            help = "number of training samples")
    args = parser.parse_args()
    training_size = args.training_size
    test_size = 100

    random.seed(0)
    test_data = classificationData.ClassificationData()
    for i in range(0, test_size):
        (x, y) = generate_data()
        test_data.add_item(x, y)
    training_data = classificationData.ClassificationData()
    for i in range(0, training_size):
        (x, y) = generate_data()
        training_data.add_item(x, y)

    kernel = kernels.PolynomialKernel(2)
    classifier = perceptron.BinaryKernelPerceptron(kernel, 
            max_iteration = 1000, margin = 10)
    tester = tester.Tester(classifier)
    tester.train_and_test(training_data, test_data)

