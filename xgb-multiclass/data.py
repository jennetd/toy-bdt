# Script to generate toy data
# Jennet Dickinson 
# May 15, 2019

import pandas as pd
import numpy as np
from sklearn.datasets import dump_svmlight_file
import matplotlib.pyplot as plt

# Shape for toy data
def f(x,y,rndm):

    df = pd.DataFrame()
    df["x"]=x.flatten()
    df["y"]=y.flatten()
    df["rndm"]=rndm.flatten()
    df["label"]=0

    df["label"][(.5*(np.cos(4*np.pi*df["x"])+.5) > df["y"]+df["rndm"])] = 1
    df["label"][(.5*(np.cos(4*np.pi*df["x"])+1.5) < df["y"]+df["rndm"])] = 2

    return df[["x","y","label"]]
    

# Generate randm data from shape f
def main():

    ntest = 1000

    x = np.random.rand(ntest)
    y = np.random.rand(ntest)

    X, Y = np.meshgrid(x, y)

    # Random smearing along the boundary between X and Y
    rndm = np.random.normal(0,0.1,len(X)*len(Y))
    rndm = np.reshape(rndm,(len(X),len(Y)))    

    df = f(X,Y,rndm)
    
    df_test = pd.DataFrame()

    x = (1.0/ntest)*np.array(range(0,ntest))+(0.5/ntest)
    y = (1.0/ntest)*np.array(range(0,ntest))+(0.5/ntest)

    X, Y = np.meshgrid(x, y)
    rndm = np.random.normal(0,0.1,len(X)*len(Y))
    rndm = np.reshape(rndm,(len(X),len(Y)))

    df_test = f(X,Y,rndm)
    
    df.to_csv("data_train.csv",sep=" ",index=False)
    df_test.to_csv("data_test.csv",sep=" ",index=False)

if __name__ == "__main__":
    main()
