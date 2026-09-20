
import re

import numpy

class InterestData(object):
    
    def __init__(self, filename):
        self.x = []
        self.y = []
        self.build_dict(filename)
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

    def build_dict(self, filename):
        self.dict = {}
        
        index = 0
        f = open(filename, "r")
        for line in f:
            if line != "$$\n":
                (items, label) = self.get_items_and_label(line)
                for item in items:
                    if item not in self.dict:
                        self.dict[item] = index
                        index += 1
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
