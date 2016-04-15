from math import log10

import xml.etree.ElementTree as et
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet as wn

STEMMER = PorterStemmer()
XML_CATEGORIES = ["Title", "Abstract"]
stop_words = set(open("stop_words.txt").read().split('\n'))


def xml_parse(text):
    root = et.fromstring(text)
    t = ""
    for child in root:
        if child.attrib.get("name") in XML_CATEGORIES:
            t += "\n" + child.text.strip()
    return t
    # categorized_text = {}
    # for category, category_text in categorized_text.items():
    #     category = category.lower()
    #     for w in word_tokenize(category_text):
    #         word = STEMMER.stem(w).lower()
    #         key = word + "." + category
    #         v[key] = v.get(key, 0) + 1


def raw_preprocess_text(text):
    return " ".join(STEMMER.stem(w).lower() for w in word_tokenize(text))


def pos_nouns_filter(text):
    text = nltk.pos_tag(word_tokenize(text))
    return [k for k, v in text if v.startswith("NN")]


def pos_verbs_filter(text):
    text = nltk.pos_tag(word_tokenize(text))
    return [k for k, v in text if v.startswith("VB")]


def stop_words_filter(text):
    return [w for w in word_tokenize(text) if w.lower() not in stop_words]


def preprocess_text(text):
    v = {}
    for w in word_tokenize(text):
        word = STEMMER.stem(w).lower()
        v[word] = v.get(word, 0) + 1
    return v


def tf(val):
    if val > 0:
        return 1 + log10(val)
    return 0


def idf(val, n):
    if val == 0:
        return 0
    return log10(1.0 * n / val)


def get_synonyms(word):
    output = set()
    for sense in wn.synsets(word):
        output.update(sense.lemma_names())

    return list(output)


def get_noun_synonyms(word):
    output = set()
    for sense in wn.synsets(word):
        if sense.name().split('.')[1] == 'n':
            output.update(sense.lemma_names())

    return [x.replace("_", " ") for x in output]
