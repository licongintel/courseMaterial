class USPSData(object):
    
    def __init__(self, filename):
        self.y = []
        self.x = []
        f = open(filename, "r")
        for line in f:
            items = line.split()
            label = str(int(items[0]) - 1)
            self.y.append(label)
            temp_x = [0] * 256
            for i in range(1, len(items)):
                (index, value) = items[i].split(":")
                temp_x[int(index) - 1] = float(value)
            self.x.append(temp_x)
        f.close()

    def get_feature(self, index):
        return self.x[index]
  
    def get_label(self, index):
        return self.y[index]

    def get_data_size(self):
        return len(self.x)
