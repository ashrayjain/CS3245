import argparse
from build_index import build_index


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
build_index(args.input, args.dictionary, args.postings, args.debug)
