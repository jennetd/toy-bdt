Jennet Dickinson
Toy BDT Model
Thesis Appendix (link)
Jan 13, 2020

To run a binary BDT with TMVA on toy data

1. Get the toy data from the xgb-binary directory and convert it to root ntuple format
```
ln -s ../xgb-binary/data*.csv .
python np2root.py
```

2. Train a BDT using hyper-parameters
```
root -l TMVAClassification.C
```

3. Apply the BDT score to the ntuple and save in ntuple format
```
root -l TMVAClassificationApplication.C
```

4. Visualize the performance and compare to the true labels
```
draw_learned.py $params
```