from bs4 import BeautifulSoup
import re
import json
from os import listdir
from collections import OrderedDict
import argparse

def main( ):

	input_file = args_.input_argument
	output_file = args_.output_argument

	# with open(output_file[0], 'w') as f_out1:
	out = output_file[0]

	for f in listdir(input_file[0]) : # careful input_file[0] is file path not a file

		in_file = input_file[0] + "/" + f
		# print (in_file)
		# f_out1.write("Category:%s\n"%(f))

		with open(in_file, 'r') as myfile:
			html_doc=myfile.read()

		soup = BeautifulSoup(html_doc, 'html.parser')
		# print(soup)
		post_content = soup.find("pre", { "class" : "genbank" })

		# organism = re.search("ORGANISM",post_content)
		# print(post_content)

		a_list = post_content.find_all("feature")
		# print(a_list)
		for a in a_list:
			a_out = a.text
			# 	# print a_out
			# 	f_out1.write("%s\n"%(a_out.encode('utf-8')))


if __name__ == "__main__" :
	parser = argparse.ArgumentParser(description="A script to extract Disease Gene Data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="OM_.txt", help="Check Mesh file and Morbid file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="OM_.txt", help="Check OMIM file")
	args_ = parser.parse_args()

	main(  )
	#print distance('Myasthenic syndrome, congenital, 10, 254300 (3)', 'Myasthenic Syndrome')
	print( 'done' )
