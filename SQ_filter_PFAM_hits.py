import sys, time, os
import argparse
import re
from SQ_parse_hmmscan_V2 import *
import pandas as pd

def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	domtbl_out_file = input_file[0]
	
	domtbl_list = domtbl_parse(domtbl_out_file) 
	df = pd.DataFrame.from_records(domtbl_list)

	df.columns = ['#dom','t_access', 'dom_len', 'q_id', 'q_access', 'q_len',\
					'seq_Eval', 'seq_score', 'seq_bias', 'dom_num', 'dom_total', \
					'dom_c_Eval', 'dom_i_Eval', 'dom_score', 'dom_bias', \
					'hmm_start', 'hmm_end', 'ali_start', 'ali_end', 'dom_start', 'dom_end',\
					'acc', 'desc']

	# df_filt1 = df[(((df['hmm_end']-df['hmm_start']) + 1)/(df['dom_len'])*1.0 >= 0.999) & (((df['hmm_end']-df['hmm_start']) + 1)/(df['dom_len'])*1.0 < 1.0001) & (df['dom_i_Eval'] < 0.0001)]

	df_filt1 = df[(((df['dom_end']-df['dom_start']) + 1)== df['dom_len']) & (df['dom_i_Eval'] < 0.001)]

	df_filt1 = df_filt1.reset_index(drop=True)

	df_filt2 = df_filt1[df_filt1['dom_c_Eval'] == df_filt1.groupby(['q_id'])['dom_c_Eval'].transform(min)]
	df_filt2 = df_filt2.sort_values('dom_c_Eval').drop_duplicates('q_id')

	# df1 = df[(((df['hmm_end']-df['hmm_start']) + 1)/(df['dom_len'])*1.0 > 0.99) & (df['dom_i_Eval'] < 0.001)]
	# df1 = df1.reset_index(drop=True)

	df_filt2.to_csv(output_file[0], index = None, sep = ' ', header=True)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')