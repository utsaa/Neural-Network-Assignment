# -*- coding: utf-8 -*-
"""Neural_Net_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X99v1P7ISEk-sQV1YpAE0np38YloHzDL
"""

# Defining the necessary libraries
from matplotlib import pyplot as plt
import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from keras.utils import np_utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Flatten, Conv2D, Activation, MaxPooling2D
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import get_custom_objects

# Defining the class NetA which computes the neural network for a linear activation function
class NetA(object):
  def __init__(self, numclass=10):
    self.numclass=numclass
    self.train_test()
    self.hist=0
# Defining a method for loading the CIFAR10 data. 
  def train_test(self):
    (X_train,Y_train),(X_test,Y_test)=cifar10.load_data()
    x_train=X_train.astype('float32')/255
    x_test=X_test.astype('float32')/255
    num_class=self.numclass
    y_train=np_utils.to_categorical(Y_train,num_classes=num_class)
    y_test=np_utils.to_categorical(Y_test,num_classes=num_class)

    self.x_test=x_test
    self.y_test=y_test

    self.x_train=x_train
    self.y_train=y_train
# This method computes the test and train accuracies and losses
  def history(self, lr=0.001, mom=0.9,batch_size=64,epochs=50):
    lf=lambda x: 1*x
    get_custom_objects().update({'lf':lf})
    model=Sequential()
    model.add(Flatten())
    model.add(Dense(self.numclass,activation='lf'))
    opt=SGD(learning_rate=lr, momentum=mom)
    model.compile(optimizer=opt, loss='categorical_crossentropy',metrics=['accuracy'])
    history=model.fit(self.x_train,self.y_train, batch_size=batch_size,epochs=epochs,validation_data=(self.x_test,self.y_test))
    self.hist= history
# This method returns the history if asked by the user.
# If the history method is not computed before, it computes the history using default values of parameters.
  def plot_history(self, comput_acc=True):
    if  comput_acc and self.hist:
      return self.hist
    elif comput_acc:
      self.history(lr=0.001, mom=0.9,batch_size=64,epochs=50)
      return self.hist

class NetB(NetA):
  def __init__(self,numclass=10 ):
    # The NetA class is inherited to load the test and train data
    NetA.__init__(self,numclass=10)
# This method computes the test and train accuracies and losses
  def history(self, lr=0.001, mom=0.9,batch_size=64,epochs=50):
    model=Sequential()
    model.add(Flatten())
    model.add(Dense(300, activation='relu'))
    model.add(Dense(10,activation='softmax'))
    opt=SGD(learning_rate=lr, momentum=mom)
    model.compile(optimizer=opt, loss='categorical_crossentropy',metrics=['accuracy'])
    history=model.fit(self.x_train,self.y_train, batch_size=64,epochs=50,validation_data=(self.x_test,self.y_test))
    self.hist= history
# This method returns the history if asked by the user.
# If the history method is not computed before, it computes the history using default values of parameters.
  def plot_history(self, comput_acc=True):
    if  comput_acc and self.hist:
      return self.hist
    elif comput_acc:
      self.history( lr=0.001, mom=0.9,batch_size=64,epochs=50)
      return self.hist

class NetC(NetA):
  def __init__(self,numclass=10 ):
    # The NetA class is inherited to load the test and train data
    NetA.__init__(self,numclass=10)

# This method computes the test and train accuracies and losses
# Here 25 nodes are used as a default value for the last hidden layer, as with increase in nodes, the data was seen to be overfitting.
  def history(self, lr=0.001, mom=0.9,batch_size=64,epochs=50, neurons=25):
    model=Sequential()
    model.add(Conv2D(25,2, activation='relu',kernel_initializer='he_uniform',padding='valid'))
    model.add(MaxPooling2D(pool_size=2,strides=2))
    model.add(Flatten())
    model.add(Dense(neurons, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(10, activation='softmax'))
    opt=SGD(learning_rate=0.001, momentum=.9)
    model.compile(optimizer=opt, loss='categorical_crossentropy',metrics=['accuracy'])
    history=model.fit(self.x_train,self.y_train, batch_size=64,epochs=50,validation_data=(self.x_test,self.y_test))
    self.hist= history
# This method returns the history if asked by the user.
# If the history method is not computed before, it computes the history using default values of parameters.
  def plot_history(self, comput_acc=True):
    if  comput_acc and self.hist:
      return self.hist
    elif comput_acc:
      self.history( lr=0.001, mom=0.9,batch_size=64,epochs=50, neurons=25)
      return self.hist

# As defined in the question, this function plots the raining and test accuracy
def plot_history(histories):
  for i in range(len(histories)):
    plt.figure(i+1, figsize=(10,10))
    plt.plot(histories[i]['train_accs'], label='Train')
    plt.plot(histories[i]['test_accs'], label='Test')
    plt.legend()
    plt.title('Accuracy plot for '+histories[i]['name'])
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
  plt.show()

# The different objects are created in a list
nets=[NetA(), NetB()]
histories=[] 
NUM_EPOCHS=50
LEARNING_RATE=0.001
COMPUTE_ACCS=True
for net in nets:
  net_name=type(net).__name__
  print(f'=== Training {net_name} ===')
  net.history(lr=LEARNING_RATE,epochs=NUM_EPOCHS)
  history=net.plot_history(comput_acc=COMPUTE_ACCS).history
  histories.append({'name': net_name, 'net': net, 'train_accs':history['accuracy'], 'test_accs': history['val_accuracy']})

# A new block is required to made as the code was crashing while writing on the same block due to RAM memory.
net= NetC()
net_name=type(net).__name__
print(f'=== Training {net_name} ===')
net.history(lr=LEARNING_RATE,epochs=NUM_EPOCHS)
history=net.plot_history(comput_acc=COMPUTE_ACCS).history
histories.append({'name': net_name, 'net': net, 'train_accs':history['accuracy'], 'test_accs': history['val_accuracy']})

plot_history(histories) # For the same reason the plotting is done in different block

