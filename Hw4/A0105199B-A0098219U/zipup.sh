#!/bin/sh

rm -rf ../A0098219U
mkdir ../A0098219U
cp -R pygtrie *.py ipc_index.txt ../A0098219U/
cd ..
zip -R A0098219U.zip A0098219U/pygtrie/* A0098219U/*
cd A0098219U
echo "Indexing..."
python index.py -i ../A0105199B-A0098219U/patsnap-corpus -d dictionary.txt -p postings.txt --debug
echo "Searching..."
python search.py -d dictionary.txt -p postings.txt -q ../A0105199B-A0098219U/q1.xml -o output.txt