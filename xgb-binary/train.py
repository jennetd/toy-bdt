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
    params={'eval_metric':'auc',
            'objective':'binary:logistic',
            'tree_method':'exact',
            'nthread':1,
            'scale_pos_weight':len(df[df["label"]<1])/len(df[df["label"]>0]),
            'max_depth':max_depth,
            'min_child_weight':min_child_weight,
            'gamma':gamma,
            'eta':eta,
            'subsample':subsample,
            'colsample_bytree':colsample_bytree,
            'alpha':alpha,
            'Lambda':Lambda
        }

    # Fit the algorithm
    watchlist = [(dtest, 'eval')]
    myboost = xgb.train(params,dtrain,num_rounds,watchlist)#,early_stopping_rounds=5)

    # Predict 
    train_predictions = myboost.predict(dtrain)
    test_predictions = myboost.predict(dtest)

    df["pred"] = train_predictions
    df_test["pred"] = test_predictions

    hyp2="{}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{}".format(max_depth,min_child_weight,gamma,subsample,colsample_bytree,eta,alpha,Lambda,num_rounds)
    outdir="output/"+hyp2+"/"

    if os.path.isdir(outdir):
        os.system("rm -r "+outdir)
    os.mkdir(outdir)

    df.to_csv(outdir+"pred_train.csv",sep=" ",index=False)
    df_test.to_csv(outdir+"pred_test.csv",sep=" ",index=False)

    xgb_fp, xgb_tp, threshs = roc_curve(dtest.get_label(), test_predictions)
    roc = pd.DataFrame()
    roc["fp"] = xgb_fp
    roc["tp"] = xgb_tp
    roc["thresh"] = threshs

    xgb_fp, xgb_tp, threshs = roc_curve(dtest.get_label(), test_predictions)
    roc_test = pd.DataFrame()
    roc_test["fp"] = xgb_fp
    roc_test["tp"] = xgb_tp
    roc_test["thresh"] =threshs

    roc.to_csv(outdir+"roc_train.csv",sep=" ",index=False)
    roc_test.to_csv(outdir+"roc_test.csv",sep=" ",index=False)

    myboost.save_model(outdir+"model.h5")

if __name__ == "__main__":
    main()
