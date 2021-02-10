
import argparse
import matplotlib.pyplot as plt  
import pandas as pd
from PD_Amino_Acid_dict import *
from matplotlib.patches import Circle, Wedge
from matplotlib import rc, rcParams
import numpy as np
from collections import OrderedDict

# Latex features
rc('text', usetex=True)
rc('font', family='serif', serif='cm30') # controls default text sizes      
rc('axes', labelsize=14) 
rc('axes', titlesize=20)   # fontsize of the x and y labels
rc('xtick', labelsize=12)    # fontsize of the tick labels
rc('ytick', labelsize=12)    # fontsize of the tick labels
rc('legend', fontsize=10)    # legend fontsize
rc('figure', titlesize=20)  # fontsize of the figure title
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


def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

 	# read foldx avg delta delta G file for all AA
	foldx_data = pd.read_csv(input_file[0], sep = '\t', header = 0)

	# LIM1 data subset contains residues : 10-66
	df1 = foldx_data[(foldx_data['Position'] > 9) & (foldx_data['Position'] <= 66)]
	df1 = df1.reset_index(drop=True)

	# LIM2 Data subset contains residues : 120-176
	df2 = foldx_data[(foldx_data['Position'] > 119) & (foldx_data['Position'] <= 176)]
	df2 = df2.reset_index(drop=True)

	# Empty character matrix to store values
	empty_data = np.chararray((20,57))
	empty_data[:] = ''

	# Fake amino acid coordinate dictionary for plotting
	val = 0
	coord_AA_dict = {}
	for res in three_letter.keys():
		if res == 'X':continue
		coord_AA_dict[res] = val
		val += 1

	# new LIM1 dataframe indexed by AA name and Columns by AA Position
	columns1 = range(10,67,1)
	index = coord_AA_dict.keys()
	df1_final = pd.DataFrame(empty_data, index=index, columns=columns1)

	# LIM1 dataframe filled with LIM1 data subset
	for ii in range(df1.shape[0]):
		subs_AA = df1['Mutation'][ii][-1]
		subs_Pos = df1['Position'][ii]
		subs_Feat = df1['Feature'][ii]
		df1_final.at[subs_AA,subs_Pos]= subs_Feat


	# new LIM2 dataframe indexed by AA name and Columns by AA Position
	columns2 = (range(120,177,1))
	df2_final = pd.DataFrame(empty_data, index=index, columns=columns2)

	# LIM2 dataframe filled with LIM2 data subset
	for ii in range(df2.shape[0]):
		subs_AA = df2['Mutation'][ii][-1]
		subs_Pos = df2['Position'][ii]
		subs_Feat = df2['Feature'][ii]
		df2_final.at[subs_AA,subs_Pos]= subs_Feat

	## Circles plot LIM1 
	fig_file1 = output_file[0]
	fig, ax = plt.subplots(figsize=(24,8))
	ax.set_facecolor('#FFFFFF')

	for ii in range(0,df1_final.shape[0]):    
		for jj in range(0,df1_final.shape[1]):
			if df1_final.iat[ii,jj]:
				full_circle((jj, ii), radius=0.3, colors=feature_col[df1_final.iat[ii,jj]], ax=ax, alpha=0.87)
				ax.axis('equal')
			# else:
			# 	dual_half_circle((jj, ii), radius=0.3, colors=('b','g'), angle=90, ax=ax, alpha=0.87)

	# Add Row Names label
	for ii in range(0,df1_final.shape[0]):       
		plt.annotate(xy= (-1, ii), s= df1_final.index.values[ii], fontsize = 10, verticalalignment='center', horizontalalignment='center')

	# Add Columns label
	for jj in range(0,df1_final.shape[1]):
		if jj % 5 == 0:
			plt.annotate(xy =(jj+0.5, -1), s = df1_final.columns.values[jj], fontsize =9, verticalalignment='center', horizontalalignment='right')

	# add legend for circle colors 
	leg1_loc = 'center right' 
	# The following two lines generate custom fake lines that will be used as legend 2 entries:
	markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='', alpha=0.87) for color in feature_col.values()]
	leg1= ax.legend(markers, feature_col.keys(), numpoints=1, loc=leg1_loc, frameon=False, title=r'\textbf{Stability}')

	# Now check the axis
	ax.set_xlim(-1,58)
	ax.set_ylim(-1,21)
	ax.set_title(r"\textbf{Mutant Residues Stability}")
	plt.axis("off")
	plt.plot([-1,57], [-1,21], alpha=0) # Fake plot to capture everything in the graph
	fig.set_size_inches(15, 5)
	plt.tight_layout()
	plt.savefig(fig_file1, dpi = 300)
	# show the plot
	plt.show()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make plot")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')