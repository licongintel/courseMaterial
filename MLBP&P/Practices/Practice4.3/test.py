
import random
import interestData
import classificationData
import nearestNeighbor
import tester

if __name__ == '__main__':
    data = interestData.InterestData("interest.acl94.txt")
    (x, y) = data.get_data()
    
    random.seed(0)
    training_data = classificationData.ClassificationData()
    test_data = classificationData.ClassificationData()
    for i in range(0, len(y)):
        if random.random() < 0.5:
            training_data.add_item(x[i], y[i])
        else:
            test_data.add_item(x[i], y[i])
            
    classifier = nearestNeighbor.NearestNeighbor()
    tester = tester.Tester(classifier)
    tester.train_and_test(training_data, test_data)




