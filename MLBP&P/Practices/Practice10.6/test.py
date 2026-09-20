
import tester
import perceptron
import uspsData
import kernels

if __name__ == '__main__':
    training_data = uspsData.USPSData("usps")
    test_data = uspsData.USPSData("usps.t")

    kernel = kernels.RBFKernel(gamma = 0.2)
    classifier = perceptron.Perceptron(max_iteration = 100, margin = 5.0, kernel = kernel)
    t = tester.Tester(classifier)
    t.train_and_test(training_data, test_data)

    input("Press Enter to continue...")

    kernel = kernels.PolynomialKernel(degree = 5)
    classifier = perceptron.Perceptron(max_iteration = 300, margin = 5.0, kernel = kernel)
    t = tester.Tester(classifier)
    t.train_and_test(training_data, test_data)





