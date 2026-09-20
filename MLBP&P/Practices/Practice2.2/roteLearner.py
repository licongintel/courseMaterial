
class RoteLearner(object):

    
    def __init__(self):
        self.training_data = None

    def train(self, training_data):
        self.training_data = training_data

    def classify(self, test_sample):
        for i in range(0, self.training_data.get_data_size()):
            x = self.training_data.get_feature(i)
            equal = True
            for j in range(0, len(x)):
                if (test_sample[j] != x[j]):
                    equal = False
                    break
            if (equal):
                return self.training_data.get_label(i)
        return None
