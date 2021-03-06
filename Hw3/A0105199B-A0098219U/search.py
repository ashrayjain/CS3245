import argparse
from utils import preprocess_text
from search_engine import Engine

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dictionary', required=True,
                    help='dictionary file')
parser.add_argument('-p', '--postings', required=True,
                    help='postings file')
parser.add_argument('-q', '--queries', required=True,
                    help='file of queries')
parser.add_argument('-o', '--output', required=True,
                    help='file of results')
parser.add_argument('--debug', dest='debug', default=False,
                    action='store_true', help='debug mode')
args = parser.parse_args()

with open(args.queries, 'r') as fq:
    with open(args.output, 'w') as fo:
        engine = Engine(args.dictionary, args.postings)
        for query in fq:
            query_map = preprocess_text(query)

            result = engine.execute_query(query_map)
            if result is None:
                fo.write('\n')
            else:
                fo.write(str(result).strip() + '\n')
