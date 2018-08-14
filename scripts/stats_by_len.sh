END=350

for ((i=70;i<=END;i = i + 10)); do
    ./stats_gen.sh snp1kg-CHR21.xg snp1kg-CHR21.gcsa $i
done
