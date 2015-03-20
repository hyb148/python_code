# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:08:49 2015

@author: 3820104
"""
#http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3885826/
#http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier
import numpy as np
from numpy import genfromtxt, savetxt
#import matplotlib.pyplot as plt

from sklearn import ensemble
#from sklearn import datasets
#from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from sklearn import cross_validation
import re
import logloss

###############################################################################
path = r'C:\Users\3820104\Documents\_python_data\Biological Response'
path = re.sub(r"\\","/",path)

dataset = np.genfromtxt(open(path+'/train.csv','r'), delimiter=',', dtype='f8')[1:]    
y = np.array([x[0] for x in dataset])
X = np.array([x[1:] for x in dataset])
offset = int(X.shape[0] * 0.9)
X_train, y_train = X[:offset], y[:offset]
X_test, y_test = X[offset:], y[offset:]
###############################################################################
test = genfromtxt(open(path+'/test.csv','r'), delimiter=',', dtype='f8')[1:]
###############################################################################
print("Fit regression model using full dataset")
params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 1,
          'learning_rate': 0.01, 'loss': 'ls'}
clf = ensemble.GradientBoostingRegressor(**params)

#clf.fit(X_train, y_train)
#mse = mean_squared_error(y_test, clf.predict(X_test))
#print("Full Learning Set MSE: %.4f" % mse)
#
##############################################################################
clf.fit(X, y)
y_test = clf.predict(test)
predicted_probs = [[index + 1, x] for index, x in enumerate(y_test)]
savetxt('GBR_full_submission.csv', predicted_probs, delimiter=',', fmt='%d,%f', 
        header='MoleculeId,PredictedProbability', comments = '')
###############################################################################
print("Fit regression model using KFold datasets")
cv = cross_validation.KFold(len(y), n_folds=5)#, indices=False)

#iterate through the training and test cross validation segments and
#run the classifier on each one, aggregating the results into a list
results = []
for traincv, testcv in cv:
    probas = clf.fit(X[traincv], y[traincv]).predict(X[testcv])
    results.append( logloss.llfun(y[testcv], [x[1] for x in probas]) )

#print out the mean of the cross-validated results
print "GBR KFold Learning Sets MSE: " + str( np.array(results).mean() )
