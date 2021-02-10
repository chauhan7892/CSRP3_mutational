#!/usr/bin/env python
import re
import argparse
from multiprocessing.pool import ThreadPool
import os,sys
import time

def fetch_pdb(param_list):
	pdb_id, outputpath = param_list
	# os.system('wget http://ftp.rcsb.org/download/%s.pdb -O %s.pdb;ln -s %s.pdb %s.pdb' % (pdb_id,pdb_id.upper(),pdb_id.upper(),pdb_id.lower()))
	os.system('wget http://ftp.rcsb.org/download/%s.pdb -O %s/%s.pdb' % \
		(pdb_id,outputpath,pdb_id.upper()))

def fetch_pdb_parallel(pdb_id_list):

	start = time.time
	pool = ThreadPool(5)
	pool.imap_unordered(fetch_pdb, pdb_id_list)

	pool.close()
	pool.join()

	end = time.time
	print("Time taken:" + (end-start))

def main( ):
        
    input_file = args_.input_argument
    output_file = args_.output_argument
    pdb_ID_list = []
    
    try:
        pdb_ID_file = input_file[0]
        with open(pdb_ID_file, 'r') as f_in_pdb:
            for line in f_in_pdb:
                pdb_id = line.strip('\n').split()
                pdb_ID_list.extend(pdb_id)

        pdb_output_path = output_file[0]

        pdb_path_list = [pdb_output_path]*len(pdb_ID_list)

        # print pdb_ID_list

        fetch_pdb_parallel(zip(pdb_ID_list, pdb_path_list))

    except Exception, e:
        print str(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to download pdb")
    parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
    parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
    args_ = parser.parse_args()
    main(  )
    print('done')    
