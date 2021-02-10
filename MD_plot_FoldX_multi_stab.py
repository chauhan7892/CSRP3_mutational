
import argparse
import matplotlib.pyplot as plt  
import pandas as pd
import seaborn as sns
from adjustText import adjust_text
from matplotlib import rc, rcParams
# rc('text', usetex=True)
# rc('font', family='serif', serif='cm30') # controls default text sizes      
# rc('axes', labelsize=14) 
# rc('axes', titlesize=20)   # fontsize of the x and y labels
# rc('xtick', labelsize=12)    # fontsize of the tick labels
# rc('ytick', labelsize=12)    # fontsize of the tick labels
# rc('legend', fontsize=10)    # legend fontsize
# rc('figure', titlesize=20)  # fontsize of the figure title

# rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]


def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	foldx_data = pd.read_csv(input_file[0], sep = '\t', header = 0)
	# Extract energy change info 
	# color scheme
	feature_col = {
	'highly de-stabilizing':'#781426',
	'de-stabilizing':'#9F3548',
	'slightly de-stabilizing':'#EFA0AE',
	'neutral':'#000000',
	'slightly stabilizing':'#6FA698',
	'stabilizing':'#256F5C',
	'highly stabilizing':'#2E6E12',
	}
		
#  stability colors


# Prepare data
	x_var = 'Position'
	groupby_var = 'Feature'
	foldx_data_agg = foldx_data.loc[:, [x_var, groupby_var]].groupby(groupby_var)
	vals = [foldx_data[x_var].values.tolist() for i, foldx_data in foldx_data_agg]

	# print vals
	# Draw
	# plt.figure(figsize=(16,9), dpi= 80)
	
	n, bins, patches = plt.hist(vals, foldx_data[x_var].unique().__len__(), stacked=True, density=False)#, color=feature_col[vals])

	# # Decoration
	# plt.legend({group:col for group, col in zip(np.unique(foldx_data[groupby_var]).tolist(), feature_col[:len(vals)])})
	# plt.title(f"Stacked Histogram of ${x_var}$ colored by ${groupby_var}$", fontsize=22)
	# plt.xlabel(x_var)
	# plt.ylabel("Frequency")
	# plt.ylim(0, 40)
	# plt.xticks(ticks=bins, labels=np.unique(foldx_data[x_var]).tolist(), rotation=90, horizontalalignment='left')
	plt.show()


	# ax=sns.scatterplot(data=foldx_data, x="Position", y="Delta_Delta_G", hue="Feature", palette = feature_col, s=120, alpha=0.87)
	# ax.set_facecolor('#FFFFFF')
	# # store text as list for adjust_text module ( change weight( bold, semibold, light) , size (smaller) accordingly)
	# # text_weight = 'normal'  # 'light' # 'semibold' # 'normal'


	# # Now label the axis 
	# ax.set_title(r"\textbf{Mutant Residues Stability}")
	# ax.set_xlabel("Residue position")
	# ax.set_ylabel(r'$\Delta(\Delta G)$ w.r.t wild type')#"Energy difference(kCal) from control",fontsize=14, fontweight='bold' )
	# ax.axhline(-0.46, ls='--', color = '#6FA698', linewidth=1)# stabilizing thres
	# ax.axhline(0.46, ls='--', color = '#EFA0AE', linewidth=1) # de-stabilizing thres


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make plot")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')