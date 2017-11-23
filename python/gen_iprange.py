#!/usr/bin/python

import sys
import itertools
import argparse

"""Hackish solution, better way would be argeparse"""
if len(sys.argv) < 2:
    print "Give one arguments: \n"
    print "gen_ip_range.py {1}"
    print "{1} is an iprange for generating all ip's in range\n"
    print "NOPENOPENOPE...exiting!"""
    sys.exit(1)

"""Declaring global variables"""
input_range	= sys.argv[1]

def ip_range(input_string):
    octets = input_string.split('.')
    chunks = [map(int, octet.split('-')) for octet in octets]
    ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]

    for address in itertools.product(*ranges):
        yield '.'.join(map(str, address))

def main():
	try:
		for address in ip_range(input_range):
			print(address)
	except Exception,e:
		print("Error: %s" % (e))
		sys.exit(1)

if __name__ == '__main__':
    """Handles main() call"""
    main()

