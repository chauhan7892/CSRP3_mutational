import sys, time, os
import argparse
import re


def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	fasta_file = input_file[0]
	seq = ''
	with open(output_file[0], 'w') as f_out:
		with open( fasta_file, 'r') as f_in_fasta:
			for line in f_in_fasta:
				if line[0] == '>':
					if seq:
						# print seq_new_name
						f_out.write(seq_new_name)
						f_out.write(seq)
					seq_full_name = line
					seq_name = seq_full_name.split('_')
					dom = seq_name[0]
					species = seq_name[2].split()[0]
					seq_new_name = dom +'_'+species+ '\n'
					seq = ''
								
				else:
					seq += line
					


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')