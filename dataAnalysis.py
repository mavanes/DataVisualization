# -*- coding: utf-8 -*-
"""
Created on Sat May 23 20:06:55 2015

@author: todd
"""

from pymongo import MongoClient
import pylab as pl
import numpy as np
import ex3_functions as cf
from sklearn import linear_model
import time
import datetime

client = MongoClient()

db = client.big_data
yt = db.youtube
dm = db.dailymotion

def convert_to_timestamp(date):
    return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())

def create_ytarray():
    X = []
    Y = []
    results = yt.find()
    for doc in results:
        entry = []
        entry.append(convert_to_timestamp((doc["snippet"]["publishedAt"]).split("T")[0]))
        X.append(entry)
        Y.append(int(doc["statistics"]["viewCount"]))
    
    X = np.array(X)
    Y = np.array(Y)
    return X, Y
    
def create_dmarray():
    X = []
    Y = []
    results = dm.find()
    for doc in results:
        entry = []
        entry.append(int(doc["fans_total"]))
        entry.append(int(doc["duration"]))
        entry.append(int(doc["created_time"]))
        X.append(entry)
        Y.append(int(doc["views_total"]))
    
    X = np.array(X)
    Y = np.array(Y)
    return X, Y
    
def dm_main():
    arr = create_dmarray()
    X = arr[0]
    Y = arr[1]
    
    X = cf.normalize(X)
    
    dimX = X.shape  # get dimensions of X as a tuple (rows, columns) 
    N = dimX[1]  # of columns in X; number of features
    Theta = np.zeros(N + 1)  # add a column for theta0
    
    #Our results
    print "Cost before gradient descent: " , cf.calculate_cost(X, Y, Theta)
    Results = cf.gradient_descent(X, Y, Theta, .01, 1000)
    print "Thetas: " , Results[0]
    Theta = Results[0]
    print "Cost after gradient descent: ", cf.calculate_cost(X, Y, Theta)
    
    
    # Compare with sci-kit-learns's implementation ##########################################
    # Create linear regression object
    regr = linear_model.LinearRegression()
    
    
    # Train the model using the training sets
    regr.fit(X, Y)
    
    # The coefficients
    print "\nResults from sci-kit-learn's linar regression method:"
    print 'Coefficients: ', regr.coef_
    print 'Intercept : ', regr.intercept_
    # The mean square error
    Theta = np.append(regr.coef_, regr.intercept_)
    
    print cf.calculate_cost(X, Y, Theta)
    # Plot cost versus iterations to check if it converges
    pl.xlabel("Iterations")
    pl.ylabel("Cost")
    pl.plot(Results[1])

    pl.show()

def yt_main():
    arr = create_ytarray()
    X = arr[0]
    Y = arr[1]
    
    X = cf.normalize(X)
    
    dimX = X.shape  # get dimensions of X as a tuple (rows, columns) 
    N = dimX[1]  # of columns in X; number of features
    Theta = np.zeros(N + 1)  # add a column for theta0
    
    #Our results
    print "Cost before gradient descent: " , cf.calculate_cost(X, Y, Theta)
    Results = cf.gradient_descent(X, Y, Theta, .05, 100)
    print "Thetas: " , Results[0]
    Theta = Results[0]
    print "Cost after gradient descent: ", cf.calculate_cost(X, Y, Theta)
    
    
    # Compare with sci-kit-learns's implementation ##########################################
    # Create linear regression object
    regr = linear_model.LinearRegression()
    
    
    # Train the model using the training sets
    regr.fit(X, Y)
    
    # The coefficients
    print "\nResults from sci-kit-learn's linar regression method:"
    print 'Coefficients: ', regr.coef_
    print 'Intercept : ', regr.intercept_
    # The mean square error
    
    
    # Plot cost versus iterations to check if it converges
    pl.xlabel("Iterations")
    pl.ylabel("Cost")
    pl.plot(Results[1])

    pl.show()


if __name__ == '__main__':
    dm_main()
    #yt_main()