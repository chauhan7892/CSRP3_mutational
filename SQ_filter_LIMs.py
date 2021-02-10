import sys, time, os
import argparse
import re
from SQ_parse_hmmscan import *
import pandas as pd

def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	fasta_file = input_file[0]
	lim_of_interest = input_file[1]

	lim_out_txt = ''

	with open( fasta_file, 'r') as f_in_fasta:
		for line in f_in_fasta:
			line = line.strip('\n')
			if line[0] == '>':
				seq_name = line.strip('\n')
			else:
				seq = line.strip('\n')
				if lim_of_interest == 'LIM1' and seq[-1] == 'Y':
					lim_out_txt += seq_name + '\n' + seq + '\n'
				if lim_of_interest == 'LIM2' and seq[-1] == 'F':
					lim_out_txt += seq_name + '\n' + seq + '\n'

	with open(output_file[0], 'w') as f_out_lim:
		f_out_lim.write(lim_out_txt)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')