from modeller import *
from modeller.automodel import *
#from modeller import soap_protein_od
import argparse
import sys

def main( ):

	input_file = args_.input_argument
	output_file = args_.output_argument
	
	align_file = input_file[0] # .ali file containing seq and pdb names 
	all_info = align_file.split('/')[-1]
	seq = all_info.split('-')[0] # query name
	pdb = all_info.split('-')[1].split('.')[0].split(':') # pdb name
	sys.stdout = open(output_file[0], 'w') # log file name

	env = environ()
	a = automodel(env, alnfile= align_file,
		knowns= tuple(pdb), sequence= seq,
		assess_methods=(assess.DOPE,
			#soap_protein_od.Scorer(),
			assess.GA341))
	a.starting_model = 1
	a.ending_model = 5
	a.make()
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make model alignment")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')