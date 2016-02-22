import os
import os.path as osp
from math import sqrt, ceil

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer

from dictionary import Dictionary
from postings import Postings
from postings_entry import PostingsEntry


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
    create_skip_pointers(dictionary, postings)


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


def create_skip_pointers(d, p):
    for term, term_obj in d.terms():
        frequency, ptr_to_entry = term_obj
        skip_len = int(ceil(sqrt(frequency)))

        # no need for skip pointers for short lists
        if skip_len < 3:
            continue

        base_entry = p.read_entry_at_offset(ptr_to_entry)
        skip_to_entry = base_entry
        while skip_to_entry.next_ptr is not None:
            skips = 0
            while skip_to_entry.next_ptr is not None and skips != skip_len:
                skip_to_entry = p.read_entry_at_offset(skip_to_entry.next_ptr)
                skips += 1
            if skips != skip_len:
                break
            base_entry.skip_ptr = skip_to_entry.offset
            base_entry.skip_doc_id = skip_to_entry.doc_id
            p.add_entry(base_entry, base_entry.offset)
            base_entry = skip_to_entry


def get_unique_vocab(text):
    v = []
    for s in sent_tokenize(text):
        v += [STEMMER.stem(w).lower() for w in word_tokenize(s)]
    return set(v)
