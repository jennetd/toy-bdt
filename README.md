Jennet Dickinson
Toy BDT Model
Thesis Appendix D (http://cds.cern.ch/record/2719502?ln=en)
Jan 10, 2020

Setup instructions

Clone repository
```
git clone https://github.com/jennetd/toy-bdt
cd toy-bdt
```

All code runs in docker image jdickins/ubu16_root_xgb_etc:d
```
docker pull jdickins/ubu16_root_xgb_etc:d
docker run -it jdickins/ubu16_root_xgb_etc:d /bin/bash
source /root-6.14.08-build/bin/thisroot.sh
```

Summary of sub-directories
* xgb-binary: Run a BDT on toy data (2 classes) using XGBoost
* xgb-multiclass: Run a BDT on toy data (3 classes) using XGBoost
* tmva-binary: Run a BDT on the same 2-class toy data using TMVA

