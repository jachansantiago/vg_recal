# Notebooks 
This folder contains useful notebook for data preprocessing, data analysis and for build, train and test models.

## [plot_svg.ipynb](https://github.com/binarySequoia/vg_recal/blob/master/notebooks/plot_svg.ipynb)

Useful to plot train and test svgs (Q-Q plots and ROC) created by [`vg/script/plot-qq.R`](https://github.com/vgteam/vg/blob/master/scripts/plot-qq.R) and [`vg/script/plot-roc.R`](https://github.com/vgteam/vg/blob/master/scripts/plot-roc.R). This script load train SVGs from `data/svgs/train` and load test data from `data/svgs/test`.

## [model_analysis_train_data.ipynb](https://github.com/binarySequoia/vg_recal/blob/master/notebooks/model_analysis_train_data.ipynb)
This notebook take outputs tsv files from models to measure their performance using Brier score. Note that the tsv file has a particular format, you need to consider that if you want to measure a new model. We use this notebook only to measure training data. This script loads tsv files from `data/stats/train` by default.

## [model_analysis_test_data.ipynb](https://github.com/binarySequoia/vg_recal/blob/master/notebooks/model_analysis_test_data.ipynb)
This notebook take outputs tsv files from models to measure their performance using Brier score. Note that the tsv file has a particular format, you need to consider that if you want to measure a new model. We use this notebook only to measure testing data. This script loads tsv files from `data/stats/test` by default.

## [train_test_model.ipynb](https://github.com/binarySequoia/vg_recal/blob/master/notebooks/train_test_model.ipynb)
This notebook load compared reads from a json file and train a model per base pairs length. At the end saves a csv file with stats about test and training data. The model used by this notebook is a neural network with score, original, mapping qualities, secondary score size and identity as inputs.

## [logistic_reg.ipynb] (https://github.com/binarySequoia/vg_recal/blob/master/notebooks/logistic_reg.ipynb)
This notebook runs a logistic regression with only original mapping quality as input.


## [logistic_reg_3.ipynb] (https://github.com/binarySequoia/vg_recal/blob/master/notebooks/logistic_reg_3.ipynb)
This notebook runs a logistic regression with original mapping quality, score, secondary score size as input.

## [bow.ipynb](https://github.com/binarySequoia/vg_recal/blob/master/notebooks/bow.ipynb)
This notebook contains a neural network with bag of words approach.

## [merge_data.ipynb](https://github.com/binarySequoia/vg_recal/blob/master/notebooks/merge_data.ipynb)
This notebook contains a script that takes training or testing data with different base pairs size and merge together in one csv.
