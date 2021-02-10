import sys, time, os
import argparse,re
import pandas as pd
import numpy as np
import seaborn as sns
#import matplotlib
# matplotlib.use('Agg')
import matplotlib as mpl
from PD_Amino_Acid_dict import *
import matplotlib.pyplot as plt
from matplotlib import rc, rcParams
from matplotlib.collections import PatchCollection
#  set Latex features
rc('text', usetex=False)
rc('font', family='serif', serif='Times') # controls default text sizes      
rc('axes', labelsize=20)
rc('axes', titlesize=20)   # fontsize of the x and y labels
rc('xtick', labelsize=20)    # fontsize of the tick labels
rc('ytick', labelsize=20)    # fontsize of the tick labels
rc('legend', fontsize=15)    # legend fontsize
# rc('figure', titlesize=25)  # fontsize of the figure title

# rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
rcParams['text.latex.preamble'] = r'\usepackage{sfmath}'
# matplotlib.rcParams['axes.unicode_minus'] = False

def read_prot_param(input_file):

	flag = False
	freq_dict = {}
	with open(input_file,'r') as f_in:
		for line in f_in:
			if line[0:5] == 'Amino':
				flag = True
				continue
			if line[0:3] == 'Pyl':
				flag = False
				continue

			if flag == True:
				line = re.sub(r'\s+', '\t', line) 
				line_attrs = line.strip().split('\t')
				AA_3_letter_name = line_attrs[0].upper()
				AA_name = one_letter[AA_3_letter_name]
				AA_freq = int(line_attrs[2])
				freq_dict[AA_name] = AA_freq

	return(freq_dict)


def main( ):

	input_file = args_.input_argument
	output_file = args_.output_argument


	SRP1 = read_prot_param(input_file[0])
	SRP2 = read_prot_param(input_file[1])
	SRP3 = read_prot_param(input_file[2])

	val = 0
	coord_AA_dict = {}
	df_dict = {}
	sorted_keys = sorted(CN_AA, key=CN_AA.get)

	for res in sorted_keys:		
		coord_AA_dict[res] = val
		df_dict[res] = [SRP1[res],SRP2[res],SRP3[res]]
		val += 1

	df_1 = pd.DataFrame(df_dict)
	df_1.index = ['CSRP1','CSRP2','CSRP3']
	df_final = df_1.transpose()/df_1.sum(axis =1)
	# print(df_final.values)
	df_final = df_final.transpose()

	ylabels = df_final.index
	xlabels = df_final.columns

	M = df_final.shape[1]
	N = df_final.shape[0]
	x, y = np.meshgrid(np.arange(M), np.arange(N))
	## scale values (100x) for better barplot 
	s = df_final.values*100
	c = df_final.values*100 -0.5

	fig, ax = plt.subplots(figsize=(10,100))

	R = s/s.max()/2 - 0.005

	circles = [plt.Circle((j,i), radius=r) for r, j, i in zip(R.flat, x.flat, y.flat)]
	col = PatchCollection(circles, array=c.flatten(), cmap="Greens", clim = (-5,s.max()))#BrBG_r
	ax.add_collection(col)
	ax.set(xticks=np.arange(M), yticks=np.arange(N),
	       xticklabels=xlabels, yticklabels=ylabels)
	ax.set_xticks(np.arange(M+1)-0.5, minor=True)
	ax.set_yticks(np.arange(N+1)-0.5, minor=True)
	ax.grid(which='minor')
	ax.set_aspect('equal')
	fig.colorbar(col, orientation='horizontal', fraction=0.1)

	plt.show()

	fig_file_1 = output_file[0]
	# plt.savefig(fig_file_1, dpi = 600, box_inches='tight')
	# plt.close(fig)
	# plt.show()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')