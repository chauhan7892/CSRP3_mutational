import numpy as np
import argparse,re
from PD_read_PDB import * # import PBD reader 
from PD_Amino_Acid_dict import * # import AA convertion dictionary 

def main( ):

	input_file = args_.input_argument
	output_file = args_.output_argument

	f_in_PDB = input_file[0]
	seq, chains = read_PDB(f_in_PDB, atom_type = 1)

	chain_of_interest = 'A' 
	chain_ID = chains.index(chain_of_interest)
	seq_used = seq[chain_ID]

	seq_txt = '>' + f_in_PDB.split('/')[-1].split('.')[0] + '\n'
	for item in range(len(seq_used)):
		three_let_name = (seq_used[item].rName)
		one_let_name = one_letter[three_let_name]
		seq_txt += one_let_name
	seq_txt += '\n'

	with open(output_file[0],'w') as f_out:
		f_out.write(seq_txt)
		
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')