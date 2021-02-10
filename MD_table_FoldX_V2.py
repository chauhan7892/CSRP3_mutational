import sys, time, os
import argparse
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
	elif (data < -0.46) & (data >= -0.92):
		return(stab_list[4]) # slightly stabilizing
	elif (data < -0.92) & (data >= -1.84):
		return(stab_list[5]) # stabilizing
	else:
		return(stab_list[6]) # highly stabilizing

# function to make tabular info for each mutation with info like Position, delta delta G value, stability
def foldx_process(delta_G_file, mutant_file, phenotype):

	delta_G_list = [] # list to store delta delta G value
	delta_G_stab = [] # list to store category

	pdb_name=delta_G_file.split('.')[0].split('Average_')[1] # model names common term

	with open(delta_G_file, 'r') as f_in_delta_G: #open avg delta delta G file
		for line in f_in_delta_G:
			line = line.strip('\n')
			if re.search(pdb_name, line): # check only models lines
				line = line.split('\t')
				mut_id_AA = line[0].split('_')[-1] # model ID
				delta_G = line[2]	 # delta delta G value			
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
			mut_list.append(mut_info) # update list

	# output data
	output_data = ''

	for item in range(len(delta_G_list)):
		output_data += mut_list[item] + '\t' + delta_G_list[item] + '\t' + delta_G_stab[item]+ '\t' + phenotype + '\n'

	return output_data

def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	delta_delta_HCM = input_file[0] # file containing avg delta delta G info HCM
	delta_delta_DCM = input_file[1] # file containing avg delta delta G info DCM

	mutant_file_HCM = input_file[2] # file containing mutations HCM
	mutant_file_DCM = input_file[3] # file containing mutations DCM
	
	# call foldx_process for HCM
	output_HCM = foldx_process(delta_delta_HCM, mutant_file_HCM, 'HCM')

	# call foldx_process for DCM
	output_DCM = foldx_process(delta_delta_DCM, mutant_file_DCM, 'DCM')

	# output 
	output = 'Mutation' + '\t' + 'Position' + '\t' + 'Delta_Delta_G' + '\t' + 'Feature' + '\t' + 'Phenotype' + '\n'
	
	# append the results
	output += output_HCM + output_DCM

	# write output to a file
	with open(output_file[0], 'w') as f_out:
		f_out.write(output)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make table for plotting foldX data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')