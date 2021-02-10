
# function to parse domtbl domain

def domtbl_parse(domtbl_out_file):

	domtbl_list = []	
	with open(domtbl_out_file, 'r') as f_in_domtbl:
		for line in f_in_domtbl:
			if line[0] == '#':continue
			line = line.strip('\n').split()
			dom = line[0]
			dom_len = int(line[2])
			q_id = line[3]
			q_len = int(line[5])
			dom_num = int(line[9])
			dom_total = int(line[10])
			dom_i_val = float(line[12])
			dom_start = int(line[19])
			dom_end = int(line[20])

			dom_info =[q_id, q_len, dom, dom_len, dom_num, dom_total, dom_i_val, dom_start, dom_end]

			domtbl_list.append(dom_info)

	return domtbl_list
