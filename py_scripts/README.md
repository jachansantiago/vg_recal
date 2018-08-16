# Python Scripts

This folder contain python scripts with useful functions, data processing, shell script generator, model training and model testing.


## Import files

- **load_data.py** : This file contains function to load training and testing data from json files.
- **models.py** : This file contains neural network models.

## Training and Testing files

- **train.py** : This script train a shallow model for each base pair lenght from 70 to 250(19 models).
- **train_bow_sz_robust.py** : This scrpit train a neural network using bag of word througt a dataset with different basepairs lenghts.
- **test_bow_sz_robust.py** : This scrpit test a neural network using bag of word througt a dataset with different basepairs lenghts.

## scripts

- **merge_data.py** : This script takes training or testing data with different base pairs size and merge together in one csv.
- **json2csv.py** : This script take *training* data in json format and convert into csv. Only choose some features from the json file.
- **json2csv_t.py** : This script take *testing* data in json format and convert into csv. Only choose some features from the json file.

## shell script generator
To run these scripts you need to run `python py_script.py > shell_script.sh`
- **qqplot_svg.py**: this script produce a shell scrpit to generate QQ-plots and roc plots.
- **gam2json.py** : this script generate a script to convert from gam format to json format
