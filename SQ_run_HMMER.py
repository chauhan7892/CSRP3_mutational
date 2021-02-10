#!/usr/bin/env python
import sys,os
import argparse


def main( ):
	binary_file = args_.binary_argument
	input_file = args_.input_argument
	output_file = args_.output_argument

	hmmer_exec = binary_file
	max_cpu = 6

	db_file = input_file[0]
	seq_file = input_file[1]
	align_file = output_file[0]
	# 
	domtbl_file = output_file[1]
	# tbl_file = output_file[2]
	# pfam_tbl_file = output_file[3]

	# command = hmmer_exec + ' --cut_ga --cpu ' + str(max_cpu) + ' -o ' + align_file + \
	# ' --tblout ' + tbl_file + ' --domtblout ' + domtbl_file + '--pfamtblout ' + \
	# pfam_tbl_file + ' ' + db_file + ' ' + seq_file

	command = hmmer_exec + ' --cut_ga --cpu ' + str(max_cpu) + ' -o ' + align_file + \
	' --domtblout ' + domtbl_file + ' ' + db_file + ' ' + seq_file
 	os.system(command)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to run hmmer")
	parser.add_argument('-b', dest='binary_argument', help="Put the binary here ")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')