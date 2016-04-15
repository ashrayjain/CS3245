import argparse
import nltk
from nltk.text import ContextIndex
from nltk.tokenize import word_tokenize
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize.treebank import TreebankWordTokenizer
from utils import *
from nltk.compat import Counter
import xml.etree.ElementTree as et
from search_engine import Engine, NotAHackEngine, feedbackEngine

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

original_query = ''

with open(args.queries, 'r') as fq:
    # thesaurus = get_thesaurus()

    text = fq.read()
    root = et.fromstring(text)
    query_text = ""
    for child in root:
        text = child.text.replace(to_strip, "")
        query_text += " " + text.strip()
    # print "Original: ", query_text

    original_query = query_text
    
    verb_list = pos_verbs_filter(query_text)
    noun_list = pos_nouns_filter(query_text)
    
    sans_stop_words_list = stop_words_filter(query_text)

    # print "Verbs: ", verb_list
    # print "Nouns: ", noun_list
    noun_synonyms = set()
    for word in noun_list:
        noun_synonyms.update(get_noun_synonyms(word))
    query_text = " ".join(verb_list + noun_list + list(noun_synonyms) + sans_stop_words_list)
    # print "Query: ", query_text

    query_text = raw_preprocess_text(query_text)
    # print "Stemmed: ", query_text

    # expanded_query = expand(filtered_query, thesaurus)
    # print "Expanded: ", query_text
    query_map = preprocess_text(query_text)

with open(args.output, 'w') as fo:
    engine = feedbackEngine(args.dictionary, args.postings)
    results = engine.execute_query(query_map).split(" ")
    results = [s.replace(".xml", "") for s in results]
    outsourced_engine = NotAHackEngine()
    main_results = outsourced_engine.execute_query(original_query).split(" ")
    main_results = [s.replace(".xml", "") for s in main_results]
    main_result_set = set(main_results)

    if results is not None:
        for r in results:
            if r not in main_result_set:
                main_results.append(r)
                main_result_set.add(r)
    main_results = " ".join(main_results)

    if main_results is None:
        fo.write('\n')
    else:
        fo.write(str(main_results.replace(".xml", "")).strip() + '\n')
