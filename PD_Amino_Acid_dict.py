
# python Amino Acids Thee2One & One2Three Dictionary
one_letter ={'VAL':'V', 'ILE':'I', 'LEU':'L', 'GLU':'E', 'GLN':'Q', \
'ASP':'D', 'ASN':'N', 'HIS':'H', 'TRP':'W', 'PHE':'F', 'TYR':'Y',    \
'ARG':'R', 'LYS':'K', 'SER':'S', 'THR':'T', 'MET':'M', 'ALA':'A',    \
'GLY':'G', 'PRO':'P', 'CYS':'C', 'UNK':'X'}

three_letter ={'V':'VAL', 'I':'ILE', 'L':'LEU', 'E':'GLU', 'Q':'GLN', \
'D':'ASP', 'N':'ASN', 'H':'HIS', 'W':'TRP', 'F':'PHE', 'Y':'TYR',    \
'R':'ARG', 'K':'LYS', 'S':'SER', 'T':'THR', 'M':'MET', 'A':'ALA',    \
'G':'GLY', 'P':'PRO', 'C':'CYS', 'X':'UNK'}

PC5 = {"I": "A", "V": "A",  "L": "A", # Aliphatic
"F": "R", "Y": "R", "W": "R", "H": "R", # Aromatic
"K": "C", "R": "C", "D": "C", "E": "C", # Charged 
"G": "T", "A": "T", "C": "T", "S": "T", # Tiny   
"T": "D", "M": "D", "Q": "D", "N": "D", "P": "D"} # Diverse 

# conventional
CN_AA = {"F": "R", "Y": "R", "W": "R", # Aromatic
"K": "C", "R": "C", "H": "C", "D" : "C", "E": "C", # Charged 
"G": "N", "A": "N", "V": "N", "L": "N", "I": "N", "P": "N", # Non-ploar
"S": "P", "T": "P", "C": "P", "M": "P", "N": "P", "Q": 'P'} # Polar 
