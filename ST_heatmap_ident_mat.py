import sys, time, os
import argparse,re
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from matplotlib import rc, rcParams

#  set Latex features
     
# plt.rc('axes', labelsize=20)
# plt.rc('axes', titlesize=20)   # fontsize of the x and y labels
# rc('xtick', labelsize=20)    # fontsize of the tick labels
# rc('ytick', labelsize=20)    # fontsize of the tick labels
# rc('legend', fontsize=15)    # legend fontsize
# rc('figure', titlesize=25)  # fontsize of the figure title

# rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
plt.rcParams['text.latex.preamble'] = r'\usepackage{sfmath}'
# matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams.update({"text.usetex": True,"font.family": "sans-serif","font.sans-serif": ["Helvetica"]})

def main( ):

	input_file = args_.input_argument
	output_file = args_.output_argument

	df_dict = {}
	with open(input_file[0],'r') as f_in:
		for line in f_in:
			if line[0] == '#':continue
			if line[0] == '\n':continue
			line = re.sub(r'\s+', '\t', line) 
			line_attrs = line.strip().split('\t')[1:]
			seq_name = str(line_attrs[0].split('|')[-1].split('_')[0])
			values = [float(x) for x in line_attrs[1:]] ## string to float
			df_dict[seq_name] = values

	df_final= pd.DataFrame(df_dict)
	df_final=df_final.transpose()
	print(df_final)
	df_final.columns = df_final.index

	fig = plt.gcf()
	fig.set_size_inches(15, 12)

	# ax = sns.heatmap(df_final)
	ax = sns.heatmap(df_final, cmap="Blues",vmin=0, vmax=100,annot=False,annot_kws={'size':35},square=True,cbar=True,linewidth=0.5,cbar_kws={"shrink": 0.4})

	ax.figure.axes[-1].set_ylabel('% identidy')

	plt.tick_params(axis='x', which='major',  labelbottom = False, bottom=False, top = False, labeltop=True, labelleft=False, left=False)
	plt.tick_params(axis='y', which='major',  labelbottom = False, bottom=False, top = True, labeltop=True, labelleft=False, left=False)
	plt.xticks(rotation=80)
	plt.yticks(rotation=0)

	fig_file_1 = output_file[0]
	plt.savefig(fig_file_1, dpi = 600, bbox_inches='tight')
	plt.close(fig)
	# plt.show()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')