class Tester(object):
    def __init__(self, classifier):
        self.classifier = classifier

    def train_and_test(self, training_data, test_data):
        self.classifier.train(training_data)
        correct = 0
        for i in range(0, test_data.get_data_size()):
            result = self.classifier.classify(
                    test_data.get_feature(i))
            if result == test_data.get_label(i):
                correct += 1
        accuracy = correct / test_data.get_data_size()
        
        return accuracy

