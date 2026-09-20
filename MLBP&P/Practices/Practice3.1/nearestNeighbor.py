
class NearestNeighbor(object):
    
    def __init__(self):
        self.training_data = None

    def train(self, training_data):
        self.training_data = training_data

    def classify(self, test_sample):
        best_index = -1
        min_distance = 10000000

        for i in range(0, self.training_data.get_data_size()):
            x = self.training_data.get_feature(i)
            distance = 0
            for j in range(0, len(x)):
                distance += abs(test_sample[j] - x[j])
            if (min_distance > distance):
                min_distance = distance
                best_index = i
        return self.training_data.get_label(best_index)
            

