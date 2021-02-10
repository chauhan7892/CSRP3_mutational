#!/usr/bin/env python
import os, re, sys
import argparse

def main( ):
        
	input_file = args_.input_argument
	output_file = args_.output_argument
	pdb_ID_list = []

	pdb_lim1 = input_file[0]
	pdb_lim2 = input_file[1]
	pdb_txt_search = input_file[2]

	lim1_set = set()
	lim2_set = set()
	search_set = set()
	with open(pdb_lim1, 'r') as f_in_lim1:
		for line in f_in_lim1:
			if line[0] == '#':continue
			if line == '\n':continue
			line = line.strip().split('\t')
			pdb_id = line[1].split('_')[0]
			lim1_set.add(pdb_id)

	with open(pdb_lim2, 'r') as f_in_lim2:
		for line in f_in_lim2:
			if line[0] == '#':continue
			if line == '\n':continue
			line = line.strip().split('\t')
			pdb_id = line[1].split('_')[0]
			lim2_set.add(pdb_id)

	with open(pdb_txt_search, 'r') as f_in_search:
		for line in f_in_search:
			if line == '\n':continue
			line = line.strip('\n').split('_')
			pdb_id = line[0]
			search_set.add(pdb_id)

	print('LIM1 PDBs: %d' %(len(lim1_set)))
	print('LIM2 PDBs: %d' %(len(lim2_set)))
	print('Search PDBs: %d' %(len(search_set)))
	print('LIM1 & LIM2 PDBs: %d' %(len(lim1_set.intersection(lim2_set))))
	print('LIM1 & txt search PDBs: %d' %(len(lim1_set.intersection(search_set))))
	print('LIM2 & txt search PDBs: %d' %(len(lim2_set.intersection(search_set))))
	print('LIM1+LIM2 & txt search PDBs: %d' %(len(lim1_set.union(lim2_set).intersection(search_set))))

	print('PDB exlusive to txt search: %s' %(search_set.difference(lim1_set.union(lim2_set))))

	all_pdb = lim1_set.union(lim2_set).union(search_set)

	with open(output_file[0], 'w') as f_out:
		for pdb in all_pdb:
			txt = pdb + '\n'
			f_out.write(txt)

	
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to download pdb")
    parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
    parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
    args_ = parser.parse_args()
    main(  )
    print('done')    
