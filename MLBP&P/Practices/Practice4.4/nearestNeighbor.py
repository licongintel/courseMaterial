import numpy

class NearestNeighbor(object):
    
    def __init__(self, distance_type = 0):
        self.training_data = None
        self.distance_type = distance_type

    def train(self, training_data):
        self.training_data = training_data

    def classify(self, test_sample):
        best_index = -1
        min_distance = 10000000

        norm = numpy.linalg.norm(test_sample, ord = 2)
        
        for i in range(0, self.training_data.get_data_size()):
            x = self.training_data.get_feature(i)

            if self.distance_type == 0:
                distance = numpy.linalg.norm(x - test_sample,
                        ord = 2)
            else:
                distance = 1 - numpy.dot(x, test_sample)\
                           / numpy.linalg.norm(x, ord = 2)\
                           / norm
                
            if (min_distance > distance):
                min_distance = distance
                best_index = i
        return self.training_data.get_label(best_index)
            

