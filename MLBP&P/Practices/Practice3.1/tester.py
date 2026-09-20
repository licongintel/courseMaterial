
import uspsData

class Tester(object):
    def __init__(self, classifier):
        self.classifier = classifier

    def train_on_file(self, training_file):
        training_data = uspsData.USPSData(training_file)
        self.classifier.train(training_data)    

    def test_accuracy_on_file(self, test_file):
        test_data = uspsData.USPSData(test_file)
        correct = 0
        
        for i in range(0, test_data.get_data_size()):
            if (i % 100 == 0):
                print("Processing sample " + str(i))
                
            result = self.classifier.classify(
                    test_data.get_feature(i))
            if (result == test_data.get_label(i)):
                correct += 1
        accuracy = correct / test_data.get_data_size()
        print("Accuracy = " + str(correct) + " / " 
              + str(test_data.get_data_size()) +
              " = " + str(accuracy))
