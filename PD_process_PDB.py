import numpy as np
### READ PDB file ########

# output an object 
# if input is atom type 1 , only backbone in the object
# if input is atom type 2 , only N, CA and C in the object
# if input is atom type any other value , all atoms are in the object

class residue(object):
	def __init__( self, num, name, atom): # initialize the node
		self.rNum = num # residue position
		self.rName = name # residue name 
		self.rAtom = atom # atom dict 

class atom(object)
	def __init__( self, atom, x_coord = 0, y_coord = 0, z_coord = 0)
		self.aName = atom # atom name 
		self.aCoord = np.array((x_coord, y_coord, z_coord), 'f')

def read_PDB(file, atom_type = 1):
	p = []
	c = []    
	rNum = None
	rChain = None
	rName = None
	chain_name = []
	with open(file, 'r') as f_in:
		for line in f_in:            
			if line[:3] == "TER": # if reached the last line
				if c: # if chain data
					p.append(c) # append chain data to the over all data
					chain_name.append(rChain) # append chain to chain name list
					c = []
				continue 
			if line[0:4] != 'ATOM': continue # look for only atom features
			atom_name = line[12:16].strip()

			if (atom_type == 1) and (atom_name != "CA"): continue # focus on backbone only
			elif (atom_type == 2) and (atom_name not in [ "N", "CA", "C" ]): continue # focus on N, CA and C only
			
			res_name = line[17:20].strip() # residue name
			chain = line[21].strip() # chain name
			res_num = int(line[22:26]) # residue number 
			if rNum != res_num:
				rName = res_name
				rChain = chain
				rNum = res_num
			rAtom = atom_name
			x_coord = float(line[30:38]) 
			y_coord = float(line[38:46])
			z_coord = float(line[46:54])
			A_coord = np.array((x_coord, y_coord, z_coord), 'f')


			aa = residue(rNum, rName, rAtom, x_coord, y_coord, z_coord)
			c.append(aa)
		if c:
			p.append(c)
			chain_name.append(rChain)
	return p, chain_name
