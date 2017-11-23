#!/bin/bash

PORTRANGE=1-65535
OPTS='-zvw 1'
RUNNC=$(which nc)

for n in $(cat /tmp/targets.txt); do
	IP=$(echo $n);
	(${RUNNC} ${OPTS} ${n} ${PORTRANGE} 2> >(grep -i open) | tee netcat.tcp.range.${PORTRANGE}.${n}.log &);
done
