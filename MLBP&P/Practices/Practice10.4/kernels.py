import numpy

class PolynomialKernel(object):
    def __init__(self, degree):
        self.degree = degree

    def calculate(self, sample1, sample2):
        return (numpy.dot(sample1,
                sample2) + 1) ** self.degree
