
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

	# read foldx avg delta delta G file for all AA
	foldx_data = pd.read_csv(input_file[0], sep = '\t', header = 0)

	fig_dir = output_file[0] # directory for figures output

	fig_specific_chunk = output_file[1] # graph type hint

	# iterate over each residues fraction range 
	for file in input_file[1:]:
		new_res_info = file.split('-')
		new_res_start = int(new_res_info[0])-1 # current residues fraction start pos
		new_res_end = int(new_res_info[1]) # residues fraction end pos

		# copy data to avoid data value leaks
		foldx_data_copy = foldx_data.copy()

		# get data for specific residues fraction 
		df1 = foldx_data_copy[(foldx_data_copy['Position'] > new_res_start) & (foldx_data_copy['Position'] <= new_res_end)]
		df1 = df1.reset_index(drop=True)

		# sns.set()
		# df1.groupby(['Position','Feature']).size().unstack().plot(kind='bar',stacked=True, colormap ='PiYG',legend=True, alpha=0.87)
		
		# aggregate by Position to and Feature to find freq of each category at the particular position
		df2 = df1.groupby(['Position','Feature']).size().unstack()
		df2.fillna(0, inplace=True) # replace NAN with zeros

		data_feat = set(df1['Feature'])
		sorting_list = []
		for key in feature_col:
			if key in data_feat:
				sorting_list.append(key)

		df2 = df2[sorting_list] # re-order dataframe columns based on required order

		bottom_val = [0]*df2.shape[0] #list to store cumulative fraction value for each category at the position
		index_pos = 0

		# graph 		
		fig, ax = plt.subplots(figsize=(24,18))
		ax.set_facecolor('#FFFFFF')
		for category in sorting_list:
			# bar plot
			# plt.bar(df2.index.values,(df2.loc[:,category]/19.0)*100, bottom = bottom_val, color = feature_col[category],alpha=0.87)
			# bottom_val += (df2.iloc[:,index_pos]/19.0)*100

			plt.bar(df2.index.values,df2.loc[:,category], bottom = bottom_val, color = feature_col[category],alpha=0.87)
			bottom_val += df2.iloc[:,index_pos]

			# print bottom_val
			index_pos += 1


		# indices for axes
		x_indices = [list(df2.index.values)[0],list(df2.index.values)[-1]]
		y_indices = [0,int(bottom_val.iloc[0])]

		# add legend 
		leg1_loc = 'lower center' 
		# The following two lines generate custom fake lines that will be used as legend 2 entries:
		markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='', alpha=0.87) for color in feature_col.values()]
		leg1= ax.legend(markers, feature_col.keys(), columnspacing = 0.7,\
			handletextpad=0.08, numpoints=1, ncol=len(feature_col),\
			loc=leg1_loc,frameon=False, title=r'\Large\textbf{Stability}')

		# set axes properties
		ax.set_xlim(x_indices[0]-0.5,x_indices[1]+0.5)
		ax.set_ylim(y_indices[0],y_indices[1])
		ax.spines['right'].set_visible(False)
		ax.spines['top'].set_visible(False)
		ax.set_title(r"\textbf{Positional Stability}")
		ax.set_xlabel("Residue position")
		ax.set_ylabel("Number of each stability category")

		fig.set_size_inches(15, 5)
		fig_name = ('').join([fig_specific_chunk, file,'.png'])
		fig_file = os.path.join(fig_dir, fig_name) 
		plt.savefig(fig_file, dpi = 300)
		# show the plot
		plt.show()



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make plot")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')