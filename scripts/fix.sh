END=350

for ((i=260;i<=END;i = i + 10)); do
	echo "$i"
	vg annotate -x ../snp1kg-CHR21.xg -a mapped$i.gam -p > mapped$i.gam 
done
