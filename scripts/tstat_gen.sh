#!/bin/sh

if [ $# -ne 1 ];
then
	echo "USAGE ./$0 LENGHT"
	exit 1
else
	LEN=$1
	#vg recalibrate --model recal$LEN-r.model tmapped$LEN.gam | vg gamcompare -r 100 - tsim$LEN.gam --tsv --aligner recal > tstats_r_$LEN.tsv
	#vg gamcompare -r 100 tmapped$LEN.gam tsim$LEN.gam --tsv --aligner orig | sed 1d >> tstats_r_$LEN.tsv

	#vg recalibrate -b --model recal$LEN-b.model tmapped$LEN.gam | vg gamcompare -r 100 - tsim$LEN.gam --tsv --aligner recal > tstats_b_$LEN.tsv
	#vg gamcompare -r 100 tmapped$LEN.gam tsim$LEN.gam --tsv --aligner orig | sed 1d >> tstats_b_$LEN.tsv

        #vg recalibrate -e --model recal$LEN-m.model tmapped$LEN.gam | vg gamcompare -r 100 - tsim$LEN.gam --tsv --aligner recal > tstats_m_$LEN.tsv
        #vg gamcompare -r 100 tmapped$LEN.gam tsim$LEN.gam --tsv --aligner orig | sed 1d >> tstats_m_$LEN.tsv

        #vg recalibrate -b -e --model recal$LEN-bm.model tmapped$LEN.gam | vg gamcompare -r 100 - tsim$LEN.gam --tsv --aligner recal > tstats_bm_$LEN.tsv
        #vg gamcompare -r 100 tmapped$LEN.gam tsim$LEN.gam --tsv --aligner orig | sed 1d >>tstats_bm_$LEN.tsv
	
	vg recalibrate -s --model recal$LEN-ms.model tmapped$LEN.gam | vg gamcompare -r 100 - tsim$LEN.gam --tsv --aligner recal > tstats_ms_$LEN.tsv
        vg gamcompare -r 100 tmapped$LEN.gam tsim$LEN.gam --tsv --aligner orig | sed 1d >> tstats_ms_$LEN.tsv

fi
