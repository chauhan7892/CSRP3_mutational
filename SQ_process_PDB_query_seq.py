#!/usr/bin/env python
import os, re, sys
import argparse


def fasta_fmt(seq):
	count = 1

	new_txt = ''
	for ch in seq:
		new_txt += ch
		if count % 50 == 0:
			new_txt += '\n'
		count += 1

	if new_txt[-1] != '\n':
		new_txt += '\n'

	return new_txt

 

def main( ):
        
	input_file = args_.input_argument
	output_file = args_.output_argument


	
	pdb_seq_file = input_file[0]
	pdb_id_file = input_file[1]

	seq = ''
	fasta_dict = {}
	with open(pdb_seq_file, 'r') as f_in_seq:
		for line in f_in_seq:
			if line == '\n':continue
			# print line
			line = line.strip('\n')
			if line[0] == '>':
				if seq:
					fasta_dict[seq_id] = seq
					seq = ''

				seq_id = line.split('>')[1].split('|')[0]	
				
			else:
				seq += line

		fasta_dict[seq_id] = seq

	out_txt = ''
	with open(pdb_id_file, 'r') as f_in_pdb_ID:
		for line in f_in_pdb_ID:
			if line == '\n':continue
			line = line.strip('\n').split('_')
			pdb_id = line[0]
			pdb_chain = line[1]
			pdb_LIM = pdb_id+':'+pdb_chain

			out_txt += '>'+pdb_LIM + '\n' + fasta_fmt(fasta_dict[pdb_LIM])


				
	with open(output_file[0], 'w') as f_out:
		f_out.write(out_txt)

	
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to download pdb")
    parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
    parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
    args_ = parser.parse_args()
    main(  )
    print('done')    
