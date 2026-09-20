import tester
import argparse

import nearestNeighbor


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--training_file", type = str,
            default = "usps",
            help = "training data file (default: usps)")
    parser.add_argument("-e", "--test_file", type = str,
            default = "usps",
            help = "test data file (default: usps)")
    args = parser.parse_args()
    training_file = args.training_file
    test_file = args.test_file

    classifier = nearestNeighbor.NearestNeighbor()
    tester = tester.Tester(classifier)
    
    tester.train_on_file(training_file)
    tester.test_accuracy_on_file(test_file)
