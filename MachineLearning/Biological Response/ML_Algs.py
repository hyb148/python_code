__author__ = 'john'

# http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3885826/
# http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier
# http://kukuruku.co/hub/python/introduction-to-machine-learning-with-python-andscikit-learn

import numpy as np
from numpy import genfromtxt, savetxt
# import matplotlib.pyplot as plt
from sklearn import ensemble
# from sklearn import datasets
# from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from sklearn import cross_validation
from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error,r2_score
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
from sklearn.ensemble import RandomForestClassifier
import scipy as sp


def load_training_data_xy(filename):
    """
    read csv file into X & y
    :param filename: str
    :return: training and key data
    :rtype : numpy arrays
    """
    try:
        dataset = np.genfromtxt(open(filename, 'r'), delimiter=',', dtype='f8')[1:]
        y = np.array([x[0] for x in dataset])
        X = np.array([x[1:] for x in dataset])
    except:
        X, y = [], []
    return X, y


def split_training_data(X, y, split=0.9):
    try:
        offset = int(X.shape[0] * split)
        X_train, y_train = X[:offset], y[:offset]
        X_test, y_test = X[offset:], y[offset:]
    except:
        X_train, y_train, X_test, y_test = [], [], [], []
    return X_train, y_train, X_test, y_test


def load_test_data(filename):
    """

    :rtype : object
    """
    try:
        return genfromtxt(open(filename, 'r'), delimiter=',', dtype='f8')[1:]
    except:
        return []


def log_loss_fun(act, pred):
    """

    :rtype : float
    """
    epsilon = 1e-15
    pred = sp.maximum(epsilon, pred)
    pred = sp.minimum(1-epsilon, pred)
    ll = sum(act*sp.log(pred) + sp.subtract(1,act)*sp.log(sp.subtract(1,pred)))
    ll = ll * -1.0/len(act)
    return ll


def test_clf(clf, X, y, split=0.9):
    X_train, y_train, X_test, y_test = splitTrainingData(X, y, split)
    clf.fit(X_train, y_train)
    mse = mean_squared_error(y_test, clf.predict(X_test))
    print("Training Learning Set MSE(%d): %.4f" % split, mse)
    return clf


def submit_clf(clf, X, y, filename):
    print("Fitting regression model using full dataset")
    clf.fit(X, y)
    y_test = clf.predict(X_test)
    predicted_probs = [[index + 1, x] for index, x in enumerate(y_test)]
    savetxt('GBR_full_submission.csv', predicted_probs, delimiter=',', fmt='%d,%f',
            header='MoleculeId,PredictedProbability', comments='')
    return clf


def rfc_k_fold_test(model, X, y, folds=5):
    """

    :param clf:
    :param X:
    :param y:
    :param folds:
    :return: mean: float
    """
    print("Fit regression model using KFold datasets")
    cv = cross_validation.KFold(len(y), n_folds=folds)  #, indices=False)

    #iterate through the training and test cross validation segments and
    #run the classifier on each one, aggregating the results into a list
    results = []
    for traincv, testcv in cv:
        probas = model.fit(X[traincv], y[traincv]).predict_proba(X[testcv])
        """
        For me, the Mean Squared Error wasn't much informative and
        used instead the R2 coefficient of determination. This
        measure is a number indicating how well a variable is able
        to predict the other. Values close to 0 means poor
        prediction and values close to 1 means perfect prediction.
        """
        mse = mean_squared_error(y[testcv], probas)
        r2 = r2_score(y[testcv], probas)
        print("MSE: %.4f" % mse)
        print("R2: %.4f" % r2)
        results.append(log_loss_fun(y[testcv], probas)) #[x[1] for x in

    #print out the mean of the cross-validated results
    return np.array(results).mean()


def recursive_feature_elimination(X, y):
    model = LogisticRegression()
    # create the RFE model and select 3 attributes
    rfe = RFE(model, 3)
    rfe = rfe.fit(X, y)
    # summarize the selection of the attributes
    print(rfe.support_)
    print(rfe.ranking_)


def test_gbr(X, y):
    params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 1,
              'learning_rate': 0.01, 'loss': 'ls'}
    clf = ensemble.GradientBoostingRegressor(**params)

    clf = testClf(clf, X, y)
    saveModel("GBR_split", clf, params)

    clf = submitClf(clf, X, y)
    saveModel("GBR_full", clf, params)

    kfoldTest(clf, X, y, 10)


def test_svm(X, y):
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


# noinspection PyByteLiteral
def test_grid_searchCV(X, y):
    """ How to Optimize Algorithm Parameters One of the most difficult stages in creating really efficient algorithms
    is choosing correct parameters. Its usually easier with experience, but one way or another, we have to do the search.
    Fortunately, Scikit-Learn provides many implemented functions for this purpose. As an example, lets take a look at
    the selection of the regularization parameter, in which several values are searched in turn: """

    # prepare a range of alpha values to test
    alphas = np.array([1, 0.1, 0.01, 0.001, 0.0001, 0])
    # create and fit a ridge regression model, testing each alpha
    model = Ridge()
    grid = GridSearchCV(estimator=model, param_grid=dict(alpha=alphas))
    grid.fit(X, y)
    print(grid)
    # summarize the results of the grid search
    print(grid.best_score_)
    print(grid.best_estimator_.alpha)


def test_random_parameters(X, y):
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


def test_decision_tree(X, y):
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


def test_knn(X, y):
    """
    k-Nearest Neighbours The kNN (k-Nearest Neighbors) method is often used as part of a more complex classification
    algorithm. For instance, we can use its estimate as an objects feature. Sometimes, a simple kNN provides great
    quality on well-chosen features. When parameters (metrics mostly) are set well, the algorithm often gives good
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


def test_naive_bayes(X, y):
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


def test_logical_regression(X, y):
    """
    Logistic Regression
    Most often used for solving tasks of classification (binary), but multi-class classification
    (the so-called one-vs-all method) is also allowed. The advantage of this algorithm is that
    there's the probability of belonging to a class for each object at the output.
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


def save_model(self, filename, clf, params):
    for key in params:
        filename += "_" + key + "_" + str(params[key])
    filename += ".pkl"
    print "writing to: " + filename
    stuff = joblib.dump(clf, filename, compress=9)
    print stuff
    """
    Later you can load back the pickled model (possibly in another Python process) with:
    >>> clf = joblib.load('filename.pkl')
    """

