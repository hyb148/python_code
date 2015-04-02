# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:08:49 2015

@author: 3820104
"""
#http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3885826/
#http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier
#http://kukuruku.co/hub/python/introduction-to-machine-learning-with-python-andscikit-learn
import numpy as np
from numpy import genfromtxt, savetxt
#import matplotlib.pyplot as plt
from sklearn import ensemble
#from sklearn import datasets
#from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from sklearn import cross_validation
from sklearn.externals import joblib
#Data Normalization
from sklearn import preprocessing
#Elimination Algorithm that is also available in the Scikit-Learn library.
from sklearn.feature_selection import RFE
from sklearn import metrics
from sklearn.svm import SVC
#Optimize Algorithm Parameters
from sklearn.linear_model import Ridge
from sklearn.grid_search import GridSearchCV
#random parameter search
from scipy.stats import uniform as sp_rand
from sklearn.grid_search import RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression









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

def RecursiveFeatureElimination(X,y):
    model = LogisticRegression()
    # create the RFE model and select 3 attributes
    rfe = RFE(model, 3)
    rfe = rfe.fit(X, y)
    # summarize the selection of the attributes
    print(rfe.support_)
    print(rfe.ranking_)

def testGBR(X,y):
    params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 1,
              'learning_rate': 0.01, 'loss': 'ls'}
    clf = ensemble.GradientBoostingRegressor(**params)

    clf = testClf(clf,X,y)
    saveModel("GBR_split",clf,params)

    clf = submitClf(clf, X, y)
    saveModel("GBR_full",clf,params)

    kfoldTest(clf,X,y,10)

def testSVM(X,y):
    """
    Support Vector Machines
    SVM (Support Vector Machines) is one of the most
    popular machine learning algorithms used mainly for the classification
    problem. As well as logistic regression, SVM allows multi-class
    classification with the help of the one-vs-all method.
    """
    # fit a SVM model to the data
    model = SVC()
    model.fit(X, y)
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

def testGridSearchCV(X,y):
    """
    How to Optimize Algorithm Parameters
    One of the most difficult stages
    in creating really efficient algorithms is choosing correct parameters.
    It’s usually easier with experience, but one way or another, we have to
    do the search. Fortunately, Scikit-Learn provides many implemented
    functions for this purpose.
    As an example, let’s take a look at the selection of the regularization
    parameter, in which several values are searched in turn:
    """
    # prepare a range of alpha values to test
    alphas = np.array([1,0.1,0.01,0.001,0.0001,0])
    # create and fit a ridge regression model, testing each alpha
    model = Ridge()
    grid = GridSearchCV(estimator=model, param_grid=dict(alpha=alphas))
    grid.fit(X, y)
    print(grid)
    # summarize the results of the grid search
    print(grid.best_score_)
    print(grid.best_estimator_.alpha)

def testRandomParamters(X,y):
    """
    Sometimes it is more efficient to randomly select a parameter from the given range,
    estimate the algorithm quality for this parameter and choose the best one.
    """
    # prepare a uniform distribution to sample for the alpha parameter
    param_grid = {'alpha': sp_rand()}
    # create and fit a ridge regression model, testing random alpha values
    model = Ridge()
    rsearch = RandomizedSearchCV(estimator=model, param_distributions=param_grid, n_iter=100)
    rsearch.fit(X, y)
    print(rsearch)
    # summarize the results of the random parameter search
    print(rsearch.best_score_)
    print(rsearch.best_estimator_.alpha)

def testDecisionTree(X,y):
    """
        Decision Trees
        Classification and Regression Trees (CART) are often used in problems,
        in which objects have category features and used for regression and classification problems.
        The trees are very well suited for multiclass classification.
    """
    # fit a CART model to the data
    model = DecisionTreeClassifier()
    model.fit(X, y)
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

def testKNN(X,y):
    """
    k-Nearest Neighbours
    The kNN (k-Nearest Neighbors) method is often used as part of a more complex
    classification algorithm. For instance, we can use its estimate as an object’s
    feature. Sometimes, a simple kNN provides great quality on well-chosen features.
    When parameters (metrics mostly) are set well, the algorithm often gives good
    quality in regression problems.
    """
    # fit a k-nearest neighbor model to the data
    model = KNeighborsClassifier()
    model.fit(X, y)
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

def testNaiveBayes(X,y):
    """
    Naive Bayes
    Is also one of the most well-known machine learning algorithms,
    the main task of which is to restore the density of data distribution
    of the training sample. This method often provides good quality in
    multiclass classification problems.
    """
    model = GaussianNB()
    model.fit(X, y)
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

def testLR(X,y):
    """
    Logistic Regression
    Most often used for solving tasks of classification (binary),
    but multiclass classification (the so-called one-vs-all method)
    is also allowed. The advantage of this algorithm is that there’s
    the probability of belonging to a class for each object at the output.
    """
    model = LogisticRegression()
    model.fit(X, y)
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

#########################################################################
if __name__=="__main__":
    norm_and_scale = False
    path = r'C:\Users\3820104\Documents\_python_data\Biological Response'
    path = re.sub(r"\\","/",path)

    X,y = loadTrainingData(path+'/train.csv')
    X_test = loadTestData(path+'/test.csv')

    if norm_and_scale:
        # normalize the data attributes
        X = preprocessing.normalize(X)
        # standardize the data attributes
        X = preprocessing.scale(X)

    #RecursiveFeatureElimination(X,y)
    #testGBR(X,y)
    #testSVM(X,y)
    #testGridSearchCV(X,y)
    #testRandomParameters(X,y)
    #testDecisionTree(X,y)
    #testKNN(X,y)
    #testNaiveBayes(X,y)
    #testLR(X,y)
###############################################################################
