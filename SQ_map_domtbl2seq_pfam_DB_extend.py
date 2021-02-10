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
	
	seq = ''
	fasta_dict = {}

	with open( fasta_file, 'r') as f_in_fasta:
		for line in f_in_fasta:
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
		"""
		dom, t_access, dom_len, q_id, q_access, q_len,\
					seq_Eval, seq_score, seq_bias, dom_num, dom_total, \
					dom_c_Eval, dom_i_Eval, dom_score, dom_bias, \
					hmm_start, hmm_end, ali_start, ali_end, dom_start, dom_end,\
					acc, desc
		"""

	domtbl_list = domtbl_parse(domtbl_out_file) 
	df = pd.DataFrame.from_records(domtbl_list)
	df.columns = ['dom','t_access', 'dom_len', 'q_id', 'q_access', 'q_len',\
					'seq_Eval', 'seq_score', 'seq_bias', 'dom_num', 'dom_total', \
					'dom_c_Eval', 'dom_i_Eval', 'dom_score', 'dom_bias', \
					'hmm_start', 'hmm_end', 'ali_start', 'ali_end', 'dom_start', 'dom_end',\
					'acc', 'desc']

	df_trim = df[['q_id', 'q_len', 'dom',  'dom_num', 'dom_len', 'dom_c_Eval', 'dom_start', 'dom_end']]

	df1 = df_trim[(df_trim['dom'] == 'LIM')]
	df1 = df1.reset_index(drop=True)

	df_filt = df1[df1['q_len'] == df1.groupby(['q_id'])['q_len'].transform(max)]

	# df_filt = df_filt.sort_values('q_len').drop_duplicates('q_id')
	df_final = df_filt.reset_index(drop=True)

	with open(output_file[0], 'w') as f_out:
		for ii in range(df_final.shape[0]):
			query_id = df_final['q_id'][ii] 
			dom_num = df_final['dom_num'][ii]
			dom_start = df_final['dom_start'][ii] 
			dom_end = df_final['dom_end'][ii] 
			seq_name = fasta_dict[query_id]['name']
			seq = fasta_dict[query_id]['seq'][dom_start-6:dom_end+5]
			if dom_num == 1:
				f_out.write('>L1|%s\n%s\n'%(seq_name,seq))
			if dom_num == 2:
				f_out.write('>L2|%s\n%s\n'%(seq_name,seq))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')