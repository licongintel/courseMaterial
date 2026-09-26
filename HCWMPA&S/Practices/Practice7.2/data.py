import numpy

class USPSData:
    def __init__(self):
        self.x = None
        self.y = []

    def read_file(self, filename):
        f = open(filename, "r")
        self.total = int(f.readline())
        self.x = numpy.zeros((self.total, 256), dtype=numpy.float32)
        for i in range(self.total):
            label = int(f.readline())
            self.y.append(label)
            self.x[i] = numpy.fromstring(f.readline(), dtype=numpy.float32, sep=" ")            
        f.close()

def read_data(filename):
    data = USPSData()
    data.read_file(filename)
    return data

