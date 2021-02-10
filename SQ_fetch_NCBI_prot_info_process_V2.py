
from os import listdir
# import asn1tools
import json
import argparse
import xmltodict




def main( ):

	input_file = args_.input_argument
	output_file = args_.output_argument

	with open(output_file[0], 'w') as f_out:
		for f in listdir(input_file[0]) : # careful input_file[0] is file path not a file
			print(f)
			# if f != 'P_001165839.1.xml':continue

			in_file = input_file[0] + "/" + f
			myfile = open(in_file,'r')
			doc = xmltodict.parse(myfile.read())
			# json.dump(doc,fout)
			# print(doc)
			root = doc['GBSet']['GBSeq']
			prot_id = root['GBSeq_locus']
			taxa = root['GBSeq_taxonomy']
			table = root['GBSeq_feature-table']['GBFeature']
			# print(table)
			list_of_interest_2 = ['Region','Site','CDS']
			list_of_interest_1 = ['GBFeature_key','GBFeature_quals','GBFeature_location']
			txt =  prot_id +'\t' + f.split('.xml')[0]+ '\t' + taxa + '\t'
			start = False
			for item in table:
				for i in item:	
					if i  in list_of_interest_1:
						if i == 'GBFeature_key':
							if item[i] in list_of_interest_2:
								start = True
								txt += item[i] + '\t'
						elif i == 'GBFeature_location':
							if start == True:
								txt += item[i] + '\t'
						elif i == 'GBFeature_quals':
							word = item[i]['GBQualifier']	
							# print(word)		
							for j in word:
								if (j['GBQualifier_name'] == 'region_name'):
									txt += j['GBQualifier_value'] + '\t'
								elif (j['GBQualifier_name'] == 'site_type'):
									txt += j['GBQualifier_value'] + '\t'
								elif (j['GBQualifier_name'] == 'coded_by' ):
									txt += j['GBQualifier_value'] + '\n'
			f_out.write(txt)

					# if table['GBFeature_key'] == 'Region':
					# 	if table['GBFeature_quals']['GBQualifier']['GBQualifier_name']=='region_name':
					# 		region_name = table['GBFeature_quals']['GBQualifier']['GBQualifier_value']
					# 		region_location = table['GBFeature_quals']['GBQualifier']
					# 		txt += region_name + '\t' + region_name + '\t'

					# if table['GBFeature_key'] == 'Site':
					# 	if table['GBFeature_quals']['GBQualifier']['GBQualifier_name']=='site_type':
					# 		site_name = table['GBFeature_quals']['GBQualifier']['GBQualifier_value']
					# 		site_location = table['GBFeature_quals']['GBQualifier']
					# 		txt += site_name + '\t' + site_location + '\t'

					# if table['GBFeature_key'] == 'CDS':
					# 	if table['GBFeature_quals']['GBQualifier']['GBQualifier_name']=='coded_by':
					# 		translation = table['GBFeature_quals']['GBQualifier']['GBQualifier_value']
					# 		txt += translation + '\t'

if __name__ == "__main__" :
	parser = argparse.ArgumentParser(description="A script to extract Disease Gene Data")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="OM_.txt", help="Check Mesh file and Morbid file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="OM_.txt", help="Check OMIM file")
	args_ = parser.parse_args()

	main(  )
	#print distance('Myasthenic syndrome, congenital, 10, 254300 (3)', 'Myasthenic Syndrome')
	print( 'done' )

