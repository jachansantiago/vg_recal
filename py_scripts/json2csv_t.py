"""
This script convert test data from json format to csv format.

"""

from load_data import *
import os

DIR = "../data/test_gamcompare/json/"
CSV_DIR = "../data/test_gamcompare/csv/"
test_files = os.listdir(DIR)

for file in test_files:
    name = file[:-5]
    df = json2csv(os.path.join(DIR, file), debug=False, bow=True)
    df.to_csv(os.path.join(CSV_DIR, name+".csv"), index=False)