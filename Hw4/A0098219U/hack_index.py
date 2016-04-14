import xml.etree.ElementTree as et
import os
import cPickle as pickle
import os.path as osp

def get_classes_from_ipc(ipc_string):
    return [x.strip()[:3] for x in ipc_string.split('|')]

def get_classes_from_patent_xml(patent_xml):
    root = et.fromstring(patent_xml)
    ipc_node = root.find('str/[@name="All IPC"]')

    if ipc_node is None:
        return "Z99"

    return get_classes_from_ipc(ipc_node.text)

def build_index(training_data_dir):
    training_files = sorted(os.listdir(training_data_dir),
                            key=lambda x: x)

    index = {}

    for training_file in training_files:
        doc_id = training_file
        doc_path = osp.join(training_data_dir, training_file)

        with open(doc_path) as fin:
            classnames = get_classes_from_patent_xml(fin.read())
            for c in classnames:
                index[c] = index.get(c, []) + [doc_id[:-4]]

    with open('class_index.txt', 'w') as fout:
        pickle.dump(index, fout, -1)
