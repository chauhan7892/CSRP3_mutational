import argparse
import re,os

def main( ):
    input_file = args_.input_argument
    output_file = args_.output_argument

    output_txt = ''
    output_path = 

    output_folder = os.path.split(input_file[0])[1].split('.')[0].upper()
    base_folder = output_file[0]
    output_folder_path = os.path.join(base_folder,output_folder)
    os.mkdir(output_folder_path)

    with open( input_file[0], 'r') as f_in_pdb:
        model = 0
        for line in f_in_pdb:
            if line[0:5] == "MODEL":
                model += 1
                output_txt = ''
                output_txt += line
            elif line[0:6] == 'ENDMDL':
                output_txt += line
                output_file_model = ('').join([output_folder_path, '/',output_folder,'_', str(model), '.pdb'])
                with open(output_file_model, 'w') as f_out:
                    f_out.write(output_txt)
            else:
                output_txt += line


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to extract PPI")
    parser.add_argument('-i', nargs='+', dest="input_argument",default="something.txt", help="something file")
    parser.add_argument('-o', nargs='+', dest="output_argument",default="something_.txt", help="something file")
    args_ = parser.parse_args()
    main(  )
    print('done')
