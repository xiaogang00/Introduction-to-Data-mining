# Collaborative Filter

## Dependence
- Python 2.7
    - Tensorflow 1.1 
    - Keras 2

## Run

- `predict_sub_txt.txt` is the final results I predicted


- Put `train_sub_txt.txt` in `data\`
- Run `ensemble.py`, generate `res.txt` in root directory
## Method 
- DeepCF re-implemented  with reference to [2] and there are  following modifications for our problem:
  - Turn it into classification problem rather than regression.
  - EarlyStop to avoid over fitting, rather than eject noise.
  - Others:  Model Ensemble.
- Inherited Ideas:
  - Use history ratings as item's raw feature, enable to  generalize better to unseen items. with at least 10 ratings.  Because the input is raw feature rather than user index.
  - Adapt In-Matrix prediction, split train: test= 9:1, no overlapping between train and test data.
  - Others: Shuffle and Clean Data, Grid Search.

# Reference
- [1] `SVD` : https://github.com/mesuvash/TFMF/blob/master/TFMF.ipynb 
- [2] `DaulNet`/`DeepCF` re-implement from Xiong Y, Lin D, Niu H, et al. Collaborative Deep Embedding via Dual Networks[J]. 2016. (With Some Modifications)