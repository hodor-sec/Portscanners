#!/bin/bash

IPSTART=1
IPEND=254
IP='192.168.1.'
PORTRANGE=443
OPTS='s_client -CApath /etc/ssl -connect'
RUNOPENSSL=$(which openssl)
RUNTIMEOUT=$(which timeout)
TIMEOUTOPTS=1

for n in $(seq ${IPSTART} ${IPEND}); do
	echo ${IP}${n}
	((${RUNTIMEOUT} ${TIMEOUTOPTS} ${RUNOPENSSL} ${OPTS} ${IP}${n}:${PORTRANGE}) | ${RUNOPENSSL} x509 -noout 2> >(grep -iv 'unable to load certificate\|Expecting: TRUSTED CERTIFICATE'));
done
