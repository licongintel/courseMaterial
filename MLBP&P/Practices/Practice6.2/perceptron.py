import numpy

class Perceptron(object):
    def __init__(self, max_iteration = 100):
        self.max_iteration = max_iteration

    def train(self, training_data):
        self.binary_perceptrons = {}
        for i in range(0, training_data.get_data_size()):
            label = training_data.get_label(i)
            if label not in self.binary_perceptrons:
                self.binary_perceptrons[label] =\
                        BinaryPerceptron(self.max_iteration)

        w = numpy.zeros(len(training_data.get_feature(0)))    
        for label in self.binary_perceptrons.keys():
            data = BinaryData(training_data, label)
            self.binary_perceptrons[label].train(data)
            w += numpy.absolute(self.binary_perceptrons[label].getw())

        #indices = [0] * len(training_data.get_feature(0))
        #for i in range(0, len(w)):
        #    indices[i] = i
        #for i in range(0, len(w)):
        #    best = i
        #    for j in range(i + 1, len(w)):
        #        if w[indices[j]] > w[indices[best]]:
        #            best = j
        #    temp = indices[best]
        #    indices[best] = indices[i]
        #    indices[i] = temp
        #    print(str(i) + " " + str(indices[i]) + " " + str(w[indices[i]]))

    def classify(self, test_sample):
        best_score = -10000000000000
        result = None
        for label in self.binary_perceptrons.keys():
            score = self.binary_perceptrons[label].\
                    score(test_sample)
            if score > best_score:
                best_score = score
                result = label
        return result

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

    def getw(self):
        return self.w
            

class BinaryData(object):
    def __init__(self, original_data, label):
        self.data = original_data
        self.label = label

    def get_data_size(self):
        return self.data.get_data_size()

    def get_feature(self, index):
        return self.data.get_feature(index)

    def get_label(self, index):
        if self.data.get_label(index) == self.label:
            return 1
        else:
            return -1

