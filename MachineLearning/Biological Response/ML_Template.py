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
from sklearn.externals import joblib
import re
import logloss

###############################################################################

def saveModel(filename,clf,params):
    for key in params:
        filename += "_"+key+"_"+str(params[key])
    filename += ".pkl"
    print "writing to: " + filename
    stuff = joblib.dump(clf, filename, compress=9)
    print stuff
    """
    Later you can load back the pickled model (possibly in another Python process) with:
    >>> clf = joblib.load('filename.pkl') 
    """
    
def loadTrainingData(filename): 
    try:
        dataset = np.genfromtxt(open(filename,'r'), delimiter=',', dtype='f8')[1:]    
        y = np.array([x[0] for x in dataset])
        X = np.array([x[1:] for x in dataset])
    except:
         X,y = [],[]       
    return X,y

def splitTrainingData(X,y, split=0.9): 
    try:
        offset = int(X.shape[0] * split)
        X_train, y_train = X[:offset], y[:offset]
        X_test, y_test = X[offset:], y[offset:]
    except:
         X_train, y_train, X_test, y_test = [],[],[],[]        
    return X_train, y_train, X_test, y_test

def loadTestData(filename):
    try:
        return genfromtxt(open(filename,'r'), delimiter=',', dtype='f8')[1:]
    except:
        return []
        
def testClf(clf,X,y,split=0.9):
    X_train,y_train,X_test,y_test = splitTrainingData(X,y,split)
    clf.fit(X_train, y_train)
    mse = mean_squared_error(y_test, clf.predict(X_test))
    print("Training Learning Set MSE(%d): %.4f" % split, mse)
    return clf
    
def submitClf(clf, X, y, filename):
    print("Fitting regression model using full dataset")
    clf.fit(X, y)
    y_test = clf.predict(X_test)
    predicted_probs = [[index + 1, x] for index, x in enumerate(y_test)]
    savetxt('GBR_full_submission.csv', predicted_probs, delimiter=',', fmt='%d,%f', 
            header='MoleculeId,PredictedProbability', comments = '')
    return clf   

def kfoldTest(clf,X,y,folds=5):
    print("Fit regression model using KFold datasets")
    cv = cross_validation.KFold(len(y), n_folds=folds)#, indices=False)

    #iterate through the training and test cross validation segments and
    #run the classifier on each one, aggregating the results into a list
    results = []
    for traincv, testcv in cv:
        probas = clf.fit(X[traincv], y[traincv]).predict(X[testcv])
        results.append( logloss.llfun(y[testcv], [x[1] for x in probas]) )
    
    #print out the mean of the cross-validated results
    print "GBR KFold Learning Sets MSE: " + str( np.array(results).mean() )
#########################################################################
path = r'C:\Users\3820104\Documents\_python_data\Biological Response'
path = re.sub(r"\\","/",path)

X,y = loadTrainingData(path+'/train.csv')
X_test = loadTestData(path+'/test.csv')  

params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 1,
          'learning_rate': 0.01, 'loss': 'ls'}
clf = ensemble.GradientBoostingRegressor(**params)

clf = testClf(clf,X,y)
saveModel("GBR_split",clf,params)

clf = submitClf(clf, X, y)
saveModel("GBR_full",clf,params)

kfoldTest(clf,X,y,10)
###############################################################################
