import ROOT
import pandas as pd
import numpy as np
import sys

def save(c, s):
    
    title = s+".";
    title_png = title+"png";
    title_pdf = title+"pdf";
    
    c.SaveAs(title_png)
    c.SaveAs(title_pdf)
    
    return

def draw_learned(hyp):
    
    hyper_params=hyp.split(",")
    
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
    
    h = ROOT.TH2D("h","h",1000,0,1,1000,0,1);
    
    hyp2="{}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{}".format(max_depth,min_child_weight,gamma,subsample,colsample_bytree,eta,alpha,Lambda,num_rounds)
    outdir="output/"+hyp2+"/"
    df = pd.read_csv(outdir+"pred_test.csv",sep=" ")
    
    for index, row in df.iterrows():
        h.Fill(row["x"],row["y"],row["pred"])

    c = ROOT.TCanvas("c","c",800,600)
    ROOT.gPad.SetRightMargin(0.15)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    h.GetXaxis().SetTitle("x");
    h.GetYaxis().SetTitle("y");
    h.GetZaxis().SetRangeUser(0,1);
    h.GetZaxis().SetTitle("Class");
    h.Draw("COLZ");
    save(c,outdir+"pred_test");
                                
    return

def main():
    draw_learned(sys.argv[1])

if __name__ == "__main__":
    main()
