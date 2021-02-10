# from pymol.cgo import *
#from PM_features import *
import sys, time, os, re
import colorsys
import pymol
from pymol import cmd

import __main__
__main__.pymol_argv = [ 'pymol', '-qei' ]

# python Amino Acids Thee2One & One2Three Dictionary
one_letter ={'VAL':'V', 'ILE':'I', 'LEU':'L', 'GLU':'E', 'GLN':'Q', \
'ASP':'D', 'ASN':'N', 'HIS':'H', 'TRP':'W', 'PHE':'F', 'TYR':'Y',    \
'ARG':'R', 'LYS':'K', 'SER':'S', 'THR':'T', 'MET':'M', 'ALA':'A',    \
'GLY':'G', 'PRO':'P', 'CYS':'C', 'UNK':'X'}

three_letter ={'V':'VAL', 'I':'ILE', 'L':'LEU', 'E':'GLU', 'Q':'GLN', \
'D':'ASP', 'N':'ASN', 'H':'HIS', 'W':'TRP', 'F':'PHE', 'Y':'TYR',    \
'R':'ARG', 'K':'LYS', 'S':'SER', 'T':'THR', 'M':'MET', 'A':'ALA',    \
'G':'GLY', 'P':'PRO', 'C':'CYS', 'X':'UNK'}


def read_model(input_file, column, feature, split_type = '\t', header = True):   

	ori_res_list = []
	res_num_list = []
	sub_res_list = []

	with open(input_file, 'r') as f_in:
		for line in f_in:
			if header == True:
				header = False
				continue
			line = line.strip('\n').split(split_type)
			target_feat = line[column-1].strip()
			# if target_feat != feature: continue
			if target_feat not in feature: continue
			mutation_properties = line[0]
			match = re.match(r'(^[A-Z]{1})([0-9]+)([A-Z]{1}$)', mutation_properties, re.I)
			if match: 
				ori_AA = three_letter[match.group(1).upper()]	# original residue	
				AA_pos = int(match.group(2))                    # original residue position
				mut_AA = three_letter[match.group(3).upper()]   # substituted residue
				ori_res_list.append(ori_AA)
				res_num_list.append(AA_pos)
				sub_res_list.append(mut_AA)

	all_together = ori_res_list, res_num_list, sub_res_list
	return(all_together)


# main
pdb_path = os.path.abspath(sys.argv[2])
pdb_name = pdb_path.split('/')[-1].split('.pdb')[0]

input_file = os.path.abspath(sys.argv[3])

de_stabilizing_list = ['highly de-stabilizing', 'de-stabilizing', 'slightly de-stabilizing']
neutral_list = ['neutral']
stabilizing_list = ['highly stabilizing', 'stabilizing', 'slightly stabilizing']

#read_model(input_file, column, feature, split_type = '\t', header = True)
mut_feat_de_stab = read_model(input_file, 4, de_stabilizing_list, split_type = '\t', header = True)
mut_feat_neut = read_model(input_file, 4, neutral_list, split_type = '\t', header = True)
mut_feat_stab = read_model(input_file, 4, stabilizing_list, split_type = '\t', header = True)

mut_feat_HCM = read_model(input_file, 5, ['HCM'], split_type = '\t', header = True)
mut_feat_DCM = read_model(input_file, 5, ['DCM'], split_type = '\t', header = True)

ori_res_HCM, res_pos_HCM, mut_res_HCM = mut_feat_HCM
ori_res_DCM, res_pos_DCM, mut_res_DCM = mut_feat_DCM
ori_res_de_stab, res_pos_de_stab, mut_res_de_stab = mut_feat_de_stab
ori_res_neut, res_pos_neut, mut_res_neut = mut_feat_neut
ori_res_stab, res_pos_stab, mut_res_stab = mut_feat_stab


# HCM part 
resi_list_HCM_part = ''
for item in range(len(res_pos_HCM)):
	resi_list_HCM_part += str(res_pos_HCM[item]) + '+'

resi_list_HCM_part = resi_list_HCM_part[:-1] # remove extra + 

print(resi_list_HCM_part)

# DCM part 
resi_list_DCM_part = ''
for item in range(len(res_pos_DCM)):
	resi_list_DCM_part += str(res_pos_DCM[item]) + '+'

resi_list_DCM_part = resi_list_DCM_part[:-1] # remove extra + 
print(resi_list_DCM_part)


# Destabilizing part 
resi_list_de_stab_part = ''
for item in range(len(res_pos_de_stab)):
	resi_list_de_stab_part += str(res_pos_de_stab[item]) + '+'

resi_list_de_stab_part = resi_list_de_stab_part[:-1] # remove extra + 
print(resi_list_de_stab_part)


# Neutral part
resi_list_neut_part = ''
for item in range(len(res_pos_neut)):
	resi_list_neut_part += str(res_pos_neut[item]) + '+'

resi_list_neut_part = resi_list_neut_part[:-1] # remove extra + 
print(resi_list_neut_part)

# stabilizing part 
resi_list_stab_part = ''
for item in range(len(res_pos_stab)):
	resi_list_stab_part += str(res_pos_stab[item]) + '+'

resi_list_stab_part = resi_list_stab_part[:-1] # remove extra + 
print(resi_list_stab_part)

cmd.load(pdb_path, pdb_name)
cmd.bg_color('white')
# cmd.zoom()
# cmd.orient()
cmd.hide('everything', pdb_name)
cmd.show('cartoon', pdb_name)
cmd.color('grey90', pdb_name)


try:
	cmd.create('HCM_part', 'resi ' + resi_list_HCM_part)
	cmd.select('HCM_ca', 'bycalpha HCM_part')
	cmd.show('sphere', 'HCM_ca')
	cmd.color('greencyan', 'HCM_part')
except CmdException:
	print('no HCM mutation')

try:
	cmd.create('DCM_part', 'resi ' + resi_list_DCM_part)
	cmd.select('DCM_ca', 'bycalpha DCM_part')
	cmd.show('sphere', 'DCM_ca')
	cmd.color('chartreuse', 'DCM_part')
except CmdException:
	print('no DCM mutation')


cmd.set('label_size', 15)
cmd.set('float_labels', 'on')

try:
	cmd.create('de_stab_part', 'resi ' + resi_list_de_stab_part)
	cmd.select('de_stab_ca', 'bycalpha de_stab_part')
	cmd.label('de_stab_ca', 'one_letter[resn]+resi')
	cmd.set('label_color', 'red', 'de_stab_ca')
except CmdException:
	print('no de-stabilizing mutation')

try:
	cmd.create('stab_part', 'resi ' + resi_list_stab_part)
	cmd.select('stab_ca', 'bycalpha stab_part')
	cmd.label('stab_ca', 'one_letter[resn]+resi')
	cmd.set('label_color', 'green', 'stab_ca')
except CmdException:
	print('no stabilizing mutation')


try:
	cmd.create('neut_part', 'resi ' + resi_list_neut_part)
	cmd.select('neut_ca', 'bycalpha neut_part')
	cmd.label('neut_ca', 'one_letter[resn]+resi')
	cmd.set('label_color', 'black', 'neut_ca')
except CmdException:
	print('no neutral mutation')

cmd.zoom()
cmd.orient()

	

