import os.path as osp
import cPickle as pickle


class Dictionary(object):
    _terms = {}  # term format: [frequency, offset]

    def __init__(self, file_name):
        self.file_name = file_name

    def add_term(self, term, offset):
        frequency = self._terms[term][0] if term in self._terms else 0
        self._terms[term] = (frequency + 1, offset)

    def term(self, term):
        return self._terms.get(term, (None, None))

    def save(self):
        with open(self.file_name, 'w') as f:
            pickle.dump(self._terms, f, pickle.HIGHEST_PROTOCOL)

    def load(self):
        if not osp.exists(self.file_name):
            return False
        with open(self.file_name) as f:
            self._terms = pickle.load(f)
        return True

if __name__ == '__main__':
    obj = Dictionary('dictionary.txt')
    print 'Adding term \'the\' with offset 100'
    obj.add_term('the', 100)
    print 'Adding term \'the\' with offset 200'
    obj.add_term('the', 200)
    print 'Adding term \'a\' with offset 20'
    obj.add_term('a', 20)
    print 'Term \'the\':',
    print obj.term('the')
    print 'Saving to disk'
    obj.save()
    del obj

    print 'Loading dictionary from disk'
    obj = Dictionary('dictionary.txt')
    obj.load()
    print 'Term \'a\':',
    print obj.term('a')
    print 'Term \'the\':',
    print obj.term('the')
