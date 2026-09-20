
class ClassificationData(object):
    
    def __init__(self):
        self.x = []
        self.y = []

    def add_item(self, feature, label):
        self.x.append(feature)
        self.y.append(label)

    def get_feature(self, index):
        return self.x[index]
  
    def get_label(self, index):
        return self.y[index]

    def get_data_size(self):
        return len(self.x)


