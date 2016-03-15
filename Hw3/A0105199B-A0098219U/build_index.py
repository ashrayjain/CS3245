import os
import os.path as osp
from math import sqrt


from dictionary import Dictionary
from postings import Postings
from utils import preprocess_doc, tf

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
        add_doc_to_index(doc_id, doc_path, dictionary, postings)
    postings.save()

    # turn line nos to byte offsets
    f = open(postings_file)
    current_line = 1
    f.readline()  # skip postings list containing all doc ids
    while True:
        term = dictionary.term_for_offset(current_line)
        dictionary.add_term(term, f.tell(), update_freq=False)
        line = f.readline()
        if not line:
            break
        current_line += 1
    dictionary.generate_idf(len(training_files))
    dictionary.save()


def add_doc_to_index(doc_id, doc_path, d, p):
    with open(doc_path) as f:
        vocab = preprocess_doc(f.read())
    add_vocab_to_index(doc_id, vocab, d, p)


def add_vocab_to_index(doc_id, vocab, d, p):
    doc_len_squared = 0
    for term in vocab.iterkeys():
        tf_val = tf(vocab[term])
        if d.does_term_exist(term):
            frequecy, offset = d.term(term)
            d.add_term(term, offset)
            p.list_at_offset(offset).add((doc_id, tf_val))
        else:
            p_list, offset = p.new_list()
            d.add_term(term, offset, add_to_offset_index=True)
            p_list.add((doc_id, tf_val))
        doc_len_squared += tf_val * tf_val
    p.not_list().add((doc_id, sqrt(doc_len_squared)))
