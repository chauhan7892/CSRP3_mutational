
import argparse,os
import numpy as np
import pandas as pd
from PD_Amino_Acid_dict import *
from collections import (OrderedDict,Counter)
from matplotlib import rc, rcParams
import matplotlib.pyplot as plt  
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

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

def read_clustal_msa(filepath):

	header = True
	fasta_dict = {}
	with open(filepath, 'r') as f_in_clust_seq:
		for line in f_in_clust_seq:
			if header == True:
				header = False
				continue
			if line[0]=='\n':continue
			if line[0]==' ':continue
			line_attrs = line.strip('\n').split(' ')
			seq_id = line_attrs[0]
			seq = line_attrs[1]
			fasta_dict[seq_id] = seq

	return(fasta_dict)



def aa_freq_fun(input_list):

	L   =  len(input_list) # Number of residues in MSA column
	c = Counter(input_list)
	for letter, count in c.most_common(1):
		# print(letter,count)
		letter, count
	return(letter, count/L)


def freq_letter_msa_fun(alignment):
	"""Calculate Shannon Entropy across the whole MSA"""
	msa_seq = read_clustal_msa(alignment)
	freq_msa_list = []
	aa_msa_list = []
	seq_ids = [seq_id for seq_id in msa_seq]
	# print(len(msa_seq))
	for base_index in range(len(msa_seq[seq_ids[0]])):
	# 	# get list of nucleotides at the current sequence position
		column = [msa_seq[seq_id][base_index] for seq_id in seq_ids]
		letter, count = aa_freq_fun(column)
		freq_msa_list.append(count)
		aa_msa_list.append(letter)

	return(aa_msa_list,freq_msa_list)

def stability(file,foldx_data):

	# Fake amino acid coordinate dictionary for plotting
	val = 0
	coord_AA_dict = {}
	sorted_keys = sorted(CN_AA, key=CN_AA.get)
	for res in sorted_keys:		
		coord_AA_dict[res] = val
		val += 1

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

	destability_list = []
	for subs_Pos in df1_final.columns:
		df = df1_final[subs_Pos][(df1_final[subs_Pos] == 'highly de-stabilizing') | (df1_final[subs_Pos] == 'de-stabilizing')]
		
		destability_list.append(df.shape[0]/19)

	return(destability_list)

def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

 	# read foldx avg delta delta G file for all AA
	foldx_data = pd.read_csv(input_file[0], sep = '\t', header = 0)

	# LIM1 fasta seq
	msa_file_LIM1 = input_file[1]
	region_LIM1 = input_file[2] 
	pos_AA, evolution_AA = freq_letter_msa_fun(msa_file_LIM1)
	stability_AA = stability(region_LIM1,foldx_data)
	

	fig, ax = plt.subplots(figsize=(30,18))
	ax.set_facecolor('#FFFFFF')
	indx = range(0,len(evolution_AA)) 
	plt.plot(indx, stability_AA, label='stability',color = (205/255.0,92/255.0,92/255.0))
	plt.plot(indx, evolution_AA, label='evolution',color = (34/255.0,139/255.0,34/255.0))
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.set_xlabel(r'{Sequence position}', fontdict={'fontsize':25})
	ax.set_ylabel(r'{}', fontdict={'fontsize':25})
	ax.set_xticks(np.arange(len(evolution_AA)))
	ax.set_xticklabels(pos_AA)
	# ax.xaxis.set_major_locator(MultipleLocator(5))
	# ax.xaxis.set_minor_locator(MultipleLocator(1))
	plt.legend()

	fig_file_1 = output_file[0]
	plt.savefig(fig_file_1, dpi = 300) # set dpi of the figure
	plt.show()

	# LIM1 fasta seq
	msa_file_LIM2 = input_file[3]
	region_LIM1 = input_file[4] 
	pos_AA,evolution_AA = freq_letter_msa_fun(msa_file_LIM2)
	stability_AA = stability(region_LIM1,foldx_data)
	

	fig, ax = plt.subplots(figsize=(30,18))
	ax.set_facecolor('#FFFFFF')
	indx = range(0,len(evolution_AA)) 
	plt.plot(indx, stability_AA, label='stability',color = (205/255.0,92/255.0,92/255.0))
	plt.plot(indx, evolution_AA, label='evolution',color = (34/255.0,139/255.0,34/255.0))
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.set_xlabel(r'{Sequence position}', fontdict={'fontsize':25})
	ax.set_ylabel(r'{}', fontdict={'fontsize':25})
	ax.set_xticks(np.arange(len(evolution_AA)))
	ax.set_xticklabels(pos_AA)
	plt.legend()

	fig_file_2 = output_file[1]
	plt.savefig(fig_file_2, dpi = 300) # set dpi of the figure
	plt.show()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make plot")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')