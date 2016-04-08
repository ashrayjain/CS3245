import codecs

class IPCIndex(object):
    def __init__(self, fname):
        self.index = {}

        with codecs.open(fname) as fin:
            for line in fin:
                line = line.strip().split()
                self.index[line[0]] = line[1:]

    def get(self, key):
        return self.index[key]        

if __name__ == "__main__":
    index = IPCIndex('ipc_index.txt')
    print index.get(index.index.keys()[0])
