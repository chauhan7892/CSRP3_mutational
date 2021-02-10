import sys, time, os
import argparse
import re
import time


def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument


	header = True
	with open(input_file[0],'r') as f_in_id:
		for line in f_in_id:
			if header == True:
				header = False
				continue
			line_attrs = line.split('\t')
			gene_id = line_attrs[1]
			all_info = 'epost -db nucleotide -id  '+gene_id+' | efetch -format fasta >>' + output_file[0]
			os.system(all_info)
			time.sleep(0.5)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')