import os
import os.path as osp


from dictionary import Dictionary
from postings import Postings
from utils import preprocess_doc

DEBUG_LIMIT = 100


def build_index(training_data_dir, dictionary_file, postings_file, is_debug):
    training_files = sorted(os.listdir(training_data_dir),
                            key=lambda x: int(x))
    if is_debug:
        training_files = training_files[:DEBUG_LIMIT]

    dictionary = Dictionary(dictionary_file)
    postings = Postings(postings_file)
    for training_file in training_files:
        doc_id = int(training_file)
        doc_path = osp.join(training_data_dir, training_file)
        postings.not_list().add(doc_id)
        add_doc_to_index(doc_id, doc_path, dictionary, postings)
    dictionary.save()
    postings.save()


def add_doc_to_index(doc_id, doc_path, d, p):
    with open(doc_path) as f:
        vocab = preprocess_doc(f.read())
    add_vocab_to_index(doc_id, vocab, d, p)


def add_vocab_to_index(doc_id, vocab, d, p):
    for term in vocab:
        if d.does_term_exist(term):
            frequecy, offset = d.term(term)
            d.add_term(term, offset)
            p.list_at_offset(offset).add(doc_id)
        else:
            p_list, offset = p.new_list()
            d.add_term(term, offset)
            p_list.add(doc_id)
