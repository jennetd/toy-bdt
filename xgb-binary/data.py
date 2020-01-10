# Script to generate toy data
# Jennet Dickinson 
# May 15, 2019

import pandas as pd
import numpy as np
from sklearn.datasets import dump_svmlight_file
import matplotlib.pyplot as plt

# Shape for toy data
def f(x,y):
    cond1 = .5*(np.cos(4*np.pi*x)+.5) > y
    cond2 = .5*(np.cos(4*np.pi*x)+1.5) < y
    return np.logical_or(cond1, cond2)

# Generate randm data from shape f
def main():

    ntest = 1000

    x = np.random.rand(ntest)
    y = np.random.rand(ntest)

    X, Y = np.meshgrid(x, y)

    # Random smearing along the boundary between X and Y
    rndm = np.random.normal(0,0.1,len(X)*len(Y))
    rndm = np.reshape(rndm,(len(X),len(Y)))    
    conds=f(X,Y+rndm)
    
    Xsig = X[np.invert(conds)]
    Ysig = Y[np.invert(conds)]
    Xbkg = X[conds]
    Ybkg = Y[conds]
    
    df = pd.DataFrame()
    df["x"] = np.append(Xsig,Xbkg)
    df["y"] = np.append(Ysig,Ybkg)
    df["label"] = np.append(np.ones(len(Xsig)),np.zeros(len(Xbkg)))
    
    df_test = pd.DataFrame()

    x = (1.0/ntest)*np.array(range(0,ntest))+(0.5/ntest)
    y = (1.0/ntest)*np.array(range(0,ntest))+(0.5/ntest)

    X, Y = np.meshgrid(x, y)
    rndm = np.random.normal(0,0.1,len(X)*len(Y))
    rndm = np.reshape(rndm,(len(X),len(Y)))

    conds=f(X,Y+rndm)
    
    Xsig = X[np.invert(conds)]
    Ysig = Y[np.invert(conds)]

    Xbkg = X[conds]
    Ybkg = Y[conds]

    df_test["x"] = np.append(Xsig,Xbkg)
    df_test["y"] = np.append(Ysig,Ybkg)
    df_test["label"] = np.append(np.ones(len(Xsig)),np.zeros(len(Xbkg)))

    df.to_csv("data_train.csv",sep=" ",index=False)
    df_test.to_csv("data_test.csv",sep=" ",index=False)

if __name__ == "__main__":
    main()
