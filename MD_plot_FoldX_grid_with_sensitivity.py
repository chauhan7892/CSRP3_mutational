
import argparse
import matplotlib.pyplot as plt  
import pandas as pd
from PD_Amino_Acid_dict import *
from matplotlib.patches import Circle, Wedge
from matplotlib import rc, rcParams
import numpy as np
from collections import OrderedDict
import os
# Latex features
rc('text', usetex=True)
rc('font', family='serif', serif='cm30') # controls default text size    
rc('axes', labelsize=16) 
rc('axes', titlesize=20)   # fontsize of the x and y labels
rc('xtick', labelsize=12)    # fontsize of the tick labels
rc('ytick', labelsize=12)    # fontsize of the tick labels
rc('legend', fontsize=14)    # legend fontsize
rc('figure', titlesize=25)  # fontsize of the figure title

rcParams['axes.titlepad'] = 5
# rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]

#  stability colors dictionary
feature_col = OrderedDict() 
feature_col['highly de-stabilizing']='#781426'
feature_col['de-stabilizing']='#9F3548'
feature_col['slightly de-stabilizing']='#EFA0AE'
feature_col['neutral']='#808080'
feature_col['slightly stabilizing']='#6FA698'
feature_col['stabilizing']='#256F5C'
feature_col['highly stabilizing']='#2E6E12'

AA_col = {
	'R':'green',
	'C':'red',
	'P':'blue',
	'N':'black'
}

def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument
 	# read foldx avg delta delta G file for all AA
	foldx_data = pd.read_csv(input_file[0], sep = '\t', header = 0)

	# Fake amino acid coordinate dictionary for plotting
	val = 0
	coord_AA_dict = {}
	sorted_keys = sorted(CN_AA, key=CN_AA.get)
	for res in sorted_keys:		
		coord_AA_dict[res] = val
		val += 1

	# iterate over each residues fraction range 

	out_txt = 'Column' + '\t' + 'Sensitive_values' + '\n'
	for file in input_file[1:]:
		new_res_info = file.split('-')
		new_res_start = int(new_res_info[0])-1 # current residues fraction start pos
		new_res_end = int(new_res_info[1]) # residues fraction end pos
		# foldx_data2 = foldx_data.copy()
		df1 = foldx_data[(foldx_data['Position'] > new_res_start) & (foldx_data['Position'] <= new_res_end)]
		df1 = df1.reset_index(drop=True)
		# Empty character matrix to store values
		new_res_len = new_res_end-new_res_start

		# empty_data = np.array((20,new_res_len))
		empty_data = np.empty((20,new_res_len),dtype='str')

		# new dataframe indexed by AA name and Columns by AA Position
		columns1 = range(new_res_start+1,new_res_end+1,1)
		index = sorted_keys
		df1_final = pd.DataFrame(empty_data, index=index, columns=columns1)

		# # new dataframe filled with residues of interest data subset
		for ii in range(df1.shape[0]):
			subs_AA = df1['Mutation'][ii][-1]
			subs_Pos = df1['Position'][ii]
			subs_Feat = df1['Feature'][ii]
			df1_final.at[subs_AA,subs_Pos]= str(subs_Feat)

		for col in df1_final.columns:
			destability_value = ((df1_final[col]== 'highly de-stabilizing') | (df1_final[col]== 'de-stabilizing')).sum()
			if destability_value/19 >= 0.75:
				sensitive_value = 'S'
			else:
				sensitive_value = 'N'
			out_txt += str(col) + '\t' + sensitive_value + '\n'

	with open(output_file[0], 'w') as f_out:
		f_out.write(out_txt)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make plot")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')