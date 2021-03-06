
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
# function to draw two half circles
def dual_half_circle(center, radius, angle=0, ax=None, colors=('w','k'), **kwargs):
	"""
	Add two half circles to the axes *ax* (or the current axes) with the 
	specified facecolors *colors* rotated at *angle* (in degrees).
	"""
	if ax is None:
		ax = plt.gca()
	theta1, theta2 = angle, angle + 180
	w1 = Wedge(center, radius, theta1, theta2, fc=colors[0], **kwargs)
	w2 = Wedge(center, radius, theta2, theta1, fc=colors[1], **kwargs)
	for wedge in [w1, w2]:
		ax.add_artist(wedge)
	return [w1, w2]

# function to draw full circle
def full_circle(center, radius, ax=None, colors=('w'), **kwargs):
	if ax is None:
		ax = plt.gca()
	c = Circle(center, radius, fc=colors, **kwargs)
	ax.add_artist(c)


def grid_plot(df1_final, feature_col, fig_dir, fig_specific_chunk, file):
	fig, ax = plt.subplots(figsize=(15,8))
	ax.set_facecolor('#FFFFFF')

	for ii in range(0,df1_final.shape[0]):    
		for jj in range(0,df1_final.shape[1]):
			if df1_final.iat[ii,jj]:
				full_circle((jj, ii), radius=0.4, colors=feature_col[df1_final.iat[ii,jj]], \
					ax=ax, alpha=0.87)
				ax.axis('equal')
			# else:
			# 	dual_half_circle((jj, ii), radius=0.3, colors=('b','g'), angle=90, ax=ax, alpha=0.87)

	# Add Row Grids and Names label
	for ii in range(0,df1_final.shape[0]): 
		plt.plot([-0.5,df1_final.shape[1]-0.5],[ii-0.5, ii-0.5], 'b-', alpha=0.33)  # add grid
		# add label   
		plt.annotate(xy= (-1, ii), text= df1_final.index.values[ii], fontsize = 14, \
			color = AA_col[CN_AA[df1_final.index.values[ii]]], verticalalignment='center', \
			horizontalalignment='center')
	 # add last row grid
	plt.plot([-0.5,df1_final.shape[1]-0.5],[df1_final.shape[0]-0.5, df1_final.shape[0]-0.5], \
		'b-', alpha=0.33)
	
	# Add Columns Grids and Names label
	for jj in range(0,df1_final.shape[1]):
		plt.plot([jj-0.5, jj-0.5], [-0.5,df1_final.shape[0]-0.5],'b-', alpha=0.33) # add grid
		# add label at interval of five
		if jj % 5 == 0:
			plt.annotate(xy =(jj, -1), text = df1_final.columns.values[jj], fontsize = 14, \
				verticalalignment='center', horizontalalignment='center')
	 # add last column grid
	plt.plot([df1_final.shape[1]-0.5, df1_final.shape[1]-0.5], [-0.5,df1_final.shape[0]-0.5],\
		'b-', alpha=0.33)
	
	# add legend for circle colors 
	leg1_loc = 'lower center' 
	# The following two lines generate custom fake lines that will be used as legend 2 entries:
	markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='', alpha=0.87) for color in feature_col.values()]
	leg1= ax.legend(markers, feature_col.keys(), columnspacing = 0.7,\
		handletextpad=0.08, numpoints=1, ncol=len(feature_col),\
		loc=leg1_loc,frameon=False, title=r'\Large\textbf{Stability}')

	# Now check the axis
	ax.set_xlim(-1,df1_final.shape[1]+1)
	ax.set_ylim(-1,df1_final.shape[0]+1)
	ax.set_title(r"\textbf{Mutant Residues Stability}")
	plt.axis("off")
	# plt.plot([-1,df1_final.shape[1]+1], [-1,df1_final.shape[0]+1], alpha=0) # Fake plot to capture everything in the graph
	plt.subplots_adjust(top=0.7) 
	fig.set_size_inches(15, 8)
	plt.tight_layout()
	fig_name = ('').join([fig_specific_chunk, file,'.png'])
	fig_file = os.path.join(fig_dir, fig_name) 
	plt.savefig(fig_file, dpi = 300)
	# show the plot
	plt.show()


def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

 	# read foldx avg delta delta G file for all AA
	foldx_data = pd.read_csv(input_file[0], sep = '\t', header = 0)

	fig_dir = output_file[0] # directory for figures output
	fig_specific_chunk = output_file[1]


	# Fake amino acid coordinate dictionary for plotting
	val = 0
	coord_AA_dict = {}
	sorted_keys = sorted(CN_AA, key=CN_AA.get)
	for res in sorted_keys:		
		coord_AA_dict[res] = val
		val += 1

	# iterate over each residues fraction range 

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

		## Circles plot for the residues of interest
		grid_plot(df1_final, feature_col, fig_dir, fig_specific_chunk, file)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make plot")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')