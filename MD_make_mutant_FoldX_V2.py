#!/usr/bin/python
import sys
import re
import argparse
from PD_read_PDB import * # import PBD reader 
from PD_Amino_Acid_dict import *

# function to read mutational list for foldx (mention if chain in pdb file)
def create_mutation_list(input_file, pdb_file, mutant_gene, phenotype, column = 3, split_type = '\t', header = True, chain = 'A'):   

	"""
		 read_PDB(f_in_PDB, atom_type = 1) feature
		 if input is atom type 1 , only backbone in the object
		 if input is atom type 2 , only N, CA and C in the object
		 if input is atom type any other value , all atoms are in the object
		 outputs are an PDB object and chains
	"""
	seq, chains = read_PDB(pdb_file, atom_type = 1) # read PDB file

	chain_ID = chains.index(chain)

	# sequence of the PDB
	seq_used = seq[chain_ID]

	output_individual = ''
	output_missing_AA = ''
	output_phenotype = ''

	pdb_res_info = {} # store pdb residue names in a dictionary with position as key
	for item in range(len(seq_used)):
		pdb_res_info[seq_used[item].rNum] = seq_used[item].rName


	with open(input_file, 'r') as f_in: # read mutation file
		for line in f_in:
			if header == True:
				header = False
				continue
			line = line.strip('\n').split(split_type)
			disease = line[0].strip() # phenotypes in the file

			# match phenotype with phenotype of interest, if no match continue
			if disease not in phenotype: continue
			gene_name = line[1].strip() # genes in the file

			# match gene with gene of interest, if no match continue
			if gene_name != mutant_gene: continue 

			# mutant residues (originalAA + AA_position + mutation_AA)
			mutation_properties = line[column-1] 
			ori_AA = mutation_properties[0]
			ori_AA_Num = mutation_properties[1:-1]

			# match original AA with PDB AA at this position.
			try :
				pdb_rName = pdb_res_info[int(ori_AA_Num)]

				""" If match fill mutation file with original AA, PDB chain, 
				position and current AA in foldx format. Otherwise write to missing AA file"""
				if ori_AA == one_letter[pdb_rName]:
					output_individual += mutation_properties[0] + chain + mutation_properties[1:] + ';' + '\n'
					# output_phenotype += mutation_properties + '\t' + disease + '\n'
				else:
					output_missing_AA += mutation_properties + '\t' + 'mismatch' + '\n'

			except KeyError:
				output_missing_AA += mutation_properties + '\t' + 'missing' + '\n'
				continue

	return output_individual, output_missing_AA, output_phenotype


def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	phenotype_file = input_file[0] # mutational file

	pdb_file = input_file[1] # PDB file 
	chain = input_file[2] # PDB chain of interest
	phenotype = input_file[3].split(':') # phenotype (HCM/DCM) of interest
	mutant_gene = input_file[4] # gene of interest

	# call create_mutation_list function
	output_individual, output_missing_AA, output_phenotype = create_mutation_list(phenotype_file, pdb_file, mutant_gene, phenotype, column = 3, split_type = ',', header = False, chain = chain)

	with open(output_file[0], 'w') as f_out1: # foldx individual_file output
		f_out1.write(output_individual)

	with open(output_file[1], 'w') as f_out2: # missing/mismatch residues in pdb file output
		f_out2.write(output_missing_AA)

	# with open(output_file[2], 'w') as f_out3: # phenotype file
	# 	f_out3.write(output_phenotype)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to make mutation file for foldX input")
    parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
    parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
    args_ = parser.parse_args()
    main(  )
    print('done')
