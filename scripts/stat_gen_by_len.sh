#!/bin/sh
END=250
N=2
J=0
for ((i=70;i<=END;i = i + 10)); do
	((J=J%N)); ((J++==0)) && wait
	./stat_gen.sh $i &
done

echo "DONE"
