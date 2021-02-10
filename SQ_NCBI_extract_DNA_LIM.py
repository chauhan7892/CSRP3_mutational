#!/usr/bin/python
import sys
import re
import argparse
from SQ_parse_hmmscan_V2 import *
import pandas as pd
args_ = None


def translate(dna,LIM_Start,LIM_End): 
	
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
	if len(dna)%3 == 0:
		for i in range(0, len(dna), 3):
			codon = dna[i:i + 3] 
			protein+= table[codon] 
			if len(protein) == LIM_Start:
				D_LIM_Start = i
			if len(protein) == LIM_End:
				D_LIM_End = i+3

	return protein,[D_LIM_Start,D_LIM_End]



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
			map_dict[protein_id] = gene_id

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

	domtbl_out_file = input_file[2]

	domtbl_list = domtbl_parse(domtbl_out_file) 
	df = pd.DataFrame.from_records(domtbl_list)
	df.columns = ['dom','t_access', 'dom_len', 'q_id', 'q_access', 'q_len',\
					'seq_Eval', 'seq_score', 'seq_bias', 'dom_num', 'dom_total', \
					'dom_c_Eval', 'dom_i_Eval', 'dom_score', 'dom_bias', \
					'hmm_start', 'hmm_end', 'ali_start', 'ali_end', 'dom_start', 'dom_end',\
					'acc', 'desc']	

	df_trim = df[['q_id', 'q_len', 'dom', 'dom_num', 'dom_len', 'dom_c_Eval', 'dom_start', 'dom_end']]
	df1 = df_trim[(df_trim['dom'] == 'LIM')]
	df1 = df1.reset_index(drop=True)

	species_list = []
	for item in df1['q_id']:
		species_name = item.split('_')[1]
		species_list.append(species_name)

	df2 = pd.DataFrame({'species':species_list})
	df3 = pd.concat([df1, df2], axis=1) # concate dataframes 

	df_filt = df3[df3['q_len'] == df3.groupby(['q_id'])['q_len'].transform(max)]

	# df_filt = df_filt.sort_values('q_len').drop_duplicates('q_id')
	df_final = df_filt.reset_index(drop=True)

	with open(output_file[0], 'w') as f_out:
		for ii in range(df_final.shape[0]):
			protein_id = df_final['q_id'][ii] 
			dom_num = df_final['dom_num'][ii] 
			dom_start = df_final['dom_start'][ii] 
			dom_end = df_final['dom_end'][ii] 
			gene_id = map_dict[protein_id]
			dna_seq = fasta_dict[gene_id]['seq']
			# prot_seq,[D_L_Start,D_L_End] = translate(dna_seq,int(dom_start),int(dom_end))
			prot_seq,[D_L_Start,D_L_End] = translate(dna_seq,dom_start,dom_end)
			dna_seq_LIM = dna_seq[D_L_Start:D_L_End]
			if dom_num == 1:
				f_out.write('>L1|%s\n%s\n'%(gene_id,dna_seq_LIM))
			if dom_num == 2:
				f_out.write('>L2|%s\n%s\n'%(gene_id,dna_seq_LIM))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to complie seed genes from Literature set and OMIM")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')
