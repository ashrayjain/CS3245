#!/bin/sh

rm -f dictionary.txt postings.txt
python index.py -i patsnap-corpus/ -d dictionary.txt -p postings.txt --debug
