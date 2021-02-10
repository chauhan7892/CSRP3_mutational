import sys, time, os
import argparse
import shutil
import concurrent.futures

# function to run FoldX BuildModel command
def single_task_foldx(params):
	(foldx_exec, repair_pdb_dir, repair_pdb_name, the_mutant_file, output_dir_phenotype) = params
	all_info2 = foldx_exec + ' --command=BuildModel --pdb-dir=' + repair_pdb_dir + \
	' --pdb=' + repair_pdb_name + ' --mutant-file=' + the_mutant_file + \
	' --temperature=298 --ionStrength=0.05 --pH=7 --vdwDesign=2 --output-dir=' + \
	output_dir_phenotype + ' --out-pdb=false --numberOfRuns=5 --screen=false'

	os.system(all_info2)

# function to run multi copy FoldX BuildModel command 
def multi_task_foldx(total_threads, param_list):
	with concurrent.futures.ThreadPoolExecutor(max_workers=total_threads) as executor:
		executor.map(single_task_foldx, param_list)

def main( ):
	start_time = time.time() # our scripts start time
	input_file = args_.input_argument


	# FoldX program
	foldx_exec = args_.binary_argument
	foldx_path = os.path.split(foldx_exec)[0]
	# foldx_rotamer_file=foldx_path + '/rotabase.txt'

	# copy rotabase.txt file to current path
	# shutil.copy(foldx_rotamer_file, './')

	# pdb file name and path
	pdb_file = input_file[0]
	pdb_info = os.path.split(pdb_file)
	pdb_name = pdb_info[1]
	pdb_dir = pdb_info[0]

	# folder to store repair PDB file
	repair_pdb_dir = input_file[1] # input_file[2] is actually directory not a file

	repair_pdb_name = pdb_name.split('.')[0]+'_Repair.pdb'

	# check if repair PDB file exists otherwise run FoldX repairPDB command
	if os.path.exists(repair_pdb_dir + '/' + repair_pdb_name):
		print('Repair file already present')
	else:
		all_info = foldx_exec + ' --command=RepairPDB --pdb-dir=' + pdb_dir + ' --pdb=' + pdb_name + \
		' --temperature=298 --ionStrength=0.05 --pH=7 --vdwDesign=2 --pdbHydrogens=false --output-dir=' + \
		repair_pdb_dir
		
		os.system(all_info)
	
	# run through all AA
	params_list = []
	for root,dirs,files in os.walk(repair_pdb_dir):
		if root !=repair_pdb_dir:		
			for file_name in files:
				the_mutant_file = os.path.join(root,file_name) # the file containg mutations
				# print(the_mutant_file)
				output_dir_phenotype = os.path.join(root,'foldx_data') # folder to store mutant models PDBs 

				"""Check if folder containing mutant models PDBs already present, 
				if so then remove folder and its content. 
				Otherwise make new folder """				
				if os.path.exists(output_dir_phenotype):					
					print('foldx_data')
					shutil.rmtree(output_dir_phenotype)
					os.mkdir(output_dir_phenotype)
				else:
					os.mkdir(output_dir_phenotype)

				# parameters for single_task_foldx function
				params = (foldx_exec, repair_pdb_dir, repair_pdb_name, the_mutant_file, output_dir_phenotype)
				# print(foldx_exec, repair_pdb_dir, repair_pdb_name, the_mutant_file, output_dir_phenotype)
				# print(params)
				# second parameter for multi_task_foldx
				params_list.append(params)

	# No. of threads used
	total_threads = 19
	# print(params_list)
	# call the smulti_task_foldx function
	multi_task_foldx(total_threads,params_list)

	# remove rotabase.txt from current path
	# os.unlink('rotabase.txt')

	# check the execution time
	end_time = time.time() - start_time
	print("Executed in %f seconds" %(end_time))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A script to make run foldX")
	parser.add_argument('-b', dest='binary_argument', help=" the binary executable ")
	parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
	args_ = parser.parse_args()
	main(  )
	print('done')
