#!/usr/bin/python
import sys
import re
import argparse
from SQ_parse_hmmscan_V2 import *
import pandas as pd
args_ = None


def translate(dna): 
	
	table = { 
		'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M', 
		'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T', 
		'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K', 
		'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',				 
		'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 
		'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P', 
		'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q', 
		'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R', 
		'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 
		'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A', 
		'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E', 
		'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G', 
		'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 
		'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L', 
		'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_', 
		'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W', 
	} 
	protein ="" 

	if len(dna)%3 ==0:	
		for i in range(0, len(dna), 3):
			codon = dna[i:i + 3] 
			protein+= table[codon] 
	return protein



def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	map_dict = {}
	header = True
	with open(input_file[0], 'r') as f_in_map:
		for line in f_in_map:
			if header == True:
				header = False
				continue
			line_attrs = line.strip('\n').split('\t')
			protein_id = line_attrs[0]
			gene_id = line_attrs[1]
			map_dict[gene_id] = protein_id

	seq = ''
	fasta_dict = {}
	with open(input_file[1], 'r') as f_in_dna_seq:
		for line in f_in_dna_seq:
			if line[0]=='\n':continue
			line = line.strip('\n')
			if line[0] == '>':
				if seq:
					fasta_dict[seq_id] = {}
					fasta_dict[seq_id]['name'] = seq_info
					fasta_dict[seq_id]['seq'] = seq
					seq = ''
				seq_info = line.split('>')[1]
				seq_id = seq_info.split()[0]	
			else:
				seq += line

		fasta_dict[seq_id] = {}
		fasta_dict[seq_id]['name'] = seq_info
		fasta_dict[seq_id]['seq'] = seq

	# print(fasta_dict.keys())

	with open(output_file[0], 'w') as f_out:
		for gene_id in fasta_dict:
			dna_seq = fasta_dict[gene_id]['seq']
			protein_id = map_dict[gene_id.split('|')[1]]
			prot_seq = translate(dna_seq)
			f_out.write('>%s\t%s\n%s\n'%(protein_id,gene_id,prot_seq))



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to complie seed genes from Literature set and OMIM")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')
