# CSRP3_mutational

## on server script
python2 Program/Script/MD_individual_list_FoldX_all_AA.py -i Data/Processed_Data/HM/Human/CSRP3_Model4_with_chain.pdb 10-66 120-176 -o Data/Processed_Data/MD/Human

python2 Program/Script/MD_run_FoldX_parallel_V2.py -b Program/Bin/FoldX/foldx -i Data/Processed_Data/HM/Human/CSRP3_Model4_with_chain.pdb Data/Processed_Data/MD/Human

python2 Program/Script/MD_table_FoldX_all_AA.py  -i Data/Processed_Data/MD/Human Data/Processed_Data/MD/Human/CSRP3_Model4_with_chain_Repair.fxout -o Data/Processed_Data/MD/Human/MD_avg_delta_G_all_AA.csv

python2 Program/Script/MD_table_FoldX_all_AA_V2.py  -i Data/Processed_Data/MD/Human Data/Processed_Data/MD/Human/CSRP3_Model4_with_chain_Repair.fxout -o Data/Processed_Data/MD/Human/MD_avg_delta_G_all_AA.csv

rsync Data/Processed_Data/MD/Human/MD_avg_delta_G_all_AA.csv pankaj@172.16.106.145:/home/pankaj/Pankaj_Projects/NCBS/CSRP3_Mutational/Data/Processed_Data/MD/Human/MD_avg_delta_G_all_AA.csv

## local script
python Program/Script/MD_plot_FoldX_grid_V2.py -i Data/Processed_Data/MD/Human/MD_avg_delta_G_all_AA.csv 10-66 120-176 -o Data/Graphics Human_LIM_stability_

python Program/Script/MD_plot_FoldX_barchart_V2.py -i Data/Processed_Data/MD/Human/MD_avg_delta_G_all_AA.csv 10-66 120-176 -o Data/Graphics Human_LIM_stab_freq_

python Program/Script/MD_plot_FoldX_heatmap.py -i Data/Processed_Data/MD/Human/MD_avg_delta_G_all_AA.csv 10-66 120-176 -o Data/Graphics Human_LIM_stability_heat
## LIM1 vs LIM2
