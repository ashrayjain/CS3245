#!/bin/sh

rm -rf ../A0098219U-A0105199B-A0103516U-A0131729E
mkdir ../A0098219U-A0105199B-A0103516U-A0131729E
cp -R pygtrie *.py ipc_index.txt README.txt stop_words.txt ../A0098219U-A0105199B-A0103516U-A0131729E
cd ..
zip -R A0098219U-A0105199B-A0103516U-A0131729E.zip A0098219U-A0105199B-A0103516U-A0131729E/pygtrie/* A0098219U-A0105199B-A0103516U-A0131729E/*
cd A0098219U-A0105199B-A0103516U-A0131729E
echo "Indexing..."
python index.py -i ../A0105199B-A0098219U/patsnap-corpus -d dictionary.txt -p postings.txt
echo "Searching..."
python search.py -d dictionary.txt -p postings.txt -q ../A0105199B-A0098219U/q1.xml -o output.txt
