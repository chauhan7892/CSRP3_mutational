#!/usr/bin/env python
import re
import argparse
from multiprocessing.pool import ThreadPool
import wget
import time

def fetch_pdb(param_list):
    pdb_id, outputpath = param_list
    url = 'http://ftp.rcsb.org/download/'+pdb_id+'.pdb'
    wget.download(url, out=outputpath+'/'+pdb_id.upper()+'.pdb')

def fetch_pdb_parallel(pdb_id_list):

    start = time.time
    pool = ThreadPool(5)
    pool.imap_unordered(fetch_pdb, pdb_id_list)

    pool.close()
    pool.join()
    
    end = time.time
    print("Time taken: %f" %(end-start))

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
