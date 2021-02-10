import sys, time, os
import argparse
import re


def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument


	header = True
	organism_dict = {}


	with open(input_file[0],'r') as f_in_fasta:
		for line in f_in_fasta:
			if line[0]=='>':
				line_attrs = line.split('[')
				prot_id_with_dom = line_attrs[0][1:-1]
				prot_id_with_dom = re.sub("\s",'_',prot_id_with_dom)
				organism = line_attrs[1].split(']')[0]
				organism2 = re.sub("\s",'_',organism)
				nwk_id = prot_id_with_dom+'_'+organism2
				organism_taxa = organism2.split('_')
				organism_short = organism_taxa[0][0]+'. '+organism_taxa[1]
				print(prot_id_with_dom)
				organism_dict[nwk_id]= line_attrs[0][1:4]+organism
				print(organism)

	with open(input_file[1],'r') as f_in_nwk:
		for line in f_in_nwk:
			line = re.sub("\s",'_',line)
			line = re.sub("'",'',line)
			# tmp = ''
			for item in organism_dict:
				# print(item, organism_dict[item])
				line = line.replace(item,organism_dict[item])
			# 	line = tmp

	with open(output_file[0], 'w') as f_out:
		f_out.write(line)
					
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to parse data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')