
import re

import numpy

class InterestData(object):
    
    def __init__(self, filename, dimension = 0):
        self.dimension = dimension
        
        self.x = []
        self.y = []
        self.read_dict(filename)
        f = open(filename, "r")
        for line in f:
            if line != "$$\n":
                (features, label) = \
                           self.convert_features_and_label(line)
                self.x.append(numpy.array(features))
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
        for item in tmp_items:
            tmp_label = self.match_label(item)
            if tmp_label == None:
                items.append(item)
            else:
                label = tmp_label
        return (items, label)

    def read_dict(self, filename):
        self.dict = {}
        f = open("myst_dict.txt", "r")
        for line in f:
            (item, index) = line.split()
            index = int(index)
            if self.dimension == 0 or index < self.dimension:
                self.dict[item] = index
        f.close()

    def convert_features_and_label(self, line):
        (items, label) = self.get_items_and_label(line)
        features = [0] * len(self.dict)
        for item in items:
            if item in self.dict:
                features[self.dict[item]] = 1
        return (features, label)

    def get_data(self):
        return (self.x, self.y)
