import sys, time, os
import argparse
from PD_Amino_Acid_dict import * # import AA convertion dictionary 
import re

# function to check stability of delta delta G value
def stability_check(data):

	# list for stability categories
	stab_list = ['highly de-stabilizing', 'de-stabilizing', 'slightly de-stabilizing',
	'neutral',
	'slightly stabilizing', 'stabilizing', 'highly stabilizing']

	# stability criterion
	if (data > 1.84):
		return(stab_list[0]) # highly de-stabilizing
	elif (data <= 1.84) & (data > 0.92):
		return(stab_list[1]) # de-stabilizing
	elif (data <= 0.92) & (data > 0.46):
		return(stab_list[2]) # slightly de-stabilizing
	elif (data <= 0.46) & (data > -0.46):
		return(stab_list[3]) # neutral
	elif (data <= -0.46) & (data > -0.92):
		return(stab_list[4]) # slightly stabilizing
	elif (data <= -0.92) & (data > -1.84):
		return(stab_list[5]) # stabilizing
	else:
		return(stab_list[6]) # highly stabilizing

# function to make tabular info for each mutation with info like Position, delta delta G value, stability
def foldx_process(delta_G_file, mutant_file, repair_pdb_name):

	delta_G_list = [] # list to store delta delta G value
	delta_G_stab = [] # list to store category
	repair_pdb_with_no_extention = repair_pdb_name.split('.')[0] # model names common term

	with open(delta_G_file, 'r') as f_in_delta_G: #open avg delta delta G file
		for line in f_in_delta_G:
			line = line.strip('\n')
			if re.search(repair_pdb_with_no_extention, line): # check only models lines
				line = line.split('\t')
				mut_id_AA = line[0].split('_')[-1] # model ID
				delta_G = line[2]	# delta delta G value			
				delta_G_list.append(delta_G) # update list

				# check stability of delta delta G
				stability = stability_check(float(delta_G))
				delta_G_stab.append(stability) # update list

	mut_list = [] # list to store mutation info 

	with open(mutant_file, 'r') as f_in_mut: # open mutation file		
		for line in f_in_mut:
			# mutation as in file containing original AA, PDB chain, position and replaced AA
			mutation = line.strip('\n').split(';')[0] 
			mut_pos = mutation[2:-1] # mutation position

			# original AA,position and replaced AA and position separately
			mut_info = mutation[0] + mutation[2:] + '\t' + mut_pos 
			mut_list.append(mut_info) # append the list

	# output data
	output_data = ''
	for item in range(len(delta_G_list)):
		output_data += mut_list[item] + '\t' + delta_G_list[item] + '\t' + delta_G_stab[item] + '\n'

	return(output_data)

def main( ):
	start_time = time.time() # our scripts start time
	input_file = args_.input_argument
	output_file = args_.output_argument

	# root dicrectory containing all AA folders
	input_dir_root = input_file[0]

	# repair PDB file
	repair_pdb_file = input_file[1]
	repair_pdb_info = os.path.split(repair_pdb_file)
	repair_pdb_name = repair_pdb_info[1]

	output_txt = 'Mutation' + '\t' + 'Position'+ '\t' + 'Delta_Delta_G' + '\t' + 'Feature' + '\n'

	# iterate for all AA folders
	for res in one_letter.keys():
		if res == 'UNK':continue
		substitite_res = one_letter[res]
		res_dir = os.path.join(input_dir_root, res) # current AA folder

		# file containing mutations for current AA folder
		mutant_file = ('').join([res_dir, '/', 'individual_list_', substitite_res, '.txt'])

		# FoldX models directory 
		foldx_dir = ('').join([res_dir, '/', 'foldx_data'])
		
		# avg delta dela G file 
		avg_delta_G_file = ('').join([foldx_dir,'/','Average_',repair_pdb_name])

		# call foldx_process for current AA 
		foldx_result = foldx_process(avg_delta_G_file, mutant_file, repair_pdb_name)

		# append the result 
		output_txt += foldx_result 

	# write output to a file
	with open(output_file[0], 'w') as f_out:
		f_out.write(output_txt)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make make table for foldx energy")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')