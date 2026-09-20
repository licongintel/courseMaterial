import random
import interestDataEnsemble
import classificationData
import tester
import ensemble

if __name__ == '__main__':
    data = interestDataEnsemble.InterestDataEnsemble("interest.acl94.txt")
    (x, y) = data.get_data()
    
    random.seed(0)
    training_data = classificationData.ClassificationData()
    test_data = classificationData.ClassificationData()
    for i in range(0, len(y)):
        if random.random() < 0.5:
            training_data.add_item(x[i], y[i])
        else:
            test_data.add_item(x[i], y[i])
    
    factory = ensemble.ClassifierFactory("Perceptron", margin = 10)
    classifier = ensemble.Ensemble(factory)
    t = tester.Tester(classifier)
    t.train_and_test(training_data, test_data)

    input("Press Enter to continue ...")

    factory = ensemble.ClassifierFactory("LogisticRegression", regularizer = 0.05, max_iteration = 1000)
    classifier = ensemble.Ensemble(factory)
    t = tester.Tester(classifier)
    t.train_and_test(training_data, test_data)



