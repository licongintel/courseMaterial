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
                
            temp_x = self.quantify(self.merge(temp_x))

            self.x.append(temp_x)            
        f.close()

    def get_feature(self, index):
        return self.x[index]
  
    def get_label(self, index):
        return self.y[index]

    def get_data_size(self):
        return len(self.x)

    def quantify(self, data):
        for i in range(0, len(data)):
            if (data[i] > -0.999):
                data[i] = 1
            else:
                data[i] = -1
        return data

    def merge(self, data):
        new_data = [0] * 64
        for i in range(0, 8):
            for j in range(0, 8):
                new_value = data[i * 2 * 16 + j * 2] + \
                        data[i * 2 * 16 + j * 2 + 1] + \
                        data[i * 2 * 16 + 16 + j * 2] + \
                        data[i * 2 * 16 + 16 + j * 2 + 1]
                new_value /= 4
                new_data[i * 8 + j] = new_value
        return new_data
