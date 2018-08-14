#!/bin/sh

if [ $# -ne 1 ];
then
	echo "USAGE ./$0 LENGHT"
	exit 1
else
	LEN=$1
	#vg gamcompare -r 100 mapped$LEN.gam sim$LEN.gam | vg recalibrate --model recal$LEN-r.model --train -
	#vg recalibrate --model recal$LEN-r.model mapped$LEN.gam | vg gamcompare -r 100 - sim$LEN.gam --tsv --aligner recal > stats_r_$LEN.tsv
	#vg gamcompare -r 100 mapped$LEN.gam sim$LEN.gam --tsv --aligner orig | sed 1d >>stats_r_$LEN.tsv

	#vg gamcompare -r 100 mapped$LEN.gam sim$LEN.gam | vg recalibrate -b --model recal$LEN-b.model --train -
	#vg recalibrate -b --model recal$LEN-b.model mapped$LEN.gam | vg gamcompare -r 100 - sim$LEN.gam --tsv --aligner recal > stats_b_$LEN.tsv
	#vg gamcompare -r 100 mapped$LEN.gam sim$LEN.gam --tsv --aligner orig | sed 1d >>stats_b_$LEN.tsv

	#vg gamcompare -r 100 mapped$LEN.gam sim$LEN.gam | vg recalibrate -e --model recal$LEN-m.model --train -
        #vg recalibrate -e --model recal$LEN-m.model mapped$LEN.gam | vg gamcompare -r 100 - sim$LEN.gam --tsv --aligner recal > stats_m_$LEN.tsv
        #vg gamcompare -r 100 mapped$LEN.gam sim$LEN.gam --tsv --aligner orig | sed 1d >>stats_m_$LEN.tsv

	#vg gamcompare -r 100 mapped$LEN.gam sim$LEN.gam | vg recalibrate -b -e --model recal$LEN-bm.model --train -
        #vg recalibrate -b -e --model recal$LEN-bm.model mapped$LEN.gam | vg gamcompare -r 100 - sim$LEN.gam --tsv --aligner recal > stats_bm_$LEN.tsv
        #vg gamcompare -r 100 mapped$LEN.gam sim$LEN.gam --tsv --aligner orig | sed 1d >>stats_bm_$LEN.tsv
	
	#vg gamcompare -r 100 mapped$LEN.gam sim$LEN.gam | vg recalibrate -s --model recal$LEN-ms.model --train -
        vg recalibrate -s --model recal$LEN-ms.model mapped$LEN.gam | vg gamcompare -r 100 - sim$LEN.gam --tsv --aligner recal > stats_ms_$LEN.tsv
        vg gamcompare -r 100 mapped$LEN.gam sim$LEN.gam --tsv --aligner orig | sed 1d >>stats_ms_$LEN.tsv

#Rscript ../../vg/scripts/plot-qq.R stats$LEN.tsv qq$LEN.svg
	exit 0
fi
