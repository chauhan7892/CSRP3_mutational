
from os import listdir
# import asn1tools
import json
import argparse
import xmltodict




def main( ):

	input_file = args_.input_argument
	output_file = args_.output_argument

	with open(output_file[0], 'w') as f_out:
		f_out.write('%s\t%s\t%s\n'%('prot_id','cds_id','protein_coding_region'))
		with open(input_file[0],'r') as f_in_info:
			for line in f_in_info:
				line_attrs = line.strip('\n').split('\t')
				prot_id = line_attrs[1]
				cds_info = line_attrs[-1].split(':')
				cds_id = cds_info[0]
				protein_coding_region = cds_info[1]
				f_out.write('%s\t%s\t%s\n'%(prot_id,cds_id,protein_coding_region))


if __name__ == "__main__" :
	parser = argparse.ArgumentParser(description="A script to extract Disease Gene Data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="OM_.txt", help="Check Mesh file and Morbid file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="OM_.txt", help="Check OMIM file")
	args_ = parser.parse_args()

	main(  )
	#print distance('Myasthenic syndrome, congenital, 10, 254300 (3)', 'Myasthenic Syndrome')
	print( 'done' )

