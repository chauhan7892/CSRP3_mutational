import sys, time, os
import argparse
import re


def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument


	# organism_dict = {}
	outdir = output_file[0]

	with open(input_file[0],'r') as f_in_seq_id:
		for line in f_in_seq_id:
			if line[0] == '\n':
				continue
			if line[0]=='>':
				line_attrs = line.split(' ')
				protein_id = line_attrs[0][1:]
				all_info = 'efetch -db protein -id ' + protein_id+' -format xml>' + outdir +'/'+ protein_id +'.xml'
				os.system(all_info)
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')