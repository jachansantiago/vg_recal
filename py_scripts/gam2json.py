import os
import sys
import re

# train files regex
sim_regex = re.compile("sim.*.gam")
map_regex = re.compile("map.*.gam")

# test files regex
tsim_regex = re.compile("tsim.*.gam")
tmap_regex = re.compile("tmap.*.gam")

files = os.listdir()

sim_fn = list(filter(sim_regex.match, files))
map_fn = list(filter(map_regex.match, files))

tsim_fn = list(filter(tsim_regex.match, files))
tmap_fn = list(filter(tmap_regex.match, files))

sim_fn.sort()
map_fn.sort()

tsim_fn.sort()
tmap_fn.sort()

for s, m in zip(tsim_fn, tmap_fn):
	sfname = s[:-4]
	mfname = m[:-4]
	#print("vg view -a {} > {}.json".format(s, sfname))
	#print("vg view -a {} > {}.json".format(m, mfname))
	#print("vg gamcompare -r 100 {} {} > tcompared_{}_{}.gam".format( m, s, mfname, sfname))
	print("vg view -a tcompared_{}_{}.gam > tcompared_{}_{}.json".format(mfname, sfname, mfname, sfname))
