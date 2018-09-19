import os
import sys
import re

# train files regex
tsv_regex = re.compile(".*.tsv")

DIR="../data/stats/test/"
files = os.listdir(DIR)

VG_DIR = '~/vg'

RSCRIPT_DIR = os.path.join(VG_DIR, "scripts")

tsv_fn = list(filter(tsv_regex.match, files))

tsv_fn.sort()


for f in tsv_fn:
    name = f[:-4]
    print("Rscript {}/plot-qq.R {} sims/svgs/test/qq_{}.svg".format(RSCRIPT_DIR, os.path.join(DIR, f), name))
    print("Rscript {}/plot-roc.R {} sims/svgs/test/roc_{}.svg".format(RSCRIPT_DIR, os.path.join(DIR, f), name))