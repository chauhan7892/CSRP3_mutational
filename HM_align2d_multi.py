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
	env.libs.topology.read(file='$(LIB)/top_heav.lib')
	env.io.atom_files_directory = ['./', '../atom_files/']
	aln = alignment(env)
		
	input_file = args_.input_argument
	output_file = args_.output_argument

	pdb_entries = len(input_file)

	f_out_query, codes1 = ali_file(input_file[0])

	out_txt = codes1 + '-' # output file name format for easier HM_model_single.py syntax

	for entry in range(1, pdb_entries, 2):
		f_out_pdb, codes2 = pdb_file(input_file[entry])
		out_txt += codes2+':'
		chains_to_model = input_file[entry + 1] # decide how many chains to model (input a string in capital letters)
		limit = len(chains_to_model)
		start_chain = 'FIRST:'+ chains_to_model[0] 
		end_chain = 'LAST:'+ chains_to_model[limit-1]
		mdl = model(env, file = f_out_pdb, model_segment=(start_chain, end_chain))
		aln.append_model(mdl, align_codes= codes2, atom_files = f_out_pdb)

	aln_block = len(aln)	
	aln.append(file = f_out_query, align_codes=codes1)

	# aln.salign(
	# 	output='', max_gap_length=2,
	# 		gap_function=False,   # to use structure-dependent gap penalty
	# 		alignment_type='PAIRWISE', align_block=aln_block,
	# 		# feature_weights=(1., 0., 0., 0., 0., 0.), overhang=0,
	# 		gap_penalties_1d=(-450, 0),
	# 		# gap_penalties_2d=(0.35, 1.2, 0.9, 1.2, 0.6, 8.6, 1.2, 0., 0.),
	# 		similarity_flag=True)
	# aln.salign(
	# rr_file='${LIB}/blosum62.sim.mat',
	# 	gap_penalties_1d=(-900, -50), output='',
	# 	# align_block=1,   # no. of seqs. in first MSA
	# 	fit_on_first=False,
	# 	align_what='PROFILE',
	# 	local_alignment= True,
	# 	alignment_type='PAIRWISE',
	# 	comparison_type='PSSM',  # or 'MAT' (Caution: Method NOT benchmarked
	# 	                        # for 'MAT')
	# 	similarity_flag=True,    # The score matrix is not rescaled
	# 	substitution=True,       # The BLOSUM62 substitution values are
	# 	                        # multiplied to the corr. coef.
	# 	#output_weights_file='test.mtx', # optional, to write weight matrix
	# 	smooth_prof_weight=10.0) # For mixing data with priors

	aln.salign()

	# aln.write(file='malign.ali', alignment_format='PIR')

	pir_file = output_file[0] + out_txt.rstrip(':') + '.ali' # HM_align2d.py output file
	pap_file = output_file[0] + out_txt.rstrip(':') + '.pap' # HM_align2d.py output file

	aln.write(file = pir_file, alignment_format='PIR')
	aln.write(file = pap_file, alignment_format='PAP')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make model alignment")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')
