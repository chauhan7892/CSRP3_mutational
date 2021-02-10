#!/usr/bin/python
import re,glob
import sys
import argparse
from operator import itemgetter
import copy

parser = argparse.ArgumentParser(description="A utility to convert nwk to mafft")

parser.add_argument('-i', dest="nwk",required = True,help="Input nwk file")
parser.add_argument('-m', dest="map",required = True,help="Input accession mapping file")
parser.add_argument('-o', dest="mafft",required = True,help="Output mafft file")

args = parser.parse_args()
accession_dict = {}
with open(args.map) as f :
    for line  in f :
        items = line.split('\t')
        accession_dict[items[0]] = items[1].rstrip('\n')

with open(args.nwk) as f :
	content = f.read()

for key in accession_dict :
	start_idx = content.find(key)
	end_idx = start_idx
	while True :
		if content[end_idx] == ':' :
			break
		else :
			end_idx += 1
	sub_str = content[start_idx:end_idx]
	content = content.replace(sub_str,accession_dict[key])


out_fd = open(args.mafft,"w")
out_fd.write(content)
out_fd.close()