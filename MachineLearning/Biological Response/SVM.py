# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 13:50:55 2015

@author: 3820104
"""

import numpy as np
from numpy import genfromtxt, savetxt
#import matplotlib.pyplot as plt
from sklearn import svm
#from sklearn import datasets
#from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
import re
###############################################################################

path = r'C:\Users\3820104\Documents\_python_data\Biological Response'
path = re.sub(r"\\","/",path)

dataset = np.genfromtxt(open(path+'/train.csv','r'), delimiter=',', dtype='f8')[1:]    
y = np.array([x[0] for x in dataset])
X = np.array([x[1:] for x in dataset])
offset = int(X.shape[0] * 0.9)
X_train, y_train = X[:offset], y[:offset]
X_test, y_test = X[offset:], y[offset:]
################################################################################
test = genfromtxt(open(path+'/test.csv','r'), delimiter=',', dtype='f8')[1:]
################################################################################
#clf = svm.SVC(kernel='linear', C=0.001)
#clf.fit(X_train,y_train) # features fit to labels
#mse = mean_squared_error(y_test, clf.predict(X_test))
#print("Linear MSE: %.4f" % mse)
################################################################################
#clf = svm.SVC(kernel='rbf', C=0.001)
#clf.fit(X_train,y_train) # features fit to labels
#mse = mean_squared_error(y_test, clf.predict(X_test))
#print("rbf MSE: %.4f" % mse)
################################################################################
################################################################################
# we create an instance of SVM and fit out data. We do not scale our
# data since we want to plot the support vectors
C = 0.0001  # SVM regularization parameter
svc = svm.SVC(kernel='linear', C=C).fit(X_train, y_train)
mse = mean_squared_error(y_test, svc.predict(X_test))
print("linear MSE: %.4f" % mse)
################################################################################
svc = svm.SVC(kernel='linear', C=C).fit(X, y)
predicted_probs = [[index + 1, x[1]] for index, x in enumerate(svc.predict(test))]
savetxt('SVM_linear_submission.csv', predicted_probs, delimiter=',', fmt='%d,%f', 
        header='MoleculeId,PredictedProbability', comments = '')
################################################################################
rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(X_train, y_train)
mse = mean_squared_error(y_test, rbf_svc.predict(X_test))
print("rbf MSE: %.4f" % mse)
################################################################################
svc = svm.SVC(kernel='rbf', C=C).fit(X, y)
predicted_probs = [[index + 1, x[1]] for index, x in enumerate(svc.predict(test))]
savetxt('SVM_rbf_submission.csv', predicted_probs, delimiter=',', fmt='%d,%f', 
        header='MoleculeId,PredictedProbability', comments = '')
################################################################################
poly_svc = svm.SVC(kernel='poly', degree=3, C=C).fit(X_train, y_train)
mse = mean_squared_error(y_test, poly_svc.predict(X_test))
print("poly MSE: %.4f" % mse)
################################################################################
svc = svm.SVC(kernel='poly', C=C).fit(X, y)
predicted_probs = [[index + 1, x[1]] for index, x in enumerate(svc.predict(test))]
savetxt('SVM_poly_submission.csv', predicted_probs, delimiter=',', fmt='%d,%f', 
        header='MoleculeId,PredictedProbability', comments = '')
################################################################################
lin_svc = svm.LinearSVC(C=C).fit(X_train, y_train)
mse = mean_squared_error(y_test, lin_svc.predict(X_test))
print("LinearSVC MSE: %.4f" % mse)
################################################################################
svc = svm.LinearSVC(C=C).fit(X, y)
predicted_probs = [[index + 1, x[1]] for index, x in enumerate(svc.predict(test))]
savetxt('LinearSVC_submission.csv', predicted_probs, delimiter=',', fmt='%d,%f', 
        header='MoleculeId,PredictedProbability', comments = '')
################################################################################
