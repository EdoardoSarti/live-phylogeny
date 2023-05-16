from supporting_functions import *


def generate_data(in_fasta_fn, header_type, out_dmtx_npy_fn):
    labels, sequences = [], []
    if header_type == "GISAID":
        iseq = 0
        no_go = False
        with open(in_fasta_fn) as f:
            for line in f:
                if line.startswith(">"):
                    no_go = False
                    date = line.split("|")[2].replace("00","01")
                    try:
                        ndate = datetime.strptime(date, "%Y-%m-%d")
                    except:
                        no_go = True
                        continue
                    iseq += 1
                    labels.append("seq" + str(iseq).zfill(10) + "_" + date)
                elif not no_go:
                    sequences.append(line.strip())
    elif header_type == "sequential":
        with open(in_fasta_fn) as f:
            for line in f:
                if line.startswith(">"):
                    labels.append(line.strip())
                else:
                    sequences.append(line.strip())

    numbPoints = len(sequences)
    distMat = np.zeros((numbPoints,numbPoints))
    for i in range(numbPoints):
        for j in range(numbPoints):
            distMat[i][j] = 1 - SI(sequences[i], sequences[j])
    np.save(out_dmtx_npy_fn, distMat)


if __name__ == "__main__":
    parser.add_argument("infasta", type=str, help="the input fasta file for which a distance matrix will be calculated")
    parser.add_argument("outmtx", type=str, help="the output matrix as an npy numpy file")
    parser.add_argument("-hdr", "--header", type=str, help="the type of header of the fasta file", choices={"sequential", "GISAID"}, default="sequential")
    args = parser.parse_args()
    generate_data(args.infasta, args.header, args.outmtx)
