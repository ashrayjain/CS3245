import sys

fpos = sys.argv[1]
fneg = sys.argv[2]
fout = sys.argv[3]

with open(fpos) as fp, open(fneg) as fn, open(fout) as fo:
    ppres, fpres = ([], [])

    def populate(f, arr):
        for line in f:
            line = line.strip()
            if line:
                arr.append(line)

    pos = []
    neg = []

    populate(fp, pos)
    populate(fn, neg)

    output = []
    for line in fo:
        output.extend(line.strip().split())

    for o in output:
        if o in pos:
            ppres.append(o)
        if o in neg:
            fpres.append(o)

    print "Positive Accuracy:", str(round(len(ppres) * 100.0 / len(pos), 2))
    print "Negative Accuracy:", str(100 - round(len(fpres) * 100.0 / len(neg), 2))

    print "Missing:", sorted(x for x in pos if x not in ppres)
    print "Extra:", sorted(x for x in fpres if x in neg)
