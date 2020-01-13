# Notebook for toy bdt
# Jennet Dickinson 
# May 15, 2019

import time, os, sys
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import roc_curve, roc_auc_score, accuracy_score

def main():

    hyp=sys.argv
    hyper_params=hyp[1].split(",")
    # default 6,1,0,0.3,1,1,0,1,10

    # assign hyper-parameter values
    max_depth = int(hyper_params[0])
    min_child_weight = float(hyper_params[1])
    gamma = float(hyper_params[2])
    num_rounds = 10000
    subsample = float(hyper_params[3])
    colsample_bytree = float(hyper_params[4])
    eta = float(hyper_params[5])
    alpha = float(hyper_params[6])
    Lambda = float(hyper_params[7])
    num_rounds = int(hyper_params[8])
    
    df = pd.read_csv("data_train.csv",sep=" ")
    df_test = pd.read_csv("data_test.csv",sep=" ")

    dtrain = xgb.DMatrix(df[["x","y"]],label=df["label"])
    dtest = xgb.DMatrix(df_test[["x","y"]],label=df_test["label"])

    # parameters for training
    params={'tree_method':'exact',
            'nthread':1,
            'max_depth':max_depth,
            'min_child_weight':min_child_weight,
            'gamma':gamma,
            'eta':eta,
            'subsample':subsample,
            'colsample_bytree':colsample_bytree,
            'alpha':alpha,
            'Lambda':Lambda
        }

    num_class = len(np.unique(dtrain.get_label()))
    # Multiclass
    if num_class > 2:
        params['objective']='multi:softprob'
        params['num_class'] = num_class
        params['tree_method'] = 'exact'
    else:
        params['eval_metric'] = 'auc'
        params['objective'] = 'binary:logistic'
        params['scale_pos_weight'] = 1.0*len(df[df["label"]<1])/len(df[df["label"]>0])
    
    # Fit the algorithm
    watchlist = [(dtest, 'eval')]
    myboost = xgb.train(params,dtrain,num_rounds,watchlist)#,early_stopping_rounds=5)

    # Predict 
    train_predictions = myboost.predict(dtrain)
    test_predictions = myboost.predict(dtest)

    for i in range(0,num_class):
        df["pred"+str(i)] = train_predictions[:,i]
        df_test["pred"+str(i)] = test_predictions[:,i]
                   
    hyp2="{}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{}".format(max_depth,min_child_weight,gamma,subsample,colsample_bytree,eta,alpha,Lambda,num_rounds)
    outdir="output/"+hyp2+"/"

    if os.path.isdir(outdir):
        os.system("rm -r "+outdir)
    os.mkdir(outdir)

    df.to_csv(outdir+"pred_train.csv",sep=" ",index=False)
    df_test.to_csv(outdir+"pred_test.csv",sep=" ",index=False)

    myboost.save_model(outdir+"model.h5")

if __name__ == "__main__":
    main()
