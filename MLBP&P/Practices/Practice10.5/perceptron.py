import numpy

class Perceptron(object):
    def __init__(self, max_iteration = 100, margin = 0):
        self.margin = margin
        
        self.max_iteration = max_iteration

    def train(self, training_data):
        self.binary_perceptrons = {}
        for i in range(0, training_data.get_data_size()):
            label = training_data.get_label(i)
            if label not in self.binary_perceptrons:                
                self.binary_perceptrons[label] =\
                        BinaryPerceptron(self.max_iteration,
                                self.margin)                
        for label in self.binary_perceptrons.keys():
            data = BinaryData(training_data, label)
            print("training classifier " + label)
            self.binary_perceptrons[label].train(data)

    def score_all(self, test_sample):
        results = {}
        for label in self.binary_perceptrons.keys():
            score = self.binary_perceptrons[label].\
                    score(test_sample)
            results[label] = score
        return results

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

class BinaryKernelPerceptron(object):

    def __init__(self, kernel, max_iteration = 100, margin = 0):
        self.margin = margin
        self.kernel = kernel
        self.max_iteration = max_iteration

    def train(self, training_data):
        self.training_data = training_data
        self.c = numpy.zeros(training_data.get_data_size())
        self.b = 0

        self.calc_threshold(training_data)
        for i in range(0, self.max_iteration):
            updated = False
            if i % 100 == 0:
                print("Epoch " + str(i))
            for j in range(0, training_data.get_data_size()):
                sample = training_data.get_feature(j)
                score = self.score(sample)
                label = training_data.get_label(j)                
                if score * label <= self.threshold:
                    self.c[j] += label
                    self.b += (label * self.max_norm_sqr)
                    updated = True
            if not updated:
                break

    def calc_threshold(self, training_data):
        self.max_norm_sqr = 0
        for i in range(0, training_data.get_data_size()):
            sample = training_data.get_feature(i)
            norm_sqr = self.kernel.calculate(sample, sample)
            if norm_sqr > self.max_norm_sqr:
                self.max_norm_sqr = norm_sqr
        self.threshold = self.max_norm_sqr\
                * self.margin

    def score(self, test_sample):
        result = 0
        for i in range(0, len(self.c)):
            if self.c[i] != 0:
                result += (self.c[i] * self.kernel.\
                        calculate(test_sample,
                        self.training_data.get_feature(i)))
        return result + self.b

    def classify(self, test_sample):
        score = self.score(test_sample)
        if score >= 0:
            return 1
        else:
            return -1

class BinaryPerceptron(object):

    def __init__(self, max_iteration = 100, margin = 0):
        self.margin = margin

        self.max_iteration = max_iteration

    def train(self, training_data):
        self.w = numpy.zeros(len(training_data.get_feature(0)))
        self.b = 0

        self.calc_threshold(training_data)

        for i in range(0, self.max_iteration):
            updated = False
            for j in range(0, training_data.get_data_size()):
                sample = training_data.get_feature(j)
                score = self.score(sample)
                label = training_data.get_label(j)
                
                if score * label <= self.threshold:
                    self.w += (sample * label)
                    self.b += (label * self.max_norm * self.max_norm)

                    updated = True
            if not updated:
                break

    def calc_threshold(self, training_data):
        self.max_norm = 0
        for i in range(0, training_data.get_data_size()):
            sample = training_data.get_feature(i)
            norm = numpy.linalg.norm(sample, ord = 2)
            if norm > self.max_norm:
                self.max_norm = norm
        self.threshold = self.max_norm * self.max_norm\
                * self.margin

    def score(self, test_sample):
        return numpy.dot(test_sample, self.w) + self.b

    def classify(self, test_sample):
        score = self.score(test_sample)
        if score >= 0:
            return 1
        else:
            return -1
            

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

