import argparse
import nltk
from nltk.text import ContextIndex
from nltk.tokenize import word_tokenize
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize.treebank import TreebankWordTokenizer
from utils import preprocess_text, raw_preprocess_text, pos_filter_text
from nltk.compat import Counter
import xml.etree.ElementTree as et
from search_engine import Engine, NotAHackEngine

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

    thesaurus = nltk.Text(word.lower() for word in corpus.words())
    return thesaurus


def similar(word, thesaurus, num=20):
    if '_word_context_index' not in thesaurus.__dict__:
        thesaurus._word_context_index = ContextIndex(
            thesaurus.tokens, filter=lambda x: x.isalpha(),
            key=lambda s: s.lower()
        )

    word = word.lower()
    wci = thesaurus._word_context_index._word_to_contexts
    if word in wci.conditions():
        contexts = set(wci[word])
        fd = Counter(w for w in wci.conditions() for c in wci[w]
                     if c in contexts and not w == word)
        words = [w for w, _ in fd.most_common(num)]
        return words
    else:
        return None


def expand(query, thesaurus):
    additional_terms = []
    for w in set(word_tokenize(query)):
        # print "Word: ", w
        similar_terms = similar(w, thesaurus)
        # print similar_terms
        if similar_terms:
            additional_terms += similar_terms
            # print additional_terms

    query += " ".join(additional_terms)
    return query

with open(args.queries, 'r') as fq:
    # thesaurus = get_thesaurus()

    text = fq.read()
    root = et.fromstring(text)
    query_text = ""
    for child in root:
        text = child.text.replace(to_strip, "")
        query_text += " " + text.strip()

    filtered_query = pos_filter_text(t)
    # filtered_query = raw_preprocess_text(filtered_query)
    # expanded_query = expand(filtered_query, thesaurus)
    # print "Query: ", filtered_query
    # print "Expanded: ", expanded_query
    # query_map = preprocess_text(filtered_query)


with open(args.output, 'w') as fo:
    engine = NotAHackEngine()
    result = engine.execute_query(query_text)
    if result is None:
        fo.write('\n')
    else:
        fo.write(str(result.replace(".xml", "")).strip() + '\n')
