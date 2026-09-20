
import numpy

class BinaryPerceptron(object):
    def __init__(self, max_iteration = 100):
        self.max_iteration = max_iteration

    def train(self, training_data):
        self.w = numpy.zeros(len(training_data.get_feature(0)))
        self.b = 0
        
        for i in range(0, self.max_iteration):
            updated = False

            for j in range(0, training_data.get_data_size()):
                sample = training_data.get_feature(j)
                score = self.score(sample)
                label = training_data.get_label(j)
                if score * label <= 0:
                    self.w += (sample * label)
                    self.b += label
                    updated = True
            if not updated:
                break

    def score(self, test_sample):
        return numpy.dot(test_sample, self.w) + self.b

    def classify(self, test_sample):
        score = self.score(test_sample)
        if score >= 0:
            return 1
        else:
            return -1           

