"""
This file merge csv files of every read base pair lenght together.
"""
import os
import numpy as np
import pandas as pd

DIR = "../data/test_gamcompare/csv/"   #FILE can be TRAINING OR TEST DATA

OUTPUT_FILE = "big_bow_df_test.csv"

files = os.listdir(DIR)

dataframes = list()

for f in files:
    print("Loading {}".format(f))
    dataframes.append(pd.read_csv(os.path.join(DIR,f)))
    
l = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 70, 80, 90]

for d, n in zip(dataframes, l):
    d['len'] = np.ones(d.shape[0]) * n
    
bigdf = pd.concat(dataframes, ignore_index=True)

bigdf.to_csv(OUTPUT_FILE, index=False)