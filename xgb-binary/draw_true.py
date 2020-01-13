import ROOT
import pandas as pd

def save(c, s):
    
    title = s+".";
    title_png = title+"png";
    title_pdf = title+"pdf";
    
    c.SaveAs(title_png)
    c.SaveAs(title_pdf)
    
    return

def draw_true():

    h_label = ROOT.TH2D("h_label","h_label",1000,0,1,1000,0,1);
    
    df = pd.read_csv("data_test.csv",sep=" ")
    df["label"][(df["label"]==0)] += 0.0000001
    
    for index, row in df.iterrows():
        h_label.Fill(row["x"],row["y"],row["label"]);
        
    c = ROOT.TCanvas("c_true","c_true",800,600)
    ROOT.gPad.SetRightMargin(0.15)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
            
    h_label.GetXaxis().SetTitle("x");
    h_label.GetYaxis().SetTitle("y");		
    h_label.GetZaxis().SetRangeUser(0,1);
    h_label.GetZaxis().SetTitle("Label");
    h_label.Draw("COLZ");
    
    save(c,"pred_label");

    return

def main():
    draw_true()

if __name__ == "__main__":
        main()
