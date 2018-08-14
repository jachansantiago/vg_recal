END=250

for ((i=70;i<=END;i = i + 10)); do
    ./sim_gen.sh ../snp1kg-CHR21.xg ../snp1kg-CHR21.gcsa $i
done
