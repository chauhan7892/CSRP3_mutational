import sys, time, os
import argparse
import re
from SQ_parse_hmmscan import *
import pandas as pd

def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	fasta_file = input_file[0]
	domtbl_out_file = input_file[1]
	
	seq = ''
	fasta_dict = {}

	with open( fasta_file, 'r') as f_in_fasta:
		for line in f_in_fasta:
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

	'''domtbl_parse function output contains following:
	query_id, query_len, domain, domain_num, domain_total, dom_i_val, dom_start, dom_end'''

	domtbl_list = domtbl_parse(domtbl_out_file) 
	df = pd.DataFrame.from_records(domtbl_list)
	df.columns = ['query_id', 'query_len', 'dom', 'dom_len', 'dom_num', 'dom_total', 'dom_i_val', 'dom_start', 'dom_end']	

	df1 = df[(df['query_len'] < 300) & (df['dom'] == 'LIM') & (df['dom_total'] == 2) & ((df['dom_end']-df['dom_start']+2) == df['dom_len'])]
	df1 = df1.reset_index(drop=True)

	species_list = []
	for item in df1['query_id']:
		species_name = item.split('_')[1]
		species_list.append(species_name)

	df2 = pd.DataFrame({'species':species_list})
	df3 = pd.concat([df1, df2], axis=1) # concate dataframes 

	idx = df3.groupby(['species'])['query_len'].transform(max) == df3['query_len']
	df_final = df3[idx]

	df_final = df_final.reset_index(drop=True)

	lim1_out_txt = ''
	lim2_out_txt = ''

	for ii in range(df_final.shape[0]):
		query_id = df1['query_id'][ii]
		dom_num = df1['dom_num'][ii] 
		dom_start = df1['dom_start'][ii] 
		dom_end = df1['dom_end'][ii] 
		seq_name = fasta_dict[query_id]['name']
		seq = fasta_dict[query_id]['seq'][dom_start-1:dom_end]
		if dom_num == 1:
			lim1_out_txt += '>' + seq_name + '\n' + seq + '\n'
		else:
			lim2_out_txt += '>' + seq_name + '\n' + seq + '\n'

	with open(output_file[0], 'w') as f_out_lim1:
		f_out_lim1.write(lim1_out_txt)

	with open(output_file[1], 'w') as f_out_lim2:
		f_out_lim2.write(lim2_out_txt)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')