import ROOT
import pandas as pd
import numpy as np
from root_numpy import tree2array

import sys

def save(c, s):
    
    title = s+".";
    title_png = title+"png";
    title_pdf = title+"pdf";
    
    c.SaveAs(title_png)
    c.SaveAs(title_pdf)
    
    return

def draw_learned():
    
#    hyper_params=hyp.split(",")
    
    # assign hyper-parameter values
#    max_depth = int(hyper_params[0])
#    min_child_weight = float(hyper_params[1])
#    gamma = float(hyper_params[2])
#    num_rounds = 10000
#    subsample = float(hyper_params[3])
#    colsample_bytree = float(hyper_params[4])
#    eta = float(hyper_params[5])
#    alpha = float(hyper_params[6])
#    Lambda = float(hyper_params[7])
#    num_rounds = int(hyper_params[8])
    
#    h0 = ROOT.TH2D("h0","h0",1000,0,1,1000,0,1);
#    h1 = ROOT.TH2D("h1","h1",1000,0,1,1000,0,1);
#    h2 = ROOT.TH2D("h2","h2",1000,0,1,1000,0,1);
    h = ROOT.TH2D("h","h",1000,0,1,1000,0,1);
    
 #   hyp2="{}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{}".format(max_depth,min_child_weight,gamma,subsample,colsample_bytree,eta,alpha,Lambda,num_rounds)
#    outdir="output/"+hyp2+"/"
#    df = pd.read_csv(outdir+"pred_test.csv",sep=" ")


    in_file = ROOT.TFile.Open("TMVApp.root", "READ")
    tree = in_file.Get("output")
    
    all_events = tree2array(
        tree,
        branches=["x","y","score"]
    )
    
    df = pd.DataFrame(all_events)
    df[df["score"]==0] += 0.0000001
    
    for index, row in df.iterrows():
        h.Fill(row["x"],row["y"],(row["score"]+1)*0.5)
        
    c = ROOT.TCanvas("c","c",800,600)
    ROOT.gPad.SetRightMargin(0.15)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    h.GetXaxis().SetTitle("x");
    h.GetYaxis().SetTitle("y");
    h.GetZaxis().SetRangeUser(0,1);
    h.GetZaxis().SetTitle("BDT score");
    h.Draw("COLZ");
    save(c,"pred_score");
                                
    return

def main():
    draw_learned()

if __name__ == "__main__":
    main()
