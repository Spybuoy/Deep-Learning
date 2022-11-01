# -*- coding: utf-8 -*-
"""546_HW1_prob1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FalNOw_4EYG22KM4Za_l56Vfe5HiOv1S
"""

!pip install scikit-learn scikit-image

"""
importing files
"""
import matplotlib .pyplot as plt
import cv2
import random
import numpy as np
from sklearn.svm import SVC
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import plot_confusion_matrix
import pandas as pd
from skimage.filters import gabor_kernel , gabor

from sklearn.datasets import fetch_openml
from sklearn. model_selection import train_test_split
"""
downloading the dataset-3c
"""
ds = fetch_openml ('mnist_784', as_frame=False)
x, x_test , y, y_test = train_test_split (ds.data , ds.target ,test_size = 0.2, random_state=42)

"""splitting x"""

"""
creating matrices
"""
random_index=random.sample(range(x.shape[0]),10000)
x_new = x[random_index] 
y_new = y[random_index]
x_new = x_new.reshape((-1,28,28))
x_test = x_test.reshape((-1,28,28))
sub_image = np.zeros((x_new.shape[0],14*14))
for i,val in enumerate(x_new):
  sub_image[i] = cv2.resize(x_new[i],(14,14)).flatten()
x_train,x_val,y_train,y_val=train_test_split(sub_image,y_new,test_size=0.2,random_state=42)
sub_image_test = np.zeros((x_test.shape[0],14*14))
for i,val in enumerate(x_test):
  sub_image_test[i] = cv2.resize(x_test[i],(14,14)).flatten()
x_test=sub_image_test

"""
chekcing for data and resizing-3c
"""
a = x[0].reshape((28 ,28))
b = cv2.resize(a, (14 ,14))

"""
displaying data, resized data and labels for a single iteration-3c
"""
fig = plt.figure(figsize=(8,8))
fig.add_subplot(1, 2, 1)
plt.imshow(a)
fig.add_subplot(1, 2, 2)
plt.imshow(b)
print('value at same index = '+ str(y[0]))

"""
classification-3d
"""
clf = make_pipeline(StandardScaler(), SVC(C = 10, kernel = 'rbf', gamma=1e-6))
# clf = make_pipeline(StandardScaler(), SVC(C = 5000, kernel = 'rbf', gamma='scale'))
clf.fit(x_train,y_train)

temp = clf.score(x_train,y_train)
print("clf_x_train_y_train = "+str(temp))

temp = clf.score(x_val,y_val)
print("clf_x_val_y_val = "+str(temp))

temp = clf.score(x_test[:2000],y_test[:2000])
print("clf_x_test_y_test = "+str(temp))

"""
confusion matrix-3d
"""
matrix=plot_confusion_matrix(clf,x_test,y_test,cmap=plt.cm.Blues, colorbar = True)
matrix.ax_.set_title('Confusion matrix')
plt.show()

"""
Grid search - this takes a lot of time to execute-3g
"""
params = [{'C':[1,10,100,1000,5000], 'gamma':[1e-2,1e-3,1e-4,1e-5,1e-6], 'kernel':['rbf','poly']}]
clf = GridSearchCV(svm.SVC(), param_grid=params, scoring='accuracy')
clf.fit(x_train, y_train)

"""
displaying results of grid search-3g
"""
df = pd.DataFrame(clf.cv_results_)
df = df.sort_values(by=['mean_test_score'])
print(df.head(5))

#highest mean_test_score-3g
print(df.iloc[-1])

"""
creating matrices-3h
"""
xx_train=np.zeros([1000,196])
yy_train=np.zeros([1000,])
z=0
for i in range(0,10):
  lst=np.where(y_train==f'{i}')
  random_index=random.sample(list(lst[0]),100)
  xx_train[z:100+z]=x_train[random_index]
  yy_train[z:100+z]=y_train[random_index]
  z+=100

"""
Gabor functions - 3h,3j -  takes too long to run.
"""
from skimage.filters import gabor_kernel , gabor
import numpy as np
ig, axs = plt.subplots(1,36)
i=1
xx_new_train=np.zeros([1000,14*14*36])
for a in range(1000):
  l=0
  for theta in np.arange(0,np.pi,np.pi/4):
    for freq in np.arange(0.05,0.5,0.15):
      for bandwidth in np.arange(0.3,1,0.3):
        gk = gabor_kernel(frequency=freq, theta=theta, bandwidth=bandwidth)
        # convolve the input image with the kernel and get co-efficients109
        # we will use only the real part and throw away the imaginary110
        # part of the co-efficients111
        image = xx_train[a].reshape((14,14))
        coeff_real , _ = gabor(image, frequency=freq, theta=theta,bandwidth=bandwidth)
        i+=1
        xx_new_train[a,l:l+196]=coeff_real.flatten()
        l+=196