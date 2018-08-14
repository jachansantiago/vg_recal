#!/bin/bash

if [ $# -ne 3 ];
then
	echo "USAGE $0 XG_FILE GCSA_FILE LENGHT"
	exit 1
else
	XG=$1
	GCSA=$2
	LEN=$3
	vg sim -x $XG -n 1000000 -l $LEN -i 0.001 --sub-rate 0.01 --random-seed 1 -a > sim$LEN.gam
	vg map -x $XG -g $GCSA -G sim$LEN.gam -k 5 | vg annotate -x $XG -a - -p > mapped$LEN.gam
	vg gamcompare -r 100 mapped$LEN.gam sim$LEN.gam | vg recalibrate --model recal.model --train -
	vg recalibrate --model recal.model mapped$LEN.gam | vg gamcompare -r 100 - sim$LEN.gam --tsv --aligner recal > stats$LEN.tsv
	vg gamcompare -r 100 mapped$LEN.gam sim$LEN.gam --tsv --aligner orig | sed 1d >>stats$LEN.tsv
	Rscript ../vg/scripts/plot-qq.R stats$LEN.tsv qq$LEN.svg
	exit 0
fi
