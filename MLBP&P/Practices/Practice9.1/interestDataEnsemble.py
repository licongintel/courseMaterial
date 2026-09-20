
import re

import numpy

class InterestDataEnsemble(object):
    
    def __init__(self, filename):
        sizes = [1000, 1, 3, 5, 7]
        self.x = []
        self.y = []
        self.build_dict(filename)
        f = open(filename, "r")
        for line in f:
            if line != "$$\n":
                
                ensembles = []
                for size in sizes:
                    (features, label) = self.\
                            convert_features_and_label(
                            line, size)
                    ensembles.append(numpy.array(features))
                self.x.append(ensembles)
                self.y.append(label)
        f.close()

    def match_label(self, item):
        if re.search("interests?_\d", item):
            label = re.match("interests?_\d", item).group(0)
            label = re.sub("interests?_", "", label)
            return label
        return None

    def get_items_and_label(self, line):
        line = line.replace("=", "")
        line = line.replace("[ ", "")
        line = line.replace(" ]", "")
        tmp_items = line.split()
        items = []
        label = None
        index = -1
        for i in range(0, len(tmp_items)):
            tmp_label = self.match_label(tmp_items[i])
            if tmp_label != None:
                label = tmp_label
                index = i
            else:
                items.append(tmp_items[i])
        return (items, label, index)

    def build_dict(self, filename):
        self.dict = {}
        index = 0
        f = open(filename, "r")
        for line in f:
            if line != "$$\n":
                (items, label, temp) = self.\
                        get_items_and_label(line)
                for item in items:
                    if item not in self.dict:
                        self.dict[item] = index
                        index += 1
        f.close()

    def convert_features_and_label(self, line, size):
        (items, label, index) = self.\
                get_items_and_label(line)
        left = index - size
        if left < 0:
            left = 0
        right = index + size
        if right > len(items):
            right = len(items)

        features = [0] * len(self.dict)
        for i in range(left, right):
            if items[i] in self.dict:
                features[self.dict[items[i]]] = 1
        return (features, label)

    def get_data(self):
        return (self.x, self.y)
