#!/usr/bin/python
import re
import nltk
import sys
import getopt
import math
import operator
from models import LanguageModel
from constants import *

models = {}

def parse(line, labeled=False):
    tokens = line.strip().split()

    label = ''
    datastr = ''

    if labeled:
        label = tokens[0]
        datastr = ' '.join(tokens[1:])
    else:
        datastr = line.strip()

    if ONLY_ALPHA:
        datastr = datastr.lower()
        datastr = filter(lambda x: x.isalpha() or x == ' ', datastr)

    ngrams = get_ngrams(datastr)
    return (label, ngrams)

def get_tokens(data):
    if MODE == 'words':
        i = 0
        tokens = data.split()
        while i < (len(tokens) - (N-1)):
            yield ' '.join(tokens[i:i+N])
            i += 1
    else:
        i = 0
        while i  < (len(data) - (N-1)):
            yield data[i:i+N]
            i += 1
    

def get_ngrams(data):
    ngrams = [ x for x in get_tokens(data) ]
    if len(ngrams) == 0:
        return []

    if MODE == 'words':
        ngrams.insert(0, ' '.join(['<start>'] + ngrams[0].split()[0:N-1]))
        ngrams.append(' '.join(ngrams[-1].split()[1:N] + ['<end>']))
    else:
        ngrams.insert(0, '<start>' + ngrams[0][0:N-1])
        ngrams.append(ngrams[-1][1:N] + '<end>')

    return ngrams

def insert_into_LMs(ngram, n_label):
    global models

    for label in models:
        if not models[label].contains(ngram):
            models[label].increment(ngram)

    models[n_label].increment(ngram)

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'
    
    global models

    models['indonesian'] = LanguageModel('indonesian', {}, {})
    models['malaysian'] = LanguageModel('malaysian', {}, {})
    models['tamil'] = LanguageModel('tamil', {}, {})

    with open(in_file) as fin:
        for line in fin:
            label, ngrams = parse(line, labeled=True)

            for ngram in ngrams:
                insert_into_LMs(ngram, label)

    for label in models:
        models[label].build()

def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "testing language models..."

    with open(in_file) as fin, open(out_file, 'w') as fout:
        for line in fin:
            null_label, ngrams = parse(line)
            log_estimates = {}
            
            for label in models:
                log_estimates[label] = 0
            
            # To store proportion missing
            missing_p = 0
            for ngram in ngrams:
                for label in models:
                    if models[label].get_p(ngram) == -1:
                        missing_p += 1
                    else:
                        log_estimates[label] += math.log(models[label].get_p(ngram))


            missing_p /= 3
            
            if len(ngrams) == 0:
                missing_p = 1
            else:
                missing_p /= 1.0 * len(ngrams)

            prediction = max(log_estimates.iteritems(), key=operator.itemgetter(1))[0]

            if missing_p >= THRESHOLD_MISSING:
                prediction = 'other'
            
            fout.write(prediction + ' ' + line)

def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
