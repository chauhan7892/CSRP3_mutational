import sys, time, os
import argparse
import shutil


# function to run FoldX BuildModel command
def single_task_foldx(params):
	(foldx_exec, repair_pdb_dir, repair_pdb_name, the_mutant_file, output_dir_phenotype) = params

	all_info2 = foldx_exec + ' --command=BuildModel --pdb-dir=' + repair_pdb_dir + \
	' --pdb=' + repair_pdb_name + ' --mutant-file=' + the_mutant_file + \
	' --temperature=298 --ionStrength=0.05 --pH=7 --vdwDesign=2 --output-dir=' + \
	output_dir_phenotype + ' --pdbHydrogens=false --numberOfRuns=5'

	os.system(all_info2)



def main( ):

	foldx_exec = args_.binary_argument
	input_file = args_.input_argument
	output_file = args_.output_argument

	# FoldX program folder path
	foldx_path = os.path.split(foldx_exec)[0]
	foldx_rotamer_file = foldx_path + '/rotabase.txt'

	# copy rotabase.txt file to current path
	shutil.copy(foldx_rotamer_file, './')

	# pdb file name and path
	pdb_file = input_file[0]
	pdb_info = os.path.split(pdb_file)
	pdb_name = pdb_info[1]
	pdb_dir = pdb_info[0]

	# file containing mutations
	mutant_file = input_file[1] 

	# folder to store repair PDB file
	repair_pdb_dir = output_file[0] # output_file[0] is actually directory not a file

	# folder to store mutant models PDBs 
	output_dir_phenotype = output_file[1]
	
	# check if repair PDB file exists otherwise run FoldX repairPDB command
	repair_pdb_name = pdb_name.split('.')[0]+'_Repair.pdb'

	if os.path.exists(repair_pdb_dir + '/' + repair_pdb_name):
		print('Repair file already present')
	else:
		all_info = foldx_exec + ' --command=RepairPDB --pdb-dir=' + pdb_dir + ' --pdb=' + pdb_name + \
		' --temperature=298 --ionStrength=0.05 --pH=7 --vdwDesign=2 --pdbHydrogens=false --output-dir=' + \
		repair_pdb_dir		

		os.system(all_info)

	"""Check if folder containing mutant models PDBs already present, if so then remove folder 
	 and its content. Otherwise make new folder """

	if os.path.exists(output_dir_phenotype):
		print('file already exists: removing it')
		shutil.rmtree(output_dir_phenotype)
		os.mkdir(output_dir_phenotype)
	else:
		os.mkdir(output_dir_phenotype)

	# parameters for single_task_foldx function
	params = (foldx_exec, repair_pdb_dir, repair_pdb_name, mutant_file, output_dir_phenotype)

	# call the single_task_foldx function
	single_task_foldx(params)

	# remove rotabase.txt from current path
	os.unlink('rotabase.txt')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make run foldX")
	parser.add_argument('-b', dest='binary_argument', help="binary executable name")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')