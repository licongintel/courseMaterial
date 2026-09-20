import argparse
import random
import numpy
import classificationData
import tester

import perceptron

max_dimension = 100
relevant_dimension = 10
rounds = 100

def generate_parameters():
    w = []
    for i in range(0, relevant_dimension):
        value = random.gauss(0, 0.5)
        value = abs(value)
        w.append(value)
    w.sort(reverse = True)
    for i in range(0, relevant_dimension):
        if random.random() > 0.5:
            w[i] = -w[i]
    b = random.random() * 2 - 1
    return (w, b)
            

def generate_data(dimension, w, b):
    x = []
    sum = 0
    for i in range(0, max_dimension):
        tmp = random.random() * 2 - 1
        if i < relevant_dimension:
            sum += (tmp * w[i])
        if i < dimension:
            x.append(tmp)
    sum += b
    if sum >= 0:
        y = 1
    else:
        y = -1
    return (numpy.array(x), y)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("training_size", type = int,
            help = "number of training samples")    

    args = parser.parse_args()
    training_size = args.training_size

    test_size = 1000

    result = []

    for dimension in range(3, 16):

        avg = 0
        for j in range(0, rounds):
            random.seed(j)
            (w, b) = generate_parameters()
            test_data = classificationData.ClassificationData()
            for i in range(0, test_size):
                (x, y) = generate_data(dimension, w, b)
                test_data.add_item(x, y)
            training_data = classificationData.ClassificationData()
            for i in range(0, training_size):
                (x, y) = generate_data(dimension, w, b)
                training_data.add_item(x, y)
                
            classifier = perceptron.BinaryPerceptron(margin = 10)
            
            tmp_tester = tester.Tester(classifier)
            accuracy = tmp_tester.train_and_test(training_data, test_data)
            avg += accuracy
            
        avg /= rounds
        print(str(dimension) + ": " + str(avg))
