import argparse
import re

def main( ):
    input_file = args_.input_argument
    output_file = args_.output_argument

    output_txt = ''
    with open( input_file[0], 'r') as f_in_pdb:
        for line in f_in_pdb:
            if line[0:6] == 'ENDMDL':
                #output_txt.rstrip('\r\n')#rstrip to remove trailing newline
                break
            elif not line[0:5] == "MODEL":
                output_txt += line

    with open( output_file[0], 'w') as f_out1:
        f_out1.write(output_txt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to extract PPI")
    parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
    parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
    args_ = parser.parse_args()
    main(  )
    print('done')
