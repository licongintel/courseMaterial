
import tester
import perceptron
import uspsData

if __name__ == '__main__':
    training_data = uspsData.USPSData("usps")
    test_data = uspsData.USPSData("usps.t")
    classifier = perceptron.Perceptron(max_iteration = 1000,
            margin = 10.0)    
    t = tester.Tester(classifier)
    t.train_and_test(training_data, test_data)




