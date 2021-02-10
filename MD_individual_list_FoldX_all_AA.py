import argparse
import os
from PD_read_PDB import * # import PBD reader 
from PD_Amino_Acid_dict import * # import AA convertion dictionary 


def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	# read pdb file 
	f_in_PDB = input_file[0]

	"""
		 read_PDB(f_in_PDB, atom_type = 1) feature
		 if input is atom type 1 , only backbone in the object
		 if input is atom type 2 , only N, CA and C in the object
		 if input is atom type any other value , all atoms are in the object
		 outputs are an PDB object and chains
	"""
	seq, chains = read_PDB(f_in_PDB, atom_type = 1)
	chain_of_interest = 'A' 
	chain_ID = chains.index(chain_of_interest)

	# sequence of the PDB
	seq_used = seq[chain_ID]


	# residues positions of interest in the sequence
	res_interest = []
	 # iterate over each residues fraction range 
	for file in input_file[1:]:
		new_res_info = file.split('-')
		new_res_start = int(new_res_info[0])-1 # current residues fraction start pos
		new_res_end = int(new_res_info[1]) # residues fraction end pos

		new_res_range = range(new_res_start,new_res_end,1)#create indivial res in current residues fraction
		res_interest.extend(new_res_range) # add to residues positions of interest

	# output directory 
	output_dir_root = output_file[0]

	# iterate over classical 20 AAs
	for res in one_letter.keys():
		if res == 'UNK':continue
		substitite_res = one_letter[res] # one letter name of AA

		# check if current AA directory exist, if not then create one
		res_dir = os.path.join(output_dir_root, res)
		if not os.path.exists(res_dir):
			os.mkdir(res_dir)

		# create mutation file (individual_list) for foldx input
		file_name_res = ('').join([res_dir, '/', 'individual_list_', substitite_res, '.txt'])
		with open(file_name_res, 'w') as f_out:
			
			# iterate over full protein
			# for position in range(len(seq_used)): iterate over full protein

			# iterate over interested residues
			for position in res_interest: 
				original_res = one_letter[seq_used[position].rName] # original AA name 

				# if original AA is same as current AA then ignore
				if original_res == substitite_res:continue

				""" otherwise fill mutation file with original AA, PDB chain, 
				position and current AA in foldx format """
				mutation_info = original_res+'A'+str(position+1)+substitite_res+';'
				# print mutation_info
				f_out.write("%s\n"%(mutation_info))
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make model alignment")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')
