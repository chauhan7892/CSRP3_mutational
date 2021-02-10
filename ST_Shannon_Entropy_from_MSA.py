import sys, time, os
import argparse
import re
import numpy as np 
import math
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.font_manager
from matplotlib import rc, rcParams
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)


#  set Latex features
rc('text', usetex=True)
# # rc('font', family='serif', serif='cm30') # controls default text sizes 
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})       
rc('axes', labelsize=30) 
rc('axes', titlesize=35)   # fontsize of the x and y labels
rc('xtick', labelsize=20)    # fontsize of the tick labels
rc('ytick', labelsize=20)    # fontsize of the tick labels
rc('legend', fontsize=20)    # legend fontsize
# # rc('figure', titlesize=20)  # fontsize of the figure title
# rcParams['text.latex.preamble']=r"\usepackage{amsmath}"
rcParams['text.latex.preamble'] = r'\usepackage{sfmath}'


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


def shannon_entropy(input_list):

	L   =  len(input_list) # Number of residues in MSA column
	unique_base = set(input_list)
	entropy_array = np.empty(len(unique_base))

	for i in range(len(unique_base)):
		n_i = input_list.count(list(unique_base)[i]) # Number of residues of type i
		p_i = n_i/float(L) # prob. of i is n_i(Number of residues of type i) / M(Number of residues in column)
		entropy_i = p_i*(math.log(p_i,2)) # entropy of i is p_i*log2(pi) 
		entropy_array[i] = entropy_i

	sh_entropy = -(np.sum(entropy_array)) # total entropy = negative of sum over p_i*log2(pi) for i = 1:unique_base

	return(sh_entropy)


def shannon_entropy_list_msa(alignment):
	"""Calculate Shannon Entropy across the whole MSA"""
	msa_seq = read_clustal_msa(alignment)
	shannon_entropy_list = []
	seq_ids = [seq_id for seq_id in msa_seq]
	# print(len(msa_seq))
	for base_index in range(len(msa_seq[seq_ids[0]])):
	# 	# get list of nucleotides at the current sequence position
		column = [msa_seq[seq_id][base_index] for seq_id in seq_ids]
		shannon_entropy_list.append(shannon_entropy(column))

	return(shannon_entropy_list)

   
def running_mean(l, N):
	sum = 0
	result = list(0 for x in l)

	for i in range( 0, N ):
		sum = sum + l[i]
		result[i] = sum / (i+1)

	for i in range( N, len(l) ):
		sum = sum - l[i-N] + l[i]
		result[i] = sum / N

	return(result)

def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	fasta_file_1 = input_file[0]
	fasta_file_2 = input_file[1]

	sel1 = shannon_entropy_list_msa(fasta_file_1)
	sel2 = shannon_entropy_list_msa(fasta_file_2)

	fig, ax = plt.subplots(figsize=(30,18))
	ax.set_facecolor('#FFFFFF')
	indx = range(1,len(sel1)+1) 
	plt.plot(indx, sel1, label='LIM1',color = (205/255.0,92/255.0,92/255.0))
	plt.plot(indx, sel2, label='LIM2',color = (34/255.0,139/255.0,34/255.0))
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.set_xlabel(r'{Sequence position}', fontdict={'fontsize':25})
	ax.set_ylabel(r'{Sequence positional entropy}', fontdict={'fontsize':25})

	# ax.set_xlabel(r'{MSA Position Index}', fontdict={'fontsize':25})
	# ax.set_ylabel(r'{Shannon Entropy}', fontdict={'fontsize':25})
	ax.xaxis.set_major_locator(MultipleLocator(5))
	ax.xaxis.set_minor_locator(MultipleLocator(1))
	plt.legend()

	fig_file_1 = output_file[0]
	plt.savefig(fig_file_1, dpi = 300) # set dpi of the figure
	plt.show()
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')