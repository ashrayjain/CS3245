import os
import os.path as osp
from dictionary import Dictionary
from postings import Postings
from postings_entry import PostingsEntry

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer

DEBUG_LIMIT = 100
STEMMER = PorterStemmer()


def build_index(training_data_dir, dictionary_file, postings_file, is_debug):
    training_files = sorted(os.listdir(training_data_dir),
                            key=lambda x: int(x), reverse=True)
    if is_debug:
        training_files = training_files[:DEBUG_LIMIT]

    dictionary = Dictionary(dictionary_file)
    postings = Postings(postings_file)
    for training_file in training_files:
        doc_id = int(training_file)
        doc_path = osp.join(training_data_dir, training_file)
        add_doc_to_index(doc_id, doc_path, dictionary, postings)
    dictionary.save()
    print dictionary.term("transfer")


def add_doc_to_index(doc_id, doc_path, d, p):
    with open(doc_path) as f:
        vocab = get_unique_vocab(f.read())
    add_vocab_to_index(doc_id, vocab, d, p)


def add_vocab_to_index(doc_id, vocab, d, p):
    for term in vocab:
        existing_term_freq, existing_term_offset = d.term(term)
        d.add_term(term, p.current_offset())
        if existing_term_freq is None:
            p.add_entry(PostingsEntry(doc_id, None))
        else:
            p.add_entry(PostingsEntry(doc_id, existing_term_offset))


def get_unique_vocab(text):
    v = []
    for s in sent_tokenize(text):
        v += [STEMMER.stem(w).lower() for w in word_tokenize(s)]
    return set(v)


def print_postings(term, d, p):
    freq, offset = d.term(term)
    if freq is None:
        print "No entries for '{}'".format(term)
        return
    print "{} entries for '{}'".format(freq, term)
    print '\t',
    while offset is not None:
        print '->',
        entry = p.read_entry_at_offset(offset)
        print entry.doc_id,
        offset = entry.next_ptr
    print

if __name__ == '__main__':
    vocab = ['a', 'the', 'a', 'the', 'food', 'lol', 'what']
    doc_id = 1
    d = Dictionary('dictionary.txt')
    p = Postings('postings.txt')
    add_vocab_to_index(doc_id, vocab, d, p)
    vocab = ['the', 'food', 'the', 'foobar', 'what']
    doc_id = 2
    add_vocab_to_index(doc_id, vocab, d, p)
    d.save()
    del p
    del d

    d = Dictionary('dictionary.txt')
    d.load()
    print d._terms
    p = Postings('postings.txt')
    print_postings('the', d, p)
    print_postings('food', d, p)
    print_postings('a', d, p)
    print_postings('lol', d, p)
    print_postings('nonexistent', d, p)
