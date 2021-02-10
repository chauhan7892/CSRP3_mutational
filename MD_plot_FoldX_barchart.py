
import argparse
import matplotlib.pyplot as plt  
import pandas as pd
from matplotlib import rc, rcParams
import os
from collections import OrderedDict
rc('text', usetex=True)
rc('font', family='serif', serif='cm30') # controls default text sizes      
rc('axes', labelsize=14) 
rc('axes', titlesize=20)   # fontsize of the x and y labels
rc('xtick', labelsize=12)    # fontsize of the tick labels
rc('ytick', labelsize=12)    # fontsize of the tick labels
rc('legend', fontsize=10)    # legend fontsize
rc('figure', titlesize=20)  # fontsize of the figure title

rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]

#  stability colors dictionary
feature_col = OrderedDict() 
feature_col['highly de-stabilizing']='#781426'
feature_col['de-stabilizing']='#9F3548'
feature_col['slightly de-stabilizing']='#EFA0AE'
feature_col['neutral']='#808080'
feature_col['slightly stabilizing']='#6FA698'
feature_col['stabilizing']='#256F5C'
feature_col['highly stabilizing']='#2E6E12'

def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	foldx_data = pd.read_csv(input_file[0], sep = '\t', header = 0)

	fig_dir = output_file[0] # directories for figures output
	fig_specific_chunk = output_file[1]


	for file in input_file[1:]:
		new_res_info = file.split('-')
		new_res_start = int(new_res_info[0])-1 # current residues fraction start pos
		new_res_end = int(new_res_info[1]) # residues fraction end pos

		foldx_data_copy = foldx_data.copy()
		df1 = foldx_data_copy[(foldx_data_copy['Position'] > new_res_start) & (foldx_data_copy['Position'] <= new_res_end)]
		df1 = df1.reset_index(drop=True)

		# sns.set()
		# df1.groupby(['Position','Feature']).size().unstack().plot(kind='bar',stacked=True, colormap ='PiYG',legend=True, alpha=0.87)
		df2 = df1.groupby(['Position','Feature']).size().unstack()
		df2.fillna(0, inplace=True)
		df2 = df2[feature_col.keys()]

		bar_positions = range(0, df2.shape[0],1)

		bottom_val = [0]*df2.shape[0]
		index_pos = 0

		fig, ax = plt.subplots(figsize=(24,8))
		ax.set_facecolor('#FFFFFF')
		for category in feature_col:
			plt.bar(bar_positions,df2.loc[:,category], bottom = bottom_val, color = feature_col[category])
			bottom_val += df2.iloc[:,index_pos]
			# print bottom_val
			index_pos += 1

		# Add Row Names label
		for ii in bar_positions:
			if ii % 5 == 0:
				plt.annotate(xy= (ii,-1), s=df2.index.values[ii], fontsize = 13, verticalalignment='center', horizontalalignment='center')

		# Add Column Names label
		for jj in range(0, 19,1):
			if jj % 5 == 0:
				plt.annotate(xy= (-1, jj), s=jj, fontsize = 13, verticalalignment='center', horizontalalignment='center')

		# add legend for 
		leg1_loc = 'center right' 
		# The following two lines generate custom fake lines that will be used as legend 2 entries:
		markers = [plt.Line2D([0,1],[0,1],color=color, marker='o', linestyle='', alpha=0.87) for color in feature_col.values()]
		leg1= ax.legend(markers, feature_col.keys(), numpoints=1, loc=leg1_loc, frameon=False, title=r'\textbf{Stability}')


		ax.set_xlim(-1,df2.shape[0]+1)
		ax.set_ylim(-1,19+1)
		ax.set_title(r"\textbf{Mutant Residues Stability Frequency}")
		plt.axis("off")

		# plt.plot([-1,df2.shape[0]+6], [-1,19+1], alpha=0)
		
		fig.set_size_inches(15, 5)
		plt.tight_layout()

		plt.show()



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make plot")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')