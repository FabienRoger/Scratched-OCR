import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.losses import MSE
import matplotlib.pyplot as plt

from constants import *

class DataCreator:
    
    
    def simple_train_generators(self, batch_size = 32):
        
        return self._get_generator('damagedtrain', batchsize=batch_size),\
               self._get_generator('damagedval', batchsize=batch_size) 
    
    def simple_predict_generator(self):
        return self._get_generator('damagedtest', batchsize=1)
    
    def io_train_generators(self, batch_size = 32):
        train_in = self._get_generator('damagedtrain', batchsize=batch_size)
        train_out = self._get_generator('origintrain', batchsize=batch_size)
        val_in = self._get_generator('damagedval', batchsize=batch_size)
        val_out = self._get_generator('originval', batchsize=batch_size)
        
        train_io = self._merge_io_generator(train_in, train_out)
        val_io = self._merge_io_generator(val_in, val_out)
        
        return train_io, val_io
    
    def io_predict_generator(self, batch_size = 32):
        test_in = self._get_generator('damagedtest', batchsize=1)
        test_out = self._get_generator('origintest', batchsize=1)
        
        test_io = self._merge_io_generator(test_in, test_out)
        
        return test_io   
    
    def _get_generator(self, directory, batchsize = 32):
        print('get gen '+directory)
        datagen = ImageDataGenerator(preprocessing_function=preprocess_input, dtype='float16')    
        generator = datagen.flow_from_directory(
            directory= directory+'/',
            target_size=(IMG_SIZE, IMG_SIZE),
            color_mode="grayscale",
            shuffle = True,
            class_mode='categorical',
            batch_size=batchsize,
            seed = 1)
        return generator
    
    #Some common seed between both generators is required for the merger to work properly
    def _merge_io_generator(self, ingen, outgen):
        while True:
            x = ingen.next()[0]
            y = outgen.next()[0]
            yield x, y