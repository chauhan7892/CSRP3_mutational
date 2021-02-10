import sys, time, os
import argparse
import re


def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	
	organism_common_dict = {

	"Homo sapiens" : 'Human',
	"Pan paniscus" : 'Bonobo',
	"Macaca mulatta" : 'Rhesus macaque',
	"Mus musculus" : 'Mouse',
	"Rattus rattus" : 'Rat',
	"Sus scrofa" : 'Wild boar',
	"Ailuropoda melanoleuca" : 'Giant panda',
	"Myotis myotis" : 'Mouse-eared bats',
	"Phyllostomus discolor" : 'Pale spear-nosed bat',
	"Sarcophilus harrisii" : 'Tasmanian devil',
	"Phascolarctos cinereus" : 'Koala',
	"Vombatus ursinus" : 'Common wombat',
	"Gallus gallus" : 'Red junglefowl',
	"Pygoscelis adeliae" : 'Adelie penguin',
	"Apteryx rowi" : 'Okarito kiwi',
	"Gekko japonicus" : "Schlegel's Japanese gecko",
	"Podarcis muralis" : 'Common wall lizard',
	"Python bivittatus" : 'Burmese python',
	"Protobothrops mucrosquamatus" : 'Brown spotted pit viper',
	"Chelonia mydas" : 'Green sea turtle',
	"Xenopus tropicalis" : 'Western clawed frog',
	"Geotrypetes seraphini" : 'Gaboon caecilian',
	"Danio rerio" : 'Zebrafish',
	"Monopterus albus" : 'Asian swamp eel',
	"Erpetoichthys calabaricus" : 'Reedfish',
	"Amblyraja radiata" : 'Thorny skate',
	"Callorhinchus milii" : 'Australian ghostshark',
	"Latimeria chalumnae" : 'African coelacanth',
	"Crocodylus porosus" : 'Saltwater crocodile',
	"Stylophora pistillata":'hood-coral',
	"Arabidopsis thaliana":'arabidopsis'}

	header = True
	organism_list = []
	with open(input_file[0],'r') as f_in_meg:
		for line in f_in_meg:

			if header == True:
				header = False
				continue

			if line[0]=='#':
				organism_id = line.strip('\n').split('#')[1]
				organism_list.append(organism_id)
	
	with open(input_file[1],'r') as f_in_nwk:
		for line in f_in_nwk:
			#line = re.sub("\s",'_',line)
			line = re.sub("'",'',line)
			# tmp = ''
			for item in organism_list:
				id_and_scientific_name = item.split('|')

				scietific_name = id_and_scientific_name[1].replace('-', ' ')
				commom_name = organism_common_dict[scietific_name]
				id_and_commom_name = id_and_scientific_name[0] + '|' + commom_name
				line = line.replace(item,id_and_commom_name)
				print(item, id_and_commom_name)
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