import os
import sys
import re

# train files regex
tsv_regex = re.compile(".*.tsv")

DIR="../data/stats/test/"
files = os.listdir(DIR)

tsv_fn = list(filter(tsv_regex.match, files))

tsv_fn.sort()
#print(tsv_fn)

for f in tsv_fn:
    name = f[:-4]
    print("Rscript ~/vg/scripts/plot-qq.R {} sims/svgs/test/qq_{}.svg".format(os.path.join(DIR, f), name))
    print("Rscript ~/vg/scripts/plot-roc.R {} sims/svgs/test/roc_{}.svg".format(os.path.join(DIR, f), name))