
import uspsData
import plotter

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("index", type = int,
            help = "index of the data sample")
    parser.add_argument("-f", "--filename", type = str,
            default = "usps", help = "data file (default: usps)")
    args = parser.parse_args()
    index = args.index
    filename = args.filename
    
    data = uspsData.USPSData(filename)
    plotter = plotter.Plotter(data.get_label(index),
            data.get_feature(index))

