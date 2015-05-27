# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 10:50:13 2014

@author: marksargent
"""
import numpy as np

def calculate_cost(X, Y, Theta):
    cost = 0.0 #You must return the correct value for cost
    
    #add y-intercept term with a column of ones
    dimX = X.shape #get dimensions of X as a tuple (rows, columns) 
    N = dimX[0] #get number of rows
    X = np.c_[np.ones(N), X]#add column of ones at beginning to accommodate theta0
    
    B = np.dot( X, Theta )
   
    Y = np.reshape(Y,(N,1))
    B = (B - Y)**2
    for i in range(N):
        cost += B[i][0]
    cost /= 2*N

################## Your Code Here #############################################################################################
# Here we will calculate the cost of a particular choice of Theta using the least squares method . Use vectorization. Make sure
# it can handle any number of features

  
  
################################################################################################################################
 
    return cost

def gradient_descent(X, Y, Theta, alpha, num_iters):
    N = len(X) #get number of rows
    T = len(Theta)
    X_ones = np.c_[np.ones(N), X]#add column of 1s
    Costs = np.zeros(num_iters)

    
    for i in range(num_iters):
        Costs[i] = calculate_cost(X, Y, Theta)  
        temp = np.zeros((N, 1))
        temp = np.dot(X_ones, np.reshape(Theta,(T,1))) - np.reshape(Y,(N,1))
        temp = np.dot(np.transpose(X_ones), temp)
        temp *= alpha/N
        Theta -= np.reshape(temp,X.shape[1]+1)
        print i
        
        
################## Your Code Here #############################################################################################
# Here we will perform a single update to our predictions vector. Note: Make sure you indent 
# properly! This function returns both the Theta vector, and a Costs vector that keeps track of the cost for each iteration. 
       
       
###############################################################################################################################  
        
        
         
        
    return Theta, Costs

    
def normalize(X):
    N = len(X[0])
    M = len(X)
    for i in range(N):
        avg = np.mean(np.hsplit(X, N)[i])
        rng = np.std(np.hsplit(X, N)[i])
        for j in range(M):
            X[j][i] -= avg
            X[j][i] /= rng
    #Using range
            
################## Your Code Here #############################################################################################
# Perform mean normalization and feature scaling, using standard deviation. Return right value of X

    
       
       
###############################################################################################################################       
    return X
