import random
import interestData
import classificationData
import tester
import numpy

import perceptron

if __name__ == '__main__':
    for dimension in numpy.arange(1000, 8100, 100):
        data = interestData.InterestData("interest.acl94.txt",
                dimension = dimension)
        (x, y) = data.get_data()
        
        random.seed(0)
        training_data = classificationData.ClassificationData()
        test_data = classificationData.ClassificationData()
        for i in range(0, len(y)):
            if random.random() < 0.5:
                training_data.add_item(x[i], y[i])
            else:
                test_data.add_item(x[i], y[i])
                
        classifier = perceptron.Perceptron()

        t = tester.Tester(classifier)
        accuracy = t.train_and_test(training_data, test_data)
        print(str(dimension) + " features: " + str(accuracy))




