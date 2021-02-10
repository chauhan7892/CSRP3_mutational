import sys, time, os
import argparse
import re

def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	header_flag = True
	# subject_list = []

	with open(input_file[0], 'r') as f_in_blast:
		subj_seq = []
		subj_pos = []
		seq_name = ''
		name_flag = True

		for line in f_in_blast:
			if line[0] == '>': 
				header_flag = False	
				name_flag = True
				if subj_seq:
					print subj_name
					print subj_pos
					print subj_seq
					
					subj_seq = []
					subj_pos = []	

			if header_flag == True: continue					

			if line[0:6] == 'Length':
				subj_name = seq_name
				name_flag = False
				seq_name = ''

			if name_flag == True:
				seq_name += line.strip('\n')


			if line[0:5] == 'Query':
				query = line.strip('\n').split()
				query_start = int(query[1])
				query_seq = query[2]
				query_end = int(query[3])

				
			if line[0:5] == 'Sbjct':
				if query_start !=1 or query_end != 57: continue
				subject = line.strip('\n').split()				
				subject_start = subject[1]	
				subject_seq	= subject[2]	
				subject_end = subject[3]
				subj_seq.append(subject_seq)
				subj_pos.append(subject_start+':'+subject_end)
			# seq_name += line.strip('\n')
		print subj_name
		print subj_pos
		print subj_seq
		
			






if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')