import numpy

class PolynomialKernel(object):
    def __init__(self, degree):
        self.degree = degree

    def calculate(self, sample1, sample2):
        return (numpy.dot(sample1,
                sample2) + 1) ** self.degree

class RBFKernel(object):
    def __init__(self, gamma = 0, sigma = 0):
        self.gamma = gamma
        if self.gamma == 0:
            self.gamma = 1 / 2 / sigma / sigma   

    def calculate(self, sample1, sample2):
        diff = sample1 - sample2
        result = numpy.dot(diff, diff)
        return numpy.exp(-self.gamma * result) 

class GramMatrix(object):
    def __init__(self, data, kernel):
        print("Calculate Gram matrix")
        self.matrix = []

        self.total = data.get_data_size()
        for i in range(0, self.total):
            line = numpy.zeros(self.total)
            for j in range(0, self.total):
                if j >= i:
                    line[j] = kernel.calculate(
                            data.get_feature(i), 
                            data.get_feature(j))
                else:
                    line[j] = self.matrix[j][i]
            self.matrix.append(line)
    
    def get_row(self, i):
        return self.matrix[i]

    def get_max_norm_sqr(self):
        max_norm_sqr = 0
        for i in range(0, self.total):
            if max_norm_sqr < self.matrix[i][i]:
                max_norm_sqr = self.matrix[i][i]
        return max_norm_sqr
