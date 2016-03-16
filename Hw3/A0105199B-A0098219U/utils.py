from math import log10

from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

STEMMER = PorterStemmer()


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
