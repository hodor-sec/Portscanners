#!/bin/bash

IPSTART=1
IPEND=254
IP='a.b.c.'
PORTRANGE=1-65535
OPTS='-zvw 1'
RUNNC=$(which nc)

for n in $(seq ${IPSTART} ${IPEND}); do
	(${RUNNC} ${OPTS} ${IP}${n} ${PORTRANGE} 2> >(grep -i open) | tee netcat.tcp.range.${PORTRANGE}.${IP}${n}.log &);
done
