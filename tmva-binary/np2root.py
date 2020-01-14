#!/usr/bin/env python
import ROOT
import numpy as np
import pandas as pd
import os

from root_numpy import array2root

def make_root(tag,cut):

   df = pd.read_csv("data_"+tag+".csv",sep=" ")
   df = df[["x","y"]][(df["label"]==cut)]
   df = df.astype('float32')
   
   if cut:
      name = "sig"
   else:
      name = "bkg"

   arr = df.to_records(index=False)
   
   array2root(arr,tag+".root",name)    
        
def main():
   os.system("rm train.root")
   os.system("rm test.root")

   make_root("test",0)
   make_root("train",0)
   
   make_root("test",1)
   make_root("train",1)
    
if __name__ == "__main__":
    main()
