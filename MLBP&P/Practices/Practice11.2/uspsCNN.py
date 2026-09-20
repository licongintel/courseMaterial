
import numpy
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D

from keras.layers import Dropout

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
if tf.test.gpu_device_name():
    print("Debug message: GPU may be used")

class USPSCNN(object):
    def __init__(self, max_epoch = 100, batch_size = 8):
        self.max_epoch = max_epoch
        self.batch_size = batch_size

    def convert_data(self, data):
        x = numpy.empty([data.get_data_size(),
                len(data.get_feature(0))])
        y = numpy.zeros(data.get_data_size())
        for i in range(0, data.get_data_size()):
            x[i] = data.get_feature(i)
            y[i] = int(data.get_label(i))
        return (x, y)

    def train(self, training_data):
        (x_train, y_train) = self.convert_data(training_data)
        scale = int(numpy.sqrt(len(x_train[0])))
        assert scale * scale == len(x_train[0])
        x_train = x_train.reshape(x_train.shape[0], scale,
                scale, 1)
        
        self.model = Sequential()
        self.model.add(Conv2D(32, kernel_size = (3, 3), 
                input_shape = (scale, scale, 1), 
                activation = tf.nn.relu))
        self.model.add(Conv2D(64, kernel_size = (3, 3), 
                activation = tf.nn.relu))
        
        self.model.add(MaxPooling2D(pool_size = (2, 2)))
        self.model.add(Flatten())
        self.model.add(Dense(128, activation = tf.nn.relu))
        
        self.model.add(Dropout(0.5))
        
        self.model.add(Dense(10, activation = tf.nn.softmax))

        self.model.compile(optimizer = 'Adadelta', 
                loss = 'sparse_categorical_crossentropy')
        self.model.fit(x = x_train, y = y_train, 
                epochs = self.max_epoch,
                batch_size = self.batch_size, 
                verbose = 1, max_queue_size = 1)
    
    def classify(self, test_sample):
        scale = int(numpy.sqrt(len(test_sample)))
        assert scale * scale == len(test_sample)
        test_sample = test_sample.reshape(1, scale, scale, 1)
        
        scores = self.model.predict(test_sample).flatten()
        max_score = -1
        result = -1
        for i in range(0, len(scores)):
            if max_score < scores[i]:
                max_score = scores[i]
                result = i 
        return str(result)

