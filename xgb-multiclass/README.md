Jennet Dickinson
Toy BDT Model
Thesis Appendix (link)
Jan 10, 2020

To run a binary BDT with XGBoost on toy data

1. Generate toy data in csv format
```
python data.py
```

2. Visualize the toy data
```
python draw_true.py
```

3. Train a BDT using hyper-parameters
```
mkdir output
params=$max_depth,$min_child_weight,$gamma,$subsample,$colsample_bytree,$eta,$alpha,$Lambda
python train.py $params
```

4. Visualize the performance and compare to the true labels
```
draw_learned.py $params
```