# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 10:13:12 2015

@author: 3820104
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from numpy import genfromtxt, savetxt
import re
#import scipy as sp
import numpy as np
import logloss


path = r'C:\Users\3820104\Documents\_python_data\Biological Response'
path = re.sub(r"\\","/",path)


def rfc():
    #create the training & test sets, skipping the header row with [1:]
    dataset = genfromtxt(open(path+'/train.csv','r'), delimiter=',', dtype='f8')[1:]    
    target = [x[0] for x in dataset]
    train = [x[1:] for x in dataset]
    test = genfromtxt(open(path+'/test.csv','r'), delimiter=',', dtype='f8')[1:]

    #create and train the random forest
    #multi-core CPUs can use: rf = RandomForestClassifier(n_estimators=100, n_jobs=2)
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(train, target)
    y_test = rf.predict_proba(test)
    predicted_probs = [[index + 1, x[1]] for index, x in enumerate(y_test)]
    savetxt('RFC_submission.csv', predicted_probs, delimiter=',', fmt='%d,%f', 
            header='MoleculeId,PredictedProbability', comments = '')

def rfc_cv():
    #read in  data, parse into training and target sets
    dataset = np.genfromtxt(open(path+'/train.csv','r'), delimiter=',', dtype='f8')[1:]    
    target = np.array([x[0] for x in dataset])
    train = np.array([x[1:] for x in dataset])

    #In this case we'll use a random forest, but this could be any classifier
    cfr = RandomForestClassifier(n_estimators=100)

    #Simple K-Fold cross validation. 5 folds.
    cv = cross_validation.KFold(len(train), n_folds=5)#, indices=False)

    #iterate through the training and test cross validation segments and
    #run the classifier on each one, aggregating the results into a list
    results = []
    for traincv, testcv in cv:
        probas = cfr.fit(train[traincv], target[traincv]).predict_proba(train[testcv])
        results.append( logloss.llfun(target[testcv], [x[1] for x in probas]) )

    #print out the mean of the cross-validated results
    print "RFC KFold Results MSE: " + str( np.array(results).mean() )
    #RFC KFold Results MSE: 0.468030772657

    
if __name__=="__main__":
    rfc()
    rfc_cv()