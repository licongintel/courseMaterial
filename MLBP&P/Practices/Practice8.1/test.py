import argparse
import random
import numpy
import classificationData

import tester
#import nearestNeighbor
import logisticRegression

def generate_data():
    x1 = random.random() * 6 - 3
    x2 = random.random() * 30 - 15
    x = []
    x.append(x1)
    y = 1
    if x[0] < -1:
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

    #classifier = nearestNeighbor.NearestNeighbor()
    classifier = logisticRegression.\
                 BinaryLogisticRegression(regularizer = 0.1)
    tester = tester.Tester(classifier)
    tester.train_and_test(training_data, test_data)

