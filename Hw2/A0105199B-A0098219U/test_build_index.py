#!/usr/bin/env python

from dictionary import Dictionary
from postings import Postings

d = Dictionary('dictionary.txt')
p = Postings('postings.txt')

def postings(term):
    freq, offset = d.term(term)
    if freq is None:
        print "No entries for '{}'".format(term)
        return
    print "{} entries for '{}'".format(freq, term)
    print '\t',
    while offset is not None:
        print '->',
        entry = p.read_entry_at_offset(offset)
        print entry.doc_id,
        offset = entry.next_ptr
    print