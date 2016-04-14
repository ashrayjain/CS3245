import os
import os.path as osp
from math import sqrt


from dictionary import Dictionary
from postings import Postings
from utils import preprocess_text, tf
from trie import Trie

import pickle
import xml.etree.ElementTree as et
from utils import preprocess_text
from nltk.corpus import stopwords
stop = stopwords.words('english')
stop_preprocessed = [preprocess_text(w).popitem()[0] for w in stop]

DEBUG_LIMIT = 100


def build_index(training_data_dir, dictionary_file, postings_file, is_debug):
    training_files = sorted(os.listdir(training_data_dir),
                            key=lambda x: x)
    if is_debug:
        training_files = training_files[:DEBUG_LIMIT]

    dictionary = Dictionary(dictionary_file)
    postings = Postings(postings_file)
    for training_file in training_files:
        doc_id = training_file
        doc_path = osp.join(training_data_dir, training_file)
        add_doc_to_index(doc_id, doc_path, dictionary, postings)
    postings.save()

    # turn line nos to byte offsets
    f = open(postings_file)
    current_line = 0
    while True:
        term = dictionary.term_for_offset(current_line)
        dictionary.add_term(term, f.tell(), update_freq=False)
        line = f.readline()
        if not line:
            break
        current_line += 1
    dictionary.generate_idf(len(training_files))
    dictionary.save()

    trie = Trie(training_data_dir)
    trie.save()

    # Varun's code to map query words in the patent doc to the patent id

    data = dict()
    for training_file in training_files:
        doc = et.parse(osp.join(training_data_dir, training_file)).getroot()
        patentnode = doc.find('str/[@name="Patent Number"]')
        patentno = patentnode.text.strip()
        titlenode = doc.find('str/[@name="Title"]')
        if titlenode is not None:
            title = titlenode.text.strip()
            title_map = preprocess_text(title)
            for word in title_map:
                if word not in stop_preprocessed:
                    data.setdefault(word, set()).add(patentno)

        abstractnode = doc.find('str/[@name="Abstract"]')
        if abstractnode is not None:
            abstract = abstractnode.text.strip()
            abstract_map = preprocess_text(abstract)
            for word in title_map:
                if word not in stop_preprocessed:
                    data.setdefault(word, set()).add(patentno)

    with open("patent_query_data", "wb") as f:
        pickle.dump(data, f, -1)





def add_doc_to_index(doc_id, doc_path, d, p):
    with open(doc_path) as f:
        vocab = preprocess_text(f.read())
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
    d.add_doc_id(doc_id, sqrt(doc_len_squared))
