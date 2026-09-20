from perceptron import Perceptron
from logisticRegression import LogisticRegression
import classificationData

class ClassifierFactory(object):
    def __init__(self, name, max_iteration = 100, 
            margin = 0, regularizer = 0.0001, 
            tolerance = 0.0001, learning_rate = 10):
        self.name = name
        self.max_iteration = max_iteration
        self.margin = margin
        self.regularizer = regularizer
        self.tolerance = tolerance
        self.learning_rate = learning_rate

    def get_classifier(self):
        if self.name == "Perceptron":
            classifier = Perceptron(
                    max_iteration = self.max_iteration,
                    margin = self.margin)
        if self.name == "LogisticRegression":
            classifier = LogisticRegression(
                    regularizer = self.regularizer,
                    tolerance = self.tolerance,
                    max_iteration = self.max_iteration,
                    learning_rate = self.learning_rate)
        return classifier

class Ensemble(object):
    def __init__(self, factory):
        self.factory = factory

    def train(self, training_data):
        classifier_number = len(training_data.get_feature(0))
        self.classifiers = []
        for i in range(0, classifier_number):
            classifier = self.factory.get_classifier()
            
            data = classificationData.ClassificationData()
            for j in range(0, training_data.get_data_size()):
                data.add_item(training_data.get_feature(j)[i],
                        training_data.get_label(j))
            print("Ensemble instance " + str(i))
            classifier.train(data)
            self.classifiers.append(classifier)

    def classify(self, test_sample):
        scores = {}
        for i in range(0, len(self.classifiers)):
            results = self.classifiers[i].score_all(
                    test_sample[i])
            for label in results.keys():
                if label not in scores:
                    scores[label] = 0
                scores[label] += results[label]
                
        best_score = -10000000000000
        result = None
        for label in scores.keys():
            if best_score < scores[label]:
                best_score = scores[label]
                result = label
        return result
