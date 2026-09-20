import argparse
import random
import numpy
import classificationData
import tester

import perceptron

def generate_data(dimension):

    x1 = random.random() * 6 - 3
    x2 = random.random() * 30 - 15
    x = []
    x.append(x1)

    if dimension == 2:
        x.append(x2)

    y = 1
    if x[0] < -1:
        y = -1
    return (numpy.array(x), y)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("training_size", type = int,
            help = "number of training samples")
    
    parser.add_argument("-d", "--dimension", type = int,
            default = 2, help = "dimension of feature vector")

    args = parser.parse_args()
    training_size = args.training_size

    dimension = args.dimension

    test_size = 100

    random.seed(0)
    test_data = classificationData.ClassificationData()
    for i in range(0, test_size):
        (x, y) = generate_data(dimension)
        test_data.add_item(x, y)
    training_data = classificationData.ClassificationData()
    for i in range(0, training_size):
        (x, y) = generate_data(dimension)
        training_data.add_item(x, y)

    classifier = perceptron.BinaryPerceptron()
    
    tester = tester.Tester(classifier)
    tester.train_and_test(training_data, test_data)

