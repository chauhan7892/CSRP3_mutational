import sys, time, os
import argparse
import re


def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	fasta_file = input_file[0]

	dom = input_file[1]
	seq = ''
	with open(output_file[0], 'w') as f_out:
		with open( fasta_file, 'r') as f_in_fasta:
			for line in f_in_fasta:
				if line[0] == '>':
					line_atr = line.lstrip('>').split('|')
					if len(line_atr) > 2: 
						line_atr = line_atr[-1]
					else :
						line_atr = ("|").join(line_atr[-2:])
					#print(line_atr)
					if dom == 'LIM1':
						seq_name = '>'+'L1'+'|'+line_atr
					else:
						seq_name = '>'+'L2'+'|'+line_atr
					f_out.write(seq_name)
				else:					
					f_out.write(line)
					


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')