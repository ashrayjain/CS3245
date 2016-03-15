#!/bin/sh

rm -f dictionary.txt postings.txt
python index.py -i $NLTK_DATA/corpora/reuters/training/ -d dictionary.txt -p postings.txt --debug
