# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 10:09:03 2015

@author: 3820104
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from matplotlib import style
style.use("ggplot")

#feattures
x = [1,5,1.5,8,1,9]
y = [2,8,1.8,8,0.6,11]

#plt.scatter(x,y)
#plt.show()

X = []
for i, j in zip(x,y):
    X.append([i, j])
X = np.array(X)

ymean = np.mean(y)
for i,ele in enumerate(y):
    if(y[i]>ymean):
        y[i] = 1
    else:
        y[i] = 0
        
clf = svm.SVC(kernel='linear', C=1.0)
clf.fit(X,y) # features fit to labels
print(clf.predict([0.58,0.76]))
print(clf.predict([10.58,10.76]))

#w = clf.coef_[0]
#print(w)
#
#a = -w[0] / w[1] #
#xx = np.linspace(np.min(x),np.max(x))
#yy = a * xx - clf.intercept_[0] / w[1]
#h0 = plt.plot(xx,yy, 'k-', label="non weighted div")
#plt.scatter(X[:,0], X[:,1], c=y)
#plt.show()