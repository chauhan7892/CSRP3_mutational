import sys, time, os
import argparse
import re

def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	fasta_file = input_file[0]

	seq = ''
	seq_id = ''
	fasta_dict = {}

	with open( fasta_file, 'r') as f_in_fasta:
		for line in f_in_fasta:
			line = line.strip('\n')
			if line[0] == '>':
				if seq and seq_id:
					fasta_dict[seq_id] = {}
					fasta_dict[seq_id]['name'] = seq_id
					fasta_dict[seq_id]['seq'] = seq
					seq = ''
				try:
					seq_id = line.split('{')[1].split(':')[-1].split('}')[0]	
					#print seq_id	
				except IndexError:
					seq_id = ''
					continue
			else:
				seq += line

		fasta_dict[seq_id] = {}
		fasta_dict[seq_id]['name'] = seq_id
		fasta_dict[seq_id]['seq'] = seq

	with open(output_file[0], 'w') as f_out:
		for query_id in fasta_dict:
			seq_name = fasta_dict[query_id]['name']
			seq = fasta_dict[query_id]['seq']
			out_txt = '>' + seq_name + '\n' + seq + '\n'
			f_out.write(out_txt)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')