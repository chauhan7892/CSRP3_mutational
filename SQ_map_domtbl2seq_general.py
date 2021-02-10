import sys, time, os
import argparse
import re
from SQ_parse_hmmscan_V2 import *
import pandas as pd

def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	fasta_file = input_file[0]
	domtbl_out_file = input_file[1]

	domain_of_interest = input_file[2]
	
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
				#print(seq_id)				
			else:
				seq += line

		fasta_dict[seq_id] = {}
		fasta_dict[seq_id]['name'] = seq_info
		fasta_dict[seq_id]['seq'] = seq

	'''domtbl_parse function output contains following:
	query_id, query_len, domain, domain_num, domain_total, dom_i_val, dom_start, dom_end'''

	domtbl_list = domtbl_parse(domtbl_out_file) 
	df = pd.DataFrame.from_records(domtbl_list)
	df.columns = ['dom','t_access', 'dom_len', 'q_id', 'q_access', 'q_len',\
					'seq_Eval', 'seq_score', 'seq_bias', 'dom_num', 'dom_total', \
					'dom_c_Eval', 'dom_i_Eval', 'dom_score', 'dom_bias', \
					'hmm_start', 'hmm_end', 'ali_start', 'ali_end', 'dom_start', 'dom_end',\
					'acc', 'desc']	

	df1 = df[(df['dom'] == domain_of_interest)]
	df1 = df1.reset_index(drop=True)


	with open(output_file[0], 'w') as f_out:

		for ii in range(df1.shape[0]):
			# query_id = df1['q_id'][ii] 
			# ali_start = df1['ali_start'][ii] 
			# ali_end = df1['ali_end'][ii] 
			# seq = fasta_dict[query_id]['seq'][ali_start-1:ali_end]

			query_id = df1['q_id'][ii] 
			dom_start = df1['dom_start'][ii] 
			dom_end = df1['dom_end'][ii] 
			seq_name = fasta_dict[query_id]['name']

			seq = fasta_dict[query_id]['seq'][dom_start-1:dom_end]

			out_txt = '>' + query_id + '\n' + seq + '\n'

			f_out.write(out_txt)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')