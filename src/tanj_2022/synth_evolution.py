from supporting_functions import *

def evolve(seq, fields, subs, alphabet, dt=1000):
    l = len(seq)

    for it in range(dt):
        pos = random.randrange(l)
        aa = random.choice(alphabet)

        ppos = fields[pos]
        psub = subs[alphabet.index(seq[pos]), alphabet.index(aa)]
        
        r = random.random()
        if r < ppos*psub:
            seq[pos] = aa
    return seq


def synthetic_sequences(in_evolmx_fn, out_fasta_fn, out_nhx_fn, LENGTH=100, TIMESTEPS=50):
    EVOLMX = np.zeros((20,20))
    with open(in_evolmx_fn) as f:
        lines = f.readlines()
        alphabet = lines[0].split()
        for iline, line in enumerate(lines[1:]):
            EVOLMX[iline,:] = np.array([min(1, 2*int(x)) for x in line.split()])

    ancestor = random.choices(alphabet, k=LENGTH)
    
    fields = np.random.rand(LENGTH)
    
    label = "ancestor"
    currents = [(label, ancestor)]
    t = Tree(label+";")
    
    with open(out_fasta_fn, "w") as f:
        print(t)
        print("".join(ancestor) + "\t" + label)
        f.write(">{0}\n".format(label))
        f.write("".join(ancestor)+"\n")
        for ts in range(1, TIMESTEPS+1):
            newcurrents = []
            for ic, c in enumerate(currents):
                label, current = c
                n = t.search_nodes(name=label)[0]
                newseq = evolve(current, fields, EVOLMX, alphabet)
                newlabel = str(ts) + "_" + str(ic)
                n.add_child(name=newlabel)
                print("".join(newseq) + "\t" + newlabel)
                f.write(">"+newlabel+"\n")
                f.write("".join(newseq)+"\n")
                newcurrents.append((newlabel, newseq))
                if random.random() < 0.1:
                    newseq2 = evolve(current, fields, EVOLMX, alphabet)
                    newlabel2 = str(ts) + "_" + str(ic) + "bis"
                    print("".join(newseq2) + "\t" + newlabel2)
                    f.write(">"+newlabel2+"\n")
                    f.write("".join(newseq2)+"\n")
                    newcurrents.append((newlabel2, newseq2))
                    n.add_child(name=newlabel2)
            currents = newcurrents
    
    print(t.get_ascii(show_internal=True))
    t.write(format=1, outfile=out_nhx_fn)


if __name__ == "__main__":
    parser.add_argument("evolmx", type=str, help="the input amino acid evolution matrix (20x20 matrix stored as a text file)")
    parser.add_argument("outf", type=str, help="the output fasta file containing the aligned sequences")
    parser.add_argument("outt", type=str, help="the output nhx file containing the sequence tree")
    parser.add_argument("-l", "--length", type=int, help="the length of the generated sequences (gaps included)", default=100)
    parser.add_argument("-t", "--timesteps", type=int, help="the number of evolution time steps to take", default=50)
    args = parser.parse_args()
    synthetic_sequences(args.evolmx, args.outf, args.outt, LENGTH=args.length, TIMESTEPS=args.timesteps) 
