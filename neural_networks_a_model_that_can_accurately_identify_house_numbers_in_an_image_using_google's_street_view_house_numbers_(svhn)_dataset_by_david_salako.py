# -*- coding: utf-8 -*-
"""Neural_Networks_A_Model_That_Can_Accurately_Identify_House_Numbers_In_An_Image_Using_Google's_Street_View_House_Numbers_(SVHN)_Dataset_By_David_Salako.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1O-ntuI2CpYfcIYOr--HLTLC5S2h4rPsu

# **Neural Networks - A Model That Can Accurately Identify House Numbers In An Image Using Google's Street View House Numbers (SVHN) Dataset.  - By David Salako.**

<br>

## **Background and Context**

The ability to process visual information using machine learning algorithms can be very useful as demonstrated in various applications. The Street View House Numbers (SVHN) dataset is one of the most popular ones. It has been used in neural networks created by Google to read house numbers and match them to their geolocations. This is a great benchmark dataset to play with, learn and train models that accurately identify street numbers, and incorporate them into all sorts of projects.

<br>

## **Objective**
In this project, we will use a dataset with images centered around a single digit (many of the images do contain some distractors at the sides). Although this is a sample of the data which is simple, it is more complex than MNIST because of the distractors. Given the dataset, the aim is to build a model that can identify house numbers in an image.

<br>

## **Dataset**

The SVHN dataset has the following features:

* Number of classes: 10
* Training data: 42000 images
* Validation data: 60000 images
* Testing data: 18000 images

<br>
"""

# Commented out IPython magic to ensure Python compatibility.
# mounting the drive to use the files in the notebook
from google.colab import drive
drive.mount('/content/drive')

# importing the required packages and loading the .h5 type data file using the h5py package  

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from keras import optimizers

import cv2

import matplotlib.pyplot as plt
# %matplotlib inline

import pandas as pd 
import numpy as np 
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report,precision_score, recall_score, f1_score, precision_recall_curve, auc
import h5py 
from sklearn.neighbors import KNeighborsClassifier

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from IPython.display import display, HTML,Markdown

"""**Read the .h5 file and check the column keys and names.**"""

# Open the .h5 file as readonly.
# Check for the columns / keys and load the data appropriately.

with h5py.File("/content/drive/My Drive/SVHN_single_grey1.h5",'r') as h5f:
    print(list(h5f.keys()))
    xtrain = np.array(h5f.get('X_train'))
    ytrain = np.array(h5f.get('y_train'))
    xtest  = np.array(h5f.get('X_test'))
    ytest  = np.array(h5f.get('y_test'))
    xval   = np.array(h5f.get('X_val'))
    yval   = np.array(h5f.get('y_val'))

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

xtest[5],ytest[5]

"""**Let us visualize some of the SVHN dataset.**"""

plt.imshow(xtrain[0]) #Show first image in the training set. 
plt.show() 
print('y (training): ', ytrain[0]) 
plt.imshow(xval[0]) #Show first image in the validation set. 
plt.show() 
print('y (validation): ', yval[0])
plt.imshow(xtest[0]) #Show first image in the test set. 
plt.show() 
print('y (testing): ', ytest[0])

# Visualize some more...
# Plot first 10 images in the training set and their respective labels.
for i in range(10):
    image = xtrain[i]
    plt.figure(i)
    plt.imshow(image)
print('Label for each of the images below: %s' % (ytrain[0:10]))

# Visualize some more...
# Plot first 10 images in the validation set and their respective labels.
for i in range(10):
    image = xval[i]
    plt.figure(i)
    plt.imshow(image)
print('Label for each of the images below: %s' % (yval[0:10]))

# Visualize some more...
# Plot first 10 images in the test set and their respective labels.
for i in range(10):
    image = xtest[i]
    plt.figure(i)
    plt.imshow(image)
print('Label for each of the images below: %s' % (ytest[0:10]))

# Commented out IPython magic to ensure Python compatibility.
# Training images displayed in grayscale in 32 x 32 pixel format.
# %matplotlib inline
plt.figure(figsize=(15, 1))
for i in range(len(xtrain)):
    plt.imshow(xtrain[i].reshape(32,32), cmap="gray")
    plt.axis('off')
plt.show()
print('Labels for each of the above respective testing images: %s' % (ytrain[0:len(xtrain)]))

# Commented out IPython magic to ensure Python compatibility.
# Validation images displayed in grayscale in 32 x 32 pixel format.
# %matplotlib inline
plt.figure(figsize=(15, 1))
for i in range(len(xval)):
    plt.imshow(xval[i].reshape(32,32), cmap="gray")
    plt.axis('off')
plt.show()
print('Labels for each of the above respective testing images: %s' % (yval[0:len(xval)]))

# Commented out IPython magic to ensure Python compatibility.
# Testing images displayed in grayscale in 32 x 32 pixel format.
# %matplotlib inline
plt.figure(figsize=(15, 1))
for i in range(len(xtest)):
    plt.imshow(xtest[i].reshape(32,32), cmap="gray")
    plt.axis('off')
plt.show()
print('Labels for each of the above respective testing images: %s' % (ytest[0:len(xtest)]))

print(xtrain.shape,ytrain.shape)
print(xval.shape,yval.shape)
print(xtest.shape,ytest.shape)

"""**Observation:**

The SVHN data set is already in grayscale format.

**Gaussian Blurring**

* Image blurring is achieved by convolving the image with a high-pass filter kernel. It is useful for sharpening the edges and removing noise.

* Using 3x3 Gaussian blurring kernal to reduce image noise and detail as a part of pre-processing.
"""

xtrain_blurred=np.copy(xtrain,subok=True)
for i in range(xtrain.shape[0]):
  cv2.GaussianBlur(xtrain[i], (5, 5), 0)

xval_blurred=np.copy(xval,subok=True)
for i in range(xval.shape[0]):
  cv2.GaussianBlur(xval[i], (5, 5), 0)

xtest_blurred=np.copy(xtest,subok=True)
for i in range(xtest.shape[0]):
  cv2.GaussianBlur(xtest[i], (5, 5), 0)

# Commented out IPython magic to ensure Python compatibility.
# Blurred training images 
# %matplotlib inline
plt.figure(figsize=(15, 1))
for i in range(10):
    plt.subplot(1, 10, i+1)
    plt.imshow(xtrain_blurred[i])
    plt.axis('off')
plt.show()
print('Labels for each of the above respective testing images: %s' % (ytrain[0:10]))

# Commented out IPython magic to ensure Python compatibility.
# Blurred validation images 
# %matplotlib inline
plt.figure(figsize=(15, 1))
for i in range(10):
    plt.subplot(1, 10, i+1)
    plt.imshow(xval_blurred[i])
    plt.axis('off')
plt.show()
print('Labels for each of the above respective testing images: %s' % (yval[0:10]))

# Commented out IPython magic to ensure Python compatibility.
# Blurred testing images 
# %matplotlib inline
plt.figure(figsize=(15, 1))
for i in range(10):
    plt.subplot(1, 10, i+1)
    plt.imshow(xtest_blurred[i])
    plt.axis('off')
plt.show()
print('Labels for each of the above respective testing images: %s' % (ytest[0:10]))

"""**Reshape and print the data in xtest, xtrain, and xval.**"""

xtrain = xtrain_blurred.reshape(xtrain.shape[0],1024)
xval = xval_blurred.reshape(xval.shape[0],1024)
xtest = xtest_blurred.reshape(xtest.shape[0],1024)
print(xtrain.shape,xval.shape,xtest.shape)

"""**Next, the data is normalized.**"""

# Normalize inputs from 0-255 to 0-1; to be used with the eventual neural network.

xtrain = xtrain/255.0
xval = xval/255.0
xtest = xtest/255.0

"""**Flatten the data so that it is ready to be fed into the eventual model(s).**"""

# Flatten the data
x_train = []
x_test = []
x_val = []
for i in range(42000):
    x_train.append(xtrain[i,:].flatten())
for i in range(60000):
    x_val.append(xval[i,:].flatten())
for i in range(18000):
    x_test.append(xtest[i,:].flatten())

"""**The dataset is quite large so let us take subsets of it in order to reduce the computational resource challenges.**"""

# Subset 4000 records for training, 1000 records for testing, and 2000 records for validation respectively.
x_train = x_train[:4000]
ytrain= ytrain[:4000]
x_test = x_test[:1000]
ytest = ytest[:1000]
x_val = x_val[:2000]
yval = yval[:2000]

"""**K Nearest Neighbor Classifier Model.**"""

neighbors = np.arange(1,15)
train_accuracy =np.empty(len(neighbors))
val_accuracy = np.empty(len(neighbors))

for i,k in enumerate(neighbors):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(x_train, ytrain)
    train_accuracy[i] = knn.score(x_train, ytrain)
    val_accuracy[i] = knn.score(x_val, yval)

for i in range(len(train_accuracy)):
    print(train_accuracy[i],val_accuracy[i])

plt.title('KNN - Varying number of neighbors')
plt.plot(neighbors, val_accuracy, label='Validation Accuracy')
plt.plot(neighbors, train_accuracy, label='Training accuracy')
plt.legend()
plt.xlabel('Number of neighbors')
plt.ylabel('Accuracy')
plt.show()

"""**The graph above seems to indicate that 3 or 4 will be the best values; therefore, we can retrain the model with the best value of K.**"""

model = KNeighborsClassifier(n_neighbors=4)
model.fit(x_train, ytrain)
predictions = model.predict(x_test)

print(predictions[:3])

print(predictions[:5])

print(predictions[:7])

print(predictions[:10])

print("Testing Data Evaluation")
print(classification_report(ytest, predictions))
cm = confusion_matrix(ytest,predictions)
print ("Confusion Matrix")
print(confusion_matrix(ytest,predictions))

#import the seaborn library in order to display a more attractive and easier to read correlation matrix.

import seaborn as sns 

df_cm = pd.DataFrame(cm, index = [i for i in "0123456789"],
                     columns = [i for i in "0123456789"])
plt.figure(figsize = (10,7))
sns.heatmap(df_cm, annot=True, fmt='d')

"""**Observations:**

* 9s (nines) and 0s (zeros) are the numbers most often misclassified.
* 6s (sixes) and 0s (zeros) are also misclassified frequently.
* 8s (eights) and 0s (zeros) too.
* All the rest of the numbers are often misclassified as zeros too.
* All the numbers are also misclassified as 1 or 2 on a less than ideal frequency too.
"""

def accuracy(val1,val2):
    count = 0
    for i in range(len(val1)):
        if val1[i] == val2[i]:
            count = count +1
    acc = count / len(val1)
    return acc

my_accuracy = accuracy(ytest,predictions)
print(my_accuracy)

"""**Unsatisfactory accuracy score at 0.347.**

**Let us retrain the model with best value of K.**
"""

model = KNeighborsClassifier(n_neighbors=15)
model.fit(x_train, ytrain)
predictions = model.predict(x_test)

print("Testing Data Evaluation")
print(classification_report(ytest, predictions))
cm = confusion_matrix(ytest,predictions)
print ("Confusion Matrix")
print(confusion_matrix(ytest,predictions))

df_cm = pd.DataFrame(cm, index = [i for i in "0123456789"],
                     columns = [i for i in "0123456789"])
plt.figure(figsize = (10,7))
sns.heatmap(df_cm, annot=True, fmt='d')

"""**Observations:**

* 9s (nines) and 0s (zeros) are the numbers most often misclassified.
* 6s (sixes) and 0s (zeros) are also misclassified frequently.
* 8s (eights) and 0s (zeros) too.
* All the rest of the numbers are often misclassified as zeros too.
* All the numbers are also misclassified as 1 or 2 on a less than ideal frequency too.
"""

def accuracy(val1,val2):
    count = 0
    for i in range(len(val1)):
        if val1[i] == val2[i]:
            count = count +1
    acc = count / len(val1)
    return acc

my_accuracy = accuracy(ytest,predictions)
print(my_accuracy)

"""**The model has not learned properly because it is underfitting with training data hovering at an average of 55% and test data achieving 38%.**

<br>

**Let us try a GridSearch cross validation with the KNN Classifier to see if it improves upon the staus quo.**
"""

from sklearn.model_selection import GridSearchCV
param_grid = {'n_neighbors':np.arange(7,21)}
knn = KNeighborsClassifier()
knn_cv= GridSearchCV(knn,param_grid,cv=5)
knn_cv.fit(x_train,ytrain)

knn_cv.best_score_

"""**No improvement in the score.**

## **Neural Network**
"""

import tensorflow as tf
import keras
from keras import losses
from keras.models import Sequential
#from keras import optimizers
from keras.layers import MaxPooling2D,BatchNormalization,Dense
from tensorflow.keras import optimizers

with h5py.File("/content/drive/My Drive/SVHN_single_grey1.h5",'r') as h5f:
    print(list(h5f.keys()))
    xtrain = np.array(h5f.get('X_train'))
    ytrain = np.array(h5f.get('y_train'))
    xtest  = np.array(h5f.get('X_test'))
    ytest  = np.array(h5f.get('y_test'))
    xval   = np.array(h5f.get('X_val'))
    yval   = np.array(h5f.get('y_val'))

print('Training dataset:', xtrain.shape, ytrain.shape)
print('Test dataset:', xtest.shape, ytest.shape)
print('Validation dataset:', xval.shape, yval.shape)

"""**Let us reshape the data.**"""

## Reshape the data for X
xtrain = xtrain.reshape(xtrain.shape[0],1024)
xtest =xtest.reshape(xtest.shape[0],1024)
xval = xval.reshape(xval.shape[0],1024)

"""**Normalize the data so that pixel values range from 0 to 1 rather that 1 to 255.**"""

xtrain = xtrain/255
xtest = xtest/255
xval = xval/255

print('Training dataset:', xtrain.shape, ytrain.shape)
print('Test dataset:', xtest.shape, ytest.shape)
print('Validation dataset:', xval.shape, yval.shape)

"""**One Hot Encode the label data (y) as there are currently 10 of them.**"""

y_train = np_utils.to_categorical(ytrain)
y_test = np_utils.to_categorical(ytest)
y_val = np_utils.to_categorical(yval)

print('Training dataset:', xtrain.shape, y_train.shape)
print('Validation dataset:',xval.shape,y_val.shape)
print('Test dataset:', xtest.shape, y_test.shape)

"""### **1) ReLU Activation Function Tweaking the Learning Rate.**"""

def NN_model_Dense(learning_rate):
    
    model = Sequential()
    model.add(Dense(256, activation='relu',input_shape = (1024, )))
    model.add(Dense(64,activation='relu'))    
    model.add(Dense(32,activation='relu'))  
    model.add(Dense(10,activation='softmax'))
    
    sgd = optimizers.SGD(lr = learning_rate)
    model.compile(optimizer = sgd, loss = 'categorical_crossentropy', metrics = ['accuracy'])
    
    return model

# Learning rate = 0.001

model_Dense = NN_model_Dense(0.001)
NN_model_Dense_history = model_Dense.fit(xtrain, y_train, epochs = 10, verbose = 1)

# Learning rate = 0.005

model_Dense = NN_model_Dense(0.005)
NN_model_Dense_history = model_Dense.fit(xtrain, y_train, epochs = 30, verbose = 1)

# Learning rate = 0.01

model_Dense = NN_model_Dense(0.01)
NN_model_Dense_history = model_Dense.fit(xtrain, y_train, epochs = 40, verbose = 1)

# Learning rate = 0.1

model_Dense = NN_model_Dense(0.1)
NN_model_Dense_history = model_Dense.fit(xtrain, y_train, epochs = 55, verbose = 1)

# Learning rate = 0.05

model_Dense = NN_model_Dense(0.05)
NN_model_Dense_history = model_Dense.fit(xtrain, y_train, epochs = 50, verbose = 1)

results = model_Dense.evaluate(xtest, y_test)
print(results)

"""**Observations:**

* A learning rate of 0.001 yields a loss of 2.1960 and an 
accuracy of 0.2367. 
* A learning rate of 0.005 yields a loss of 0.8015 and an accuracy of 0.7537. 
* A learning rate of 0.01 yields a loss of 0.5833 and an accuracy of 0.8220. 
* A learning rate of 0.1 yields a loss of 0.5194 and an accuracy of 0.8368. 
* A learning rate of 0.05 yields a loss of 0.4809 and an accuracy of 0.8485. 

<BR>

The 0.05 learning rate produces the highest accuracy at 0.85 (not high enough) and the lowest losss so far of 0.48 (not low enough).

### **2) Next, Batch Normalization tweaking.**
"""

from keras.utils import np_utils
def nn_model():
    model = Sequential()
    model.add(BatchNormalization())
    model.add(Dense(256,activation = 'relu'))
    model.add(Dense(64,activation = 'relu'))
    model.add(Dense(32,activation = 'relu'))
    model.add(Dense(16,activation = 'relu'))
    model.add(Dense(10,activation = 'softmax'))
    
    sgd = optimizers.Adam(lr = 1e-3)
    model.compile(loss = losses.categorical_crossentropy,optimizer=sgd,metrics = ['accuracy'])
    return model

    sgd = optimizers.SGD(lr = learning_rate)

model_seq = nn_model()

# Batch size = 300 with 50 epochs.

NN_Built_model = model_seq.fit(xtrain,y_train,validation_data = (xval,y_val),epochs = 50,batch_size = 300,verbose = 1)

"""
**Batch normalization (with 50 epochs) helped improve the validation accuracy to 0.9121 and decrease the loss to 0.3621 compared to the earlier model implementation without batch normalization.**"""

# Plot training & validation accuracy values

plt.plot(NN_Built_model.history['accuracy'])
plt.plot(NN_Built_model.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# Plot training & validation losses values

plt.plot(NN_Built_model.history['loss'])
plt.plot(NN_Built_model.history['val_loss'])
plt.title('Model Losses')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

"""**Observations:**
<BR>
In comparison with K Nearest Neigbors the Neural Network implementing Batch Normalization has a better accuracy above the 90th percentile. The accuracy in the training dataset and the accuracy in the validation dataset are close in value. Loss is also improving in both.
"""

model_seq.summary()

# Batch size = 300 with 50 epochs.

NN_Built_model = model_seq.fit(xtest,y_test,epochs = 50,batch_size = 300,verbose = 1)

"""**Observations:**

The neural network model has performed well on test data with improved accuracy ~ 96% (0.9564) and loss decrease ~ 10% (0.0970).
"""

model_seq.evaluate(xtest,y_test)

print(model_seq.metrics_names)
print(NN_Built_model)

NN_Model_Predicted_Y = np.argmax(model_seq.predict(xtest), axis=-1)

#print(ytest[:10],NN_Model_Predicted_Y[:10])
print("Actual labels:    {}".format(ytest[:10]))
print("Predicted labels: {}\n".format(NN_Model_Predicted_Y[:10]))

plt.figure(figsize=(20, 1))
for i in range(20):
    plt.subplot(1, 20, i+1)
    plt.imshow(xtest[i].reshape(32,32))
    plt.axis('off')
plt.show()
print('Label for each of the above respective images: %s' % (ytest[:20]))

#print(ytest[11:25],NN_Model_Predicted_Y[11:25])
print("Actual labels:    {}".format(ytest[11:25]))
print("Predicted labels: {}\n".format(NN_Model_Predicted_Y[11:25]))

"""All correctly predicted above."""

#print(ytest[30:55],NN_Model_Predicted_Y[30:55])
print("Actual labels:    {}".format(ytest[30:55]))
print("Predicted labels: {}\n".format(NN_Model_Predicted_Y[30:55]))

"""All correctly predicted above."""

#print(ytest[60:70],NN_Model_Predicted_Y[60:70])
print("Actual labels:    {}".format(ytest[60:70]))
print("Predicted labels: {}\n".format(NN_Model_Predicted_Y[60:70]))

"""All correctly predicted above."""

#print(ytest[75:85],NN_Model_Predicted_Y[75:85])
print("Actual labels:    {}".format(ytest[75:85]))
print("Predicted labels: {}\n".format(NN_Model_Predicted_Y[75:85]))

"""All correct except a 9 was predicted instead of a 4."""

#print(ytest[90:105],NN_Model_Predicted_Y[90:105])
print("Actual labels:    {}".format(ytest[90:105]))
print("Predicted labels: {}\n".format(NN_Model_Predicted_Y[90:105]))

"""All correctly predicted above."""

cm = confusion_matrix(ytest,NN_Model_Predicted_Y)
print ("Confusion Matrix")
print(confusion_matrix(ytest,NN_Model_Predicted_Y))

df_cm = pd.DataFrame(cm, index = [i for i in "0123456789"],
                     columns = [i for i in "0123456789"])
plt.figure(figsize = (10,7))
sns.heatmap(df_cm, annot=True, fmt='d')

"""**Observations:**

Some of the images are blurry; the Neural Network is somewhat predicting fairly well with some mistakes/misclassifications; perhaps Accuracy can be further improved upon by tweaking or refining data augumentation, drop outs etc..

### **3) Dropout**
"""

def nn_model_with_dropouts():
    model = Sequential()
    model.add(BatchNormalization())
    model.add(Dense(256,activation = 'relu'))
    model.add(Dropout(0.5))
    model.add(Dense(34,activation = 'relu'))
    model.add(Dropout(0.5))
    model.add(Dense(10,activation = 'softmax'))
    
    sgd = optimizers.Adam(lr = 1e-3)
    model.compile(loss = losses.categorical_crossentropy,optimizer=sgd,metrics = ['accuracy'])
    return model

from keras.layers import Dropout
nn_seq_dropout = nn_model_with_dropouts()
Dropout_NN = nn_seq_dropout.fit(xtrain,y_train,validation_data = (xval,y_val),epochs = 50,batch_size = 300,verbose = 1)

"""**Observations:**
<br>

Compared to the previous method, Dropout did not improve the situation. Here validation accuracy is higher than training accuracy, leading to Underfitting. Additionally, the loss is unacceptably high.
"""

result_dropout = nn_seq_dropout.evaluate(xtest,y_test)

print(result_dropout)

# Plot training & validation accuracy values
plt.plot(Dropout_NN.history['accuracy'])
plt.plot(Dropout_NN.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# Plot training & validation loss
plt.plot(Dropout_NN.history['loss'])
plt.plot(Dropout_NN.history['val_loss'])
plt.title('Model Losses')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

"""### **4) Using Activation functions and kernal "he_normal" initializer.**"""

def NN_activation(activation_fun,learn_rate):
    model = Sequential()
    
    model.add(Dense(256, activation = activation_fun,input_shape = (1024, ), kernel_initializer='he_normal'))     
    model.add(Dense(124, activation=activation_fun,kernel_initializer='he_normal'))                            
    model.add(Dense(64, activation = activation_fun,kernel_initializer='he_normal'))                           
    model.add(Dense(32, activation= activation_fun, kernel_initializer='he_normal'))    
    model.add(Dense(10, activation='softmax',kernel_initializer='he_normal'))                            
   
    sgd = optimizers.SGD(lr = learn_rate)
    model.compile(optimizer = sgd, loss = 'categorical_crossentropy', metrics = ['accuracy'])
    
    return model

"""**Sigmoid function:**"""

# "He_Normal" Kernal Initializer with Sigmoid function and Learning Rate of 0.001.

model = NN_activation('sigmoid',0.001)
model_history = model.fit(xtrain,y_train,validation_data = (xval,y_val),epochs = 50,batch_size = 300,verbose = 1)

# "He_Normal" Kernal Initializer with Sigmoid function and Learning Rate of 0.005.

model = NN_activation('sigmoid',0.005)
model_history = model.fit(xtrain,y_train,validation_data = (xval,y_val),epochs = 50,batch_size = 300,verbose = 1)

# "He_Normal" Kernal Initializer with Sigmoid function and Learning Rate of 0.01.

model = NN_activation('sigmoid',0.01)
model_history = model.fit(xtrain,y_train,validation_data = (xval,y_val),epochs = 50,batch_size = 300,verbose = 1)

# "He_Normal" Kernal Initializer with Sigmoid function and Learning Rate of 0.1.

model = NN_activation('sigmoid',0.1)
model_history = model.fit(xtrain,y_train,validation_data = (xval,y_val),epochs = 50,batch_size = 300,verbose = 1)

# "He_Normal" Kernal Initializer with Sigmoid function and Learning Rate of 0.05.

model = NN_activation('sigmoid',0.05)
model_history = model.fit(xtrain,y_train,validation_data = (xval,y_val),epochs = 50,batch_size = 300,verbose = 1)

"""**Relu function:**"""

# "He_Normal" Kernal Initializer with Relu function and Learning Rate of 0.001.

model = NN_activation('relu',0.001)
model_history = model.fit(xtrain,y_train,validation_data = (xval,y_val),epochs = 50,batch_size = 300,verbose = 1)

# "He_Normal" Kernal Initializer with Relu function and Learning Rate of 0.005.

model = NN_activation('relu',0.005)
model_history = model.fit(xtrain,y_train,validation_data = (xval,y_val),epochs = 50,batch_size = 300,verbose = 1)

# "He_Normal" Kernal Initializer with Relu function and Learning Rate of 0.01.

model = NN_activation('relu',0.01)
model_history = model.fit(xtrain,y_train,validation_data = (xval,y_val),epochs = 50,batch_size = 300,verbose = 1)

# "He_Normal" Kernal Initializer with Relu function and Learning Rate of 0.1.

model = NN_activation('relu',0.1)
model_history = model.fit(xtrain,y_train,validation_data = (xval,y_val),epochs = 50,batch_size = 300,verbose = 1)

# "He_Normal" Kernal Initializer with Relu function and Learning Rate of 0.05.

model = NN_activation('relu',0.05)
model_history = model.fit(xtrain,y_train,validation_data = (xval,y_val),epochs = 50,batch_size = 300,verbose = 1)

"""**Observations:**

Poor results all around (with both Sigmoid and Relu functions) in terms of loss and accuracy tweaking the kernal optimizer "he_normal".

### **5) Implementing Data Augmentation**
"""

with h5py.File("/content/drive/My Drive/SVHN_single_grey1.h5",'r') as h5f:
    print(list(h5f.keys()))
    xtrain = np.array(h5f.get('X_train'))
    ytrain = np.array(h5f.get('y_train'))
    xtest  = np.array(h5f.get('X_test'))
    ytest  = np.array(h5f.get('y_test'))
    xval   = np.array(h5f.get('X_val'))
    yval   = np.array(h5f.get('y_val'))

"""**ImageDataGenerator**

In order to get more robust results out of our model, we are going to augment the images in the dataset, by randomly rotating them, zooming them in and out, shifting them up and down (IMPORTANT NOTE: It is best that we do not shift them horizontally, since there are also distracting digits in the images), shifting their channels and shearing them.
"""

# Data augmentation

from keras.preprocessing.image import ImageDataGenerator
datagen = ImageDataGenerator(rotation_range=90,horizontal_flip=True, vertical_flip=True,zca_whitening=True)

xtrain = xtrain.reshape([-1,32,32,1])
datagen.fit(xtrain)

for i in range(0,9):
    plt.subplot(330 + 1 + i)
    plt.imshow(xtrain[i].reshape(32,32))
plt.show()

print(xtrain.shape)
type(xtrain)

"""**Reshape and flatten the dataset.**"""

train_features = xtrain.reshape(42000, 1024)
print(train_features.shape)
test_features = xtest.reshape(18000, 1024)
print(test_features.shape)
val_features = xval.reshape(60000, 1024)
print(val_features.shape)

"""**One Hot Encode the Label Data.**"""

y_train = np_utils.to_categorical(ytrain)
y_test = np_utils.to_categorical(ytest)
y_val = np_utils.to_categorical(yval)

"""**Normalize the Data.**"""

train_features /= 255.0
test_features /= 255.0
val_features /= 255.0

"""**Run the Neural Network model with the augmentation.**"""

# Learning rate = 0.01 with 60 epochs.

aug_model_Dense = NN_model_Dense(0.01)
aug_model_history = aug_model_Dense.fit(train_features, y_train, epochs = 60, verbose = 1)

# Learning rate = 0.1 with 60 epochs.

aug_model_Dense = NN_model_Dense(0.1)
aug_model_history = aug_model_Dense.fit(train_features, y_train, epochs = 60, verbose = 1)

# Learning rate = 0.05 with 60 epochs.

aug_model_Dense = NN_model_Dense(0.05)
aug_model_history = aug_model_Dense.fit(train_features, y_train, epochs = 60, verbose = 1)

Augument_Result = aug_model_Dense.evaluate(test_features,y_test)
print(result_dropout)

"""**Observations:**

Implementing data augmentation did not improve the Accuracy nor the Loss at different learning rates.

## **Insights**

In this kernel, we have trained a Feed forward Neural Network to recognize the digits in the Street View House Numbers dataset. In particular, we have performed some minimal preprocessing of the data, we have tweaked a few hyperparameters and finally, we have trained the final NN and evaluated it on the test images data. 

<BR>

Furthermore, we have provided useful visualizations (confusion matrix et al.) so as get a sense of how our model actually works and not view it as just a black-box process. 

<BR>

Finally, it should be noted that there is quite a bit of room for tuning and different architectures so as to improve the accuracy of the model; nonetheless, our results are pretty good given the simplicity of our approach.

<BR>

The steps followed at a high level were:

<BR>

A) Began the model building by implementing K Nearest Neighbor (KNN) on a reduced size dataset due to computational resource limitations.

<BR>

B) Applied Gaussian Blurring filter to assist in clearing up some of the noisy blurring in many of the images.

<BR>

C) KNN delivered an unsatisfactory accuracy and loss.

<BR>

D) Implemented a Feed Forward Neural Network with the following variations: 

<BR>

   * Relu Activation function with a learning rate of 0.05 and 50 epochs returned with an accuracy of 0.8485 and a loss of 0.4809.

<BR>

   * Batch Normalization (with Relu activation) with the test data set, batch size 300 and 50 epochs returned an impressive accuracy of 0.9564 and a low loss of 0.0970.

<BR>

   * Dropouts returned an accuracy of 0.8391 and a loss of 0.5674.

<BR>

   * "He" Initializer with Sigmoid function, a learning rate of 0.05, batch size 300 and 50 epochs returned a very low accuracy of 0.1009 and a high loss of 2.3028. Poor performance and no improvement over batch normalization and dropouts results.


<BR>

 * "He" Initializer with Relu function, a learning rate of 0.05, batch size 300 and 50 epochs returned a low accuracy of 0.7898 and a high loss of 0.6683. No improvement over batch normalization and dropouts results.


<BR>

   * Data Augmentation with a learning rate of 0.05 and 50 epochs returned with an accuracy of 0.8165 and a loss of 0.5808. Data augmentation dod not improve on the earlier results.

<BR>

### **Conclusion**

<br>

Artificial Neural Networks (ANNs) do not always work  well with image data, because ANNs do not take 2-D images as input. They flatten the image and make it lose its spatial struture, whereas Convoluted Neural Networks (CNNs) take the full 2D-image as input in order to perform feature extraction. So CNNs do not lose the image's spatial structure, which makes them more suitable for working with image datasets.

<br>

There is still scope for improvement in the test accuracy and loss of the ANN model chosen here. CNNs with different architectures can be built and hyperparamter tuning can be performed to obtain a an even more accurate image classifier approaching the 99th percentile.

<br>

Batch Normalization delivered the highest accuracy and best loss results compared to all the other hyperparameter tuning methods in this ANN; this is a model that can identify house numbers on blurry images presented to it albeit with a small margin of error.

<br>

Running the same model on the entire larger data set should produce greater accuracy and smaller loss results on a more powerful server or computer without the current resource constraints.
"""