python3 synth_evolution.py blosum62.txt ../data/preprocessed_data/synthetic.fasta ../data/preprocessed_data/synthetic.nhx
python3 calc_dissimilarity_matrix.py ../data/preprocessed_data/synthetic.fasta ../data/preprocessed_data/synthetic.npy -hdr sequential
