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
    
    h0 = ROOT.TH2D("h0","h0",1000,0,1,1000,0,1);
    h1 = ROOT.TH2D("h1","h1",1000,0,1,1000,0,1);
    h2 = ROOT.TH2D("h2","h2",1000,0,1,1000,0,1);
    h = ROOT.TH2D("h","h",1000,0,1,1000,0,1);
    
    hyp2="{}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{:.4f}_{}".format(max_depth,min_child_weight,gamma,subsample,colsample_bytree,eta,alpha,Lambda,num_rounds)
    outdir="output/"+hyp2+"/"
    df = pd.read_csv(outdir+"pred_test.csv",sep=" ")
    
    for index, row in df.iterrows():
        h0.Fill(row["x"],row["y"],row["pred0"]);
        h1.Fill(row["x"],row["y"],row["pred1"]);
        h2.Fill(row["x"],row["y"],row["pred2"]);

        m = np.argmax([row["pred0"],row["pred1"],row["pred2"]])
        if m == 0 :
            m += 0.0000001
        h.Fill(row["x"],row["y"],m)

    c = ROOT.TCanvas("c","c",800,600)
    ROOT.gPad.SetRightMargin(0.15)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    h.GetXaxis().SetTitle("x");
    h.GetYaxis().SetTitle("y");
    h.GetZaxis().SetRangeUser(0,2);
    h.GetZaxis().SetTitle("Class");
    h.Draw("COLZ");
    save(c,outdir+"pred_class");
                                
    c0 = ROOT.TCanvas("c0","c0",800,600)
    h0.GetXaxis().SetTitle("x");
    h0.GetYaxis().SetTitle("y");		
    h0.GetZaxis().SetRangeUser(0,1);
    h0.GetZaxis().SetTitle("Score 0");
    h0.Draw("COLZ");
    save(c0,outdir+"pred_score0");

    c1 = ROOT.TCanvas("c1","c1",800,600)
    h1.GetXaxis().SetTitle("x");
    h1.GetYaxis().SetTitle("y");
    h1.GetZaxis().SetRangeUser(0,1);
    h1.GetZaxis().SetTitle("Score 1");
    h1.Draw("COLZ");
    save(c1,outdir+"pred_score1");

    c2 = ROOT.TCanvas("c2","c2",800,600)
    h2.GetXaxis().SetTitle("x");
    h2.GetYaxis().SetTitle("y");
    h2.GetZaxis().SetRangeUser(0,1);
    h2.GetZaxis().SetTitle("Score 2");
    h2.Draw("COLZ");
    save(c2,outdir+"pred_score2");

    return

def main():
    draw_learned(sys.argv[1])

if __name__ == "__main__":
    main()
