import sys, time, os
import argparse
import re

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

	header = True
	with open(output_file[0], 'w') as f_out:
		with open(input_file[1],'r') as f_in_id:
			for line in f_in_id:
				if header == True:
					header = False
					continue
				line_attrs = line.split('\t')
				gene_id = line_attrs[1]
				region = line_attrs[2].split('..')
				reg_start = int(region[0])
				reg_end = int(region[1])
				seq = fasta_dict[gene_id]['seq'][reg_start-1:reg_end]
				f_out.write('>%s\n%s\n'%(gene_id,seq))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')