
import argparse
import pandas as pd
import seaborn as sns
from adjustText import adjust_text
from matplotlib import rc, rcParams
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt  

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', serif='cm30')
rc('axes', labelsize=20)
rc('axes', titlesize=20)   # fontsize of the x and y labels
rc('xtick', labelsize=18)    # fontsize of the tick labels
rc('ytick', labelsize=18)    # fontsize of the tick labels
rc('legend', fontsize=18)    # legend fontsize
# plt.rc('figure', titlesize=25)  # fontsize of the figure title
# rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
rcParams['text.latex.preamble'] = r'\usepackage{sfmath}'

# rcParams.update({
#     "text.usetex": True,
#     "font.family": "serif",
#     "font.serif": ["Times"],
# })
rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})
#  phenotype colors dictionary
phenotype_col = {'HCM':'#3366CC', 'DCM':'#4E9231'} # phenotypes colors
	
#  stability colors dictionary
feature_col = {
'highly de-stabilizing':'#781426',
'de-stabilizing':'#9F3548',
'slightly de-stabilizing':'#EFA0AE',
'neutral':'#000000',
'slightly stabilizing':'#6FA698',
'stabilizing':'#256F5C',
'highly stabilizing':'#2E6E12',
}

def main( ):

	input_file = args_.input_argument
	output_file = args_.output_argument

	# read foldx avg delta delta G info file
	df_final = pd.read_csv(input_file[0], sep = '\t', header = 0)

	# sort the values based on delta delta G
	df_final.sort_values(by=['Delta_Delta_G'],inplace=True, ascending=False)

	# saving important mutant residues
	imp_res_out_txt = ''

	# Graph
	# scatterplot
	ax=sns.scatterplot(data=df_final, x="Position", y="Delta_Delta_G", hue="Feature", palette = feature_col, s=120, alpha=0.87)
	# set background color
	ax.set_facecolor('#FFFFFF')

	# add labels to points
	texts = []
	for i in range(0,df_final.shape[0]):
		label_x = df_final.Position[i]+0.5 # label x-coord
		label_y = df_final.Delta_Delta_G[i] # label y-coord
		label = df_final.Mutation[i] # label name
		label_col = phenotype_col[df_final.Phenotype[i]] # label color
		if df_final.Feature[i] == 'neutral': # if label is neutal then hide it
			label = ''	
		else: # record important mutant residues
			imp_res_out_txt += label + '\t' + df_final.Phenotype[i]+ '\n'

		texts.append(ax.text(label_x, label_y, label, color = label_col, alpha=1,fontsize=18))


	# adjust the text labels using adjust_text 
	adjust_text(texts)

	# define first legend's position and show the legend
	leg1_loc='center right'
	leg1 = ax.legend(loc = leg1_loc, frameon=False)
	# leg1 = ax.legend(loc=(820, 20), frameon=False)

	# define second legend's position and show the legend
	leg2_loc = 'upper right' # 'lower left' # 
	# The following two lines generate custom fake lines that will be used as legend 2 entries:
	markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='', alpha=0.87) for color in phenotype_col.values()]
	leg2= ax.legend(markers, phenotype_col.keys(), numpoints=1, loc=leg2_loc, frameon=False, title=r'\textbf{Phenotype}')

	# leg1 will be removed from figure
	# Manually add the first legend back
	ax.add_artist(leg1)

	# Now label the axis 
	ax.set_title(r"\textbf{Mutant Residues Stability}")
	ax.set_xlabel("Residue position")
	# ax.set_ylabel(r'$\Delta\Delta G$ kcal/mol w.r.t wild type')#"Energy difference(kCal) from control",fontsize=14, fontweight='bold' )
	ax.set_ylabel(r'$\Delta\Delta G$ kcal/mol')#"Energy difference(kCal) from control",fontsize=14, fontweight='bold' )
	ax.axhline(-0.46, ls='--', color = '#6FA698', linewidth=1)# stabilizing thres
	ax.axhline(0.46, ls='--', color = '#EFA0AE', linewidth=1) # de-stabilizing thres
	# remove top and right axes
	sns.despine()

	# save the plot
	fig_file = output_file[0]
	figure = plt.gcf() # get current figure
	figure.set_size_inches(8, 5)
	plt.savefig(fig_file, dpi = 300)#, box_inches='tight')
	# show the plot
	plt.show()

	# file for saving important residues
	res_of_int_file = output_file[1]
	with open( res_of_int_file, 'w') as f_out:
		f_out.write(imp_res_out_txt)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make plot")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')