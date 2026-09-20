import numpy
import math
from perceptron import BinaryData

class LogisticRegression(object):
    def __init__(self, regularizer = 0.0001, tolerance = 0.0001,  
            max_iteration = 1000, learning_rate = 10):
        self.regularizer = regularizer
        self.tolerance = tolerance
        self.max_iteration = max_iteration
        self.learning_rate = learning_rate

    def train(self, training_data):
        self.binary_regressors = {}
        for i in range(0, training_data.get_data_size()):
            label = training_data.get_label(i)
            if label not in self.binary_regressors:
                self.binary_regressors[label] =\
                        BinaryLogisticRegression(
                        regularizer = self.regularizer,
                        tolerance = self.tolerance,
                        max_iteration = self.max_iteration,
                        learning_rate = self.learning_rate)
                
        for label in self.binary_regressors.keys():
            data = BinaryData(training_data, label)
            print("Training classifier " + label)
            self.binary_regressors[label].train(data)

    def score_all(self, test_sample):
        results = {}
        for label in self.binary_regressors.keys():
            score = self.binary_regressors[label].\
                    score(test_sample)
            results[label] = score
        return results

    def classify(self, test_sample):
        best_score = -10000000000000
        result = None
        for label in self.binary_regressors.keys():
            score = self.binary_regressors[label].\
                    score(test_sample)
            if score > best_score:
                best_score = score
                result = label
        return result


class BinaryLogisticRegression(object):
    def __init__(self, regularizer = 0.0001, tolerance = 0.0001, 
            max_iteration = 1000, learning_rate = 10):

        self.max_iteration = max_iteration
        self.regularizer = regularizer
        self.learning_rate = learning_rate
        self.tolerance = tolerance

    def train(self, training_data):
        self.w = numpy.zeros(len(training_data.get_feature(0)))
        self.b = 0
        previous_loss = -1
        
        for i in range(0, self.max_iteration):
            if i % 100 == 0:
                print("Iteration " + str(i))
                
            w_gradient = numpy.zeros(
                    len(training_data.get_feature(0)))
            b_gradient = 0
            loss = 0
            
            for j in range(0, training_data.get_data_size()):
                feature = training_data.get_feature(j)
                label = self.transform_label(
                        training_data.get_label(j))
                p = self.score(feature)
                loss -= ((label * math.log(p) + (1 - label)\
                        * math.log(1 - p)))
                w_gradient += (feature * (p - label))
                b_gradient += (p - label)
                
            loss += numpy.dot(self.w, self.w) *\
                    self.regularizer / 2
            loss /= training_data.get_data_size()
            #print('iteration {}: w = {:.2f}, b = {:.2f}, '.\
            #        format(i, self.w[0], self.b), end = '')
            #print('loss = {:.6f}'.format(loss))
            
            if previous_loss != -1:
                if abs(previous_loss - loss) < self.tolerance:
                    break
            previous_loss = loss

            w_gradient += (self.w * self.regularizer)
            w_gradient /= training_data.get_data_size()
            b_gradient /= training_data.get_data_size()
            self.w -= (w_gradient * self.learning_rate)
            self.b -= (b_gradient * self.learning_rate)

    def transform_label(self, label):
        if label == -1:
            return 0
        return 1

    def score(self, test_sample):
        result = numpy.dot(test_sample, self.w) + self.b
        return 1 / (1 + math.exp(-result))

    def classify(self, test_sample):
        score = self.score(test_sample)
        if score >= 0.5:
            return 1
        else:
            return -1


