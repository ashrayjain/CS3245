import argparse
from build_index import build_index
from rewrite_corpus import CorpusProcessor

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=True,
                    help='training documents directory')
parser.add_argument('-d', '--dictionary', required=True,
                    help='dictionary file')
parser.add_argument('-p', '--postings', required=True,
                    help='postings file')
parser.add_argument('--debug', dest='debug', default=False,
                    action='store_true', help='debug mode')
args = parser.parse_args()

c_dir_new = 'processed_corpus'
c_processor = CorpusProcessor(args.input)
c_processor.xml_to_text(c_dir_new)

build_index(c_dir_new, args.dictionary, args.postings, args.debug)
