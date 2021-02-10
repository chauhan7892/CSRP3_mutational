import sys, time, os
import argparse
import re

species_dict = {
"Homo sapiens":'human',
"Pan paniscus":'bonobo',
"Mus musculus":'mouse',
"Myotis myotis":'mouse-eared-bats',
"Phascolarctos cinereus":'koala',
"Gallus gallus":'red-junglefowl',
"Podarcis muralis":'common-wall-lizard',
"Python bivittatus":'Burmese-python',
"Chelonia mydas":'green-sea-turtle',
"Xenopus tropicalis":'western-clawed-frog',
"Danio rerio":'zebrafish',
"Amblyraja radiata":'thorny-skate',
"Stylophora pistillata":'hood-coral',
"Arabidopsis thaliana":'arabidopsis'}


def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument


	header = True
	organism_dict = {}


	with open(output_file[0], 'w') as f_out:

		with open(input_file[0],'r') as f_in_fasta:
			for line in f_in_fasta:
				if line[0] == '\n':continue
				if line[0]=='>':
					line_attrs = line.split('[')
					prot_id_with_dom = line_attrs[0][0:-1]
					prot_id = prot_id_with_dom.split(' ')[0]
					organism = line_attrs[1].split(']')[0]
					organism_common = species_dict[organism]
					print(organism_common)
					f_out.write('>'+organism_common+'\n')
				else:
					f_out.write(line)

				
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')