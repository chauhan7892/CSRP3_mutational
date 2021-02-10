
# function to parse domtbl domain

def domtbl_parse(domtbl_out_file):

	domtbl_list = []	
	with open(domtbl_out_file, 'r') as f_in_domtbl:
		for line in f_in_domtbl:
			if line[0] == '#':continue
			line = line.strip('\n').split()
			dom = line[0]
			t_access = line[1]
			dom_len = int(line[2])
			q_id = line[3]
			q_access = line[4]
			q_len = int(line[5])
			seq_Eval = float(line[6])
			seq_score = float(line[7])
			seq_bias = float(line[8])
			dom_num = int(line[9])
			dom_total = int(line[10])
			dom_c_Eval = float(line[11])
			dom_i_Eval = float(line[12])
			dom_score = float(line[13])
			dom_bias = float(line[14])
			hmm_start = int(line[15])
			hmm_end = int(line[16])
			ali_start = int(line[17])
			ali_end = int(line[18])
			dom_start = int(line[19])
			dom_end = int(line[20])
			acc = float(line[21])
			desc = line[22]

			dom_info =[dom, t_access, dom_len, q_id, q_access, q_len,\
			seq_Eval, seq_score, seq_bias, dom_num, dom_total, \
			dom_c_Eval, dom_i_Eval, dom_score, dom_bias, \
			hmm_start, hmm_end, ali_start, ali_end, dom_start, dom_end,\
			acc, desc]

			domtbl_list.append(dom_info)

	return domtbl_list
