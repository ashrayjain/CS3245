#!/bin/sh

rm -rf ../A0098219U-A0105199B
mkdir ../A0098219U-A0105199B
cp -R pygtrie *.py ipc_index.txt stop_words.txt ../A0098219U-A0105199B
cd ..
zip -R A0098219U-A0105199B.zip A0098219U-A0105199B/pygtrie/* A0098219U-A0105199B/*
cd A0098219U-A0105199B
echo "Indexing..."
python index.py -i ../A0105199B-A0098219U/patsnap-corpus -d dictionary.txt -p postings.txt --debug
echo "Searching..."
python search.py -d dictionary.txt -p postings.txt -q ../A0105199B-A0098219U/q1.xml -o output.txt
