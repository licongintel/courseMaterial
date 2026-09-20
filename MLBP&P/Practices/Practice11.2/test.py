
import numpy
import uspsData
import uspsCNN
import tester

if __name__ == '__main__':
    training_data = uspsData.USPSData("usps")
    test_data = uspsData.USPSData("usps.t")
    
    numpy.random.seed(0)
    classifier = uspsCNN.USPSCNN(max_epoch = 30)
    tester = tester.Tester(classifier)
    tester.train_and_test(training_data, test_data)
