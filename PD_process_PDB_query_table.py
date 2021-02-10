#!/usr/bin/env python
import os, re, sys
import argparse

def main( ):
        
	input_file = args_.input_argument
	output_file = args_.output_argument
	pdb_txt_search = input_file[0]

	out_txt = ''
	pdb_uniq_list = []
	with open(pdb_txt_search, 'r') as f_in_search:
		for line in f_in_search:
			if line == '\n':continue
			line = line.strip('\n').split('\t')
			pdb_id = line[0]
			pdb_chain = line[1]
			domain = line[4]
			if not domain:continue
			group = re.match('LIM',domain)
			if group:
				pdb_LIM =  pdb_id+'_'+pdb_chain
				if pdb_LIM not in pdb_uniq_list:
					pdb_uniq_list.append(pdb_LIM)
					out_txt += pdb_LIM + '\n'
				
	with open(output_file[0], 'w') as f_out:
		f_out.write(out_txt)

	
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to download pdb")
    parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
    parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
    args_ = parser.parse_args()
    main(  )
    print('done')    
