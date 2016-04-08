import argparse
from utils import preprocess_text
import xml.etree.ElementTree as et
from search_engine import IPCEngine


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

to_strip = "Relevant documents will describe "

with open(args.queries, 'r') as fq:
    text = fq.read()
    root = et.fromstring(text)
    t = ""
    for child in root:
        text = child.text.replace(to_strip, "")
        t += "\n" + text.strip()
    query_map = preprocess_text(t)


with open(args.output, 'w') as fo:
    engine = IPCEngine()
    result = engine.execute_query(query_map)
    if result is None:
        fo.write('\n')
    else:
        fo.write(str(result.replace(".xml", "")).strip() + '\n')
