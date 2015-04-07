# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:08:49 2015

@author: 3820104
"""
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import os.path
import re
from numpy import savetxt
import time
from sklearn.externals import joblib
import cPickle as pickle
import sys

sys.path.append(".")
import ML_Algs
###############################################################################
def get_tick():
    return time.time()


def get_dt(tick):
    return time.time() - tick

#########################################################################
if __name__ == "__main__":
    norm_and_scale = False
    path = r'../../../_python_data\Biological Response'
    path = re.sub(r"\\", "/", path)
    training_data_path = path + '/train.csv'
    test_data_path = path + '/test.csv'
    if os.path.isfile(training_data_path):
        print "data file exists."
    else:
        print "bad data file name."
        exit()

    tick = get_tick()
    X_train, y_train = ML_Algs.load_training_data_xy(training_data_path)
    X_test = ML_Algs.load_test_data(test_data_path)
    print('loading time = ', get_dt(tick))

    if norm_and_scale:
        # normalize the data attributes
        X_train = preprocessing.normalize(X_train)
        # standardize the data attributes
        X_train = preprocessing.scale(X_train)
    n_estimators = 100
    if False:
        # train model and test on X_test data, save to submissions file
        print "Running RFC on data ..."
        tick = get_tick()
        model = RandomForestClassifier(n_estimators)
        model.fit(X_train, y_train)
        print('training time = ', get_dt(tick))
        predicted_probs = [[index + 1, x[1]] for index, x in enumerate(model.predict_proba(X_test))]
        savetxt(path + '/RFC_submission.csv', predicted_probs, delimiter=',', fmt='%d,%f',
                header='MoleculeId,PredictedProbability', comments='')
        print "saved results file."
    """
        pickle.dumps(model, open(path+'/RFC.pkl', "wb"))
        #joblib.dump(model, path+'/RFC.pkl')
    else:
        model = pickle.load(open(path+'/RFC.pkl', "rb"))
        #model = joblib.load(path+'/RCF.pkl')
    """

    print "Running K-Fold Cross Validation test ..."
    tick = get_tick()
    model = RandomForestClassifier(n_estimators)
    results = ML_Algs.rfc_k_fold_test(model, X_train, y_train, 5)
    print('cross validation time = ', get_dt(tick))
    print "Mean results: " + str(results)


    # RecursiveFeatureElimination(X_train,y_train_train)
    #testGBR(X_train,y_train)
    #testSVM(X_train,y_train)
    #testGridSearchCV(X_train,y_train)
    #testRandomParameters(X_train,y_train)
    #testDecisionTree(X_train,y_train)
    #testKNN(X_train,y_train)
    #testNaiveBay_traines(X_train,y_train)
    #testLR(X_train,y_train)
###############################################################################
