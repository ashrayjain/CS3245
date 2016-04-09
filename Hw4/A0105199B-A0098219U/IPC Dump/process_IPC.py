import os
import sys
import codecs
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import utils

index = {}


def process(fipc):
    global index
    for line in fipc:
        line = line.strip().split()
        ipc = line[0].decode('utf-8')
        desc = " ".join(line[1:])
        normalized = utils.preprocess_text(desc.decode('utf-8')).keys()
        for w in normalized:
            ipclist = index.get(w, [])
            ipclist.append(ipc)
            index[w] = ipclist

for s, d, files in os.walk('.'):
    for f in files:
        if f[:2] == 'EN':
            print 'Processing: ', f
            with open(os.path.join(s, f)) as fipc:
                process(fipc)

    with codecs.open('ipc_index.txt', 'w', 'utf-8') as fout:
        for w in index:
            outstr = w + " " + " ".join(index[w]) + "\n"
            fout.write(outstr)
