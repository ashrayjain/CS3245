import argparse
from nltk import Text
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize.treebank import TreebankWordTokenizer
from utils import preprocess_text
import xml.etree.ElementTree as et
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

to_strip = "Relevant documents will describe "

def get_thesaurus():
    corpus = PlaintextCorpusReader(
                './processed_corpus/', 
                '.*', 
                word_tokenizer=TreebankWordTokenizer())
    
    thesaurus = Text(word.lower() for word in corpus.words())
    return thesaurus

def expand(query, thesaurus):
    additional_terms = ""

    for w in query:
        similar_terms = thesaurus.similar(w)
        if similar_terms:
            additional_terms += ' ' + similar_terms

    query += additional_terms

    return query

with open(args.queries, 'r') as fq:
    thesaurus = get_thesaurus()

    text = fq.read()
    root = et.fromstring(text)
    t = ""
    for child in root:
        text = child.text.replace(to_strip, "")
        t += "\n" + text.strip()

    expanded_query = expand(t, thesaurus)
        
    query_map = preprocess_text(t)


with open(args.output, 'w') as fo:
    engine = Engine(args.dictionary, args.postings)
    result = engine.execute_query(query_map)
    if result is None:
        fo.write('\n')
    else:
        fo.write(str(result.replace(".xml", "")).strip() + '\n')
