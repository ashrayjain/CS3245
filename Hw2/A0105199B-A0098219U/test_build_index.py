#!/usr/bin/env python

from dictionary import Dictionary
from postings import Postings

d = Dictionary('dictionary.txt')
p = Postings('postings.txt')


def postings(term, skips=False):
    freq, next_ptr = d.term(term)
    if freq is None:
        print "No entries for '{}'".format(term)
        return
    print "{} entries for '{}'".format(freq, term)
    print '\t',
    while next_ptr is not None:
        print '->',
        entry = p.read_entry_at_offset(next_ptr)
        print entry.doc_id,
        next_ptr = entry.next_ptr if not skips else entry.skip_ptr
    print
