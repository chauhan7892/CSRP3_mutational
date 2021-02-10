
import argparse


def add_chain(input_file):
	output = ''
	with open(input_file, 'r') as f_in:
		for line in f_in:            
			if line[0:4] != 'ATOM': 
				output += line
				continue
			chain = line[21].strip() # chain name
			if not chain:
				output += line[0:21] + 'A' + line[22:]
	return output

def main( ):
	input_file = args_.input_argument
	output_file = args_.output_argument

	pdb_file = input_file[0]
	pdb_with_chain_file = output_file[0]

	output_pdb = add_chain(pdb_file)

	with open(pdb_with_chain_file, 'w') as f_out:
		f_out.write(output_pdb)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to add chain to chainless pdb")
    parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
    parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
    args_ = parser.parse_args()
    main(  )
    print('done')
