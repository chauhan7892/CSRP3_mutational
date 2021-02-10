from modeller import *
import argparse

def ali_file(f_in_query): # auto formating the fasta file to modeller query format
	codes1 = f_in_query.split('/')[-1].split('.')[0] # query name
	seq = ''
	seq += '>P1;' + codes1 + '\n'
	seq += 'sequence:' + codes1 + ':::::::0.00: 0.00' + '\n'

	header = True
	with open(f_in_query, 'r') as f_in:
		for line in f_in:
			if header == True:
				header = False
				continue
			seq += line
		seq_new = seq[:-1]+'*' # ending the modeller query format

	f_out_query = f_in_query.split('.')[0] + '.ali'

	with open(f_out_query, 'w') as f_out: # write modeller query.ali file 
		f_out.write(seq_new)

	return f_out_query, codes1 #return modeller query file full path name and only name 

def pdb_file(f_in_pdb):
	f_out_pdb = f_in_pdb.split('.')[0]
	codes2 = f_out_pdb.split('/')[-1]
	return f_out_pdb, codes2 #return pdb file full path name and only name 


def main( ):

	env = environ()
	aln = alignment(env)
		
	input_file = args_.input_argument
	output_file = args_.output_argument

	f_out_query, codes1 = ali_file(input_file[0])
	f_out_pdb, codes2 = pdb_file(input_file[1])

	chains_to_model = input_file[2] # decide how many chains to model (input a string in capital letters)

	limit = len(chains_to_model)
	start_chain = 'FIRST:'+ chains_to_model[0] 
	end_chain = 'LAST:'+ chains_to_model[limit-1]

	mdl = model(env, file = f_out_pdb, model_segment = (start_chain, end_chain))
	aln.append_model(mdl, align_codes= codes2, atom_files = input_file[1])
	
	aln.append(file = f_out_query, align_codes=codes1)
	aln.align2d()

	out_txt = codes1 + '-' + codes2 # output file name format for easier HM_model_single.py syntax

	pir_file = output_file[0] + '/' + out_txt + '.ali' # HM_align2d.py output file
	pap_file = output_file[0] + '/' + out_txt + '.pap' # HM_align2d.py output file

	aln.write(file = pir_file, alignment_format='PIR')
	aln.write(file = pap_file, alignment_format='PAP')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make model alignment")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')

