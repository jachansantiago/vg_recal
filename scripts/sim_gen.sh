#!/bin/bash

if [ $# -ne 3 ]
then
	echo USAGE $0 XG_FILE GCSA_FILE LENGHT
	exit 1
else
	XG=$1
	GCSA=$2
	LEN=$3
	vg sim -x $XG -n 1000000 -l $LEN -i 0.001 --sub-rate 0.01 --random-seed 1 -a > sim$LEN.gam
	vg map -x  $XG -g $GCSA -G sim$LEN.gam | vg annotate -x $XG -a - -p > mapped$LEN.gam
fi
