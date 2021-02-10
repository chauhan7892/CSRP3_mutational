
def get_seqs_from_fasta(filepath):
    header_seq = {}
    with open(filepath, 'r') as f:
        seqs = []
        header = ''
        for line in f:
            line = line.rstrip()
            if '>' in line:
                if header == '':
                    header = line.replace('>','')
                else:
                    header_seq[header] = ''.join(seqs)
                    seqs = []
                    header = line.replace('>','')
            else:
                seqs.append(line)
        header_seq[header] = ''.join(seqs)
    return header_seq


def get_msa_aln(aln_path):
    # get the strain-sequence dictionary for the MSA
    # strain name is the fasta sequence header
    strain_seq = get_seqs_from_fasta(aln_path)

    # get a list of the strain names from the strain-sequence dictionary
    strains = [strain for strain in strain_seq]
    # sort alphabetically
    strains.sort()

    # get length of the MSA and check that all of the seq are the same length
    seq_len = 0
    len_check = set()
    for x in strain_seq:
        seq_len = len(strain_seq[x])
        len_check.add(seq_len)
    if len(len_check) > 1:
        print 'Sequences in MSA', aln_path, 'not of the same length!'
        print [x for x in len_check]

    # get the list of SNPs
    snps = []
    for nt_index in range(0, seq_len):
        # get list of nucleotides at the current sequence position
        nts = [strain_seq[strain][nt_index] for strain in strains]
        # check if there is a SNP at this position
        if len(set(nts)) == 1:
            # if there isn't then continue onto the next position
            continue

        # get the nucleotide frequency
        nt_counts = {}
        for nt in nts:
            if nt not in nt_counts:
                nt_counts[nt] = 1
            else:
                nt_counts[nt] += 1
        
        # add a small dictionary containing:
        # nt_index: index of SNP within sequence
        # nt_counts: nucleotide dictionary with counts for each nucleotide
        # nts: list of nucleotide at index i
        snps.append(
            {'index':nt_index, 
            'nt_counts':nt_counts, 
            'nts':nts})
    return {'seq_len':seq_len, 'strains':strains, 'snps':snps}
