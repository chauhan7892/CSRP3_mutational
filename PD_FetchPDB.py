#!/usr/bin/env python
import os, re, sys
import argparse
import multiprocessing
def fetch_pdb(pdb_id):
    # os.system('wget http://ftp.rcsb.org/download/%s.pdb -O %s.pdb;ln -s %s.pdb %s.pdb' % (pdb_id,pdb_id.upper(),pdb_id.upper(),pdb_id.lower()))
    os.system('wget http://ftp.rcsb.org/download/%s.pdb -O %s.pdb' % (pdb_id,pdb_id.upper()))

def fetch_pdb_parallel(pdb_id_list):
    pool = multiprocessing.Pool(20)
    pool.map(fetch_pdb, pdb_id_list)

    pool.close()
    pool.join()

def clear_newline(x):
    return re.sub(r'\r|\n', '', x)

def main( ):
        
    input_file = args_.input_argument
    output_file = args_.output_argument
    pdb_map_list = []
    try:
        pdb_list_file = input_file[0]
        with open(pdb_list_file) as F_in_pdb:
            pdb_list = F_in_pdb.readlines()
            for pdb_id in pdb_list:
                pdb_id = pdb_id.split('_')[0]
                pdb_map_list.append(pdb_id)
        pdb_final_list = map(clear_newline, pdb_map_list)
        fetch_pdb_parallel(pdb_final_list)
    except Exception, e:
    print str(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to download pdb")
    parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
    parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
    args_ = parser.parse_args()
    main(  )
    print('done')    
