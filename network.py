import numpy as np
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Conv2D, MaxPool2D, ReLU, Input, Flatten, Reshape
from tensorflow.keras import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy, CategoricalCrossentropy, MSE
from tensorflow.keras.models import Model
from tensorflow.keras import regularizers
import matplotlib.pyplot as plt

from constants import *

class Network:
    
    def __init__(self, net='simple',inner_nodes=50,f=16,ks=3, io_model = None,
                 name = 'nn1',learning_rate=0.0004, regularization = 0):
        self.name = name
        if net=='simple' or net=='advanced':
            X_input = None 
            if net=='simple':
                X_input = Input([IMG_SIZE,IMG_SIZE,IMG_CHANNELS])
                X = X_input
            else:
                X_input = io_model.input
                X = io_model.output
            X = Conv2D(f,ks)(X_input)
            X = MaxPool2D()(X)
            X = ReLU()(X)
            X = Flatten()(X)
            
            preds=Dense(26,activation='softmax', kernel_regularizer=regularizers.l2(regularization))(X)
            
            self.model=Model(inputs=X_input,outputs=preds)
            
            self.model.compile(optimizer=Adam(lr=learning_rate),
                               loss=CategoricalCrossentropy(from_logits=True),
                               metrics=['accuracy'])
        elif net=='io':
            X_input = Input([IMG_SIZE,IMG_SIZE,IMG_CHANNELS])
            X = Conv2D(f,ks, padding="same")(X_input)
            X = Conv2D(IMG_CHANNELS,ks, padding="same")(X_input)
            
            self.model=Model(inputs=X_input,outputs=X)
            self.model.compile(optimizer=Adam(lr=learning_rate),
                               loss=MSE,
                               metrics=['accuracy'])
        
    def train(self,train_generator,validation_generator,epochs,verbose = 1, step_size_train=5, step_size_val=1):
        step_size_train=303
        step_size_val=38        
        history = self.model.fit(train_generator,
                                 steps_per_epoch = step_size_train,
                                 validation_data = validation_generator, 
                                 validation_steps = step_size_val,
                                 epochs=epochs, verbose=verbose)   
        return history     
    
    def predict(self,pred_generator,labels=None,verbose = 1):
        step_size_pred=1
        
        pred=self.model.predict(pred_generator,
                                steps=step_size_pred,
                                verbose=verbose)
        if labels != None:
            predicted_class_indices=np.argmax(pred,axis=1)
            labels = dict((v,k) for k,v in (labels).items())
            predictions = [labels[k] for k in predicted_class_indices]
            filenames = pred_generator.filenames
            return [predictions, filenames]
        else:
            return pred
    
    def load(self, name = None):
        if name == None:name = self.name
        self.model.load_weights('models/weights of '+name+'.nn')
    
    def save(self, name = None):
        if name == None:name = self.name
        self.model.save_weights('models/weights of '+name+'.nn')
    
    def plot_learning_curves(self,history):
        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']
        
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        
        plt.figure(figsize=(8, 8))
        plt.subplot(2, 1, 1)
        plt.plot(acc, label='Training Accuracy')
        plt.plot(val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.ylabel('Accuracy')
        plt.ylim([min(plt.ylim()),1])
        plt.title('Training and Validation Accuracy')
        
        plt.subplot(2, 1, 2)
        plt.plot(loss, label='Training Loss')
        plt.plot(val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.ylabel('Cross Entropy')
        plt.ylim([min(plt.ylim()),max(plt.ylim())])
        plt.title('Training and Validation Loss')
        plt.xlabel('epoch')
        plt.show()    