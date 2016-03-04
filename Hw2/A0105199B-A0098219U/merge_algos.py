from postings_list import PostingsList
from postings import Postings

def next_or_skip(p, val):
    if not p.has_next():
        return None

    if p.can_skip():
        p.skip()
        if p.entry < val:
            return p

        p.skip(dirn=PostingsList.SKIP_LEFT)
    
    p.next()
    return p

def append_entries(r, dlist):
    dlist = sorted(list(set(dlist)))

    for x in dlist:
        r.add_entry(x)

def add_until_end(p, r):
    while p.has_next():
        r.add_entry(p.entry)
        p.next()

    r.add_entry(p.entry)

def intersect(p1, p2):

    if p1 == None or p2 == None:
        return None

    result = PostingsList()

    while p1 != None and p2 != None:
        if p1.entry == p2.entry:
            result.add_entry(p1.entry)
            p1.next()
            p2.next()
        else if p1.entry < p2.entry:
            p1 = next_or_skip(p1, p2.entry)
        else:
            p2 = next_or_skip(p2, p1.entry)

    return results

def next_or_none(p):
    if p.has_next():
        p.next()
    else:
        return None

    return p

def union(p1, p2):
    if p1 == None and p2 == None:
        return None

    results = PostingsList()

    while p1 != None or p2 != None:
        if p1 == None:
            add_until_end(p2, results)
            p2 = None
        elif p2 == None:
            add_until_end(p1, results)
            p1 = None
        else:
            append_entries(results, [p1.entry, p2.entry])
            
            p1 = next_or_none(p1)
            p2 = next_or_none(p2)

def complement(p):
    results = PostingsList()    
    c = Postings.not_list()

    while p != None:
        # c cannot overtake p as c is everything, 
        # and both move together when equal
        if p.entry == c.entry:
            p = next_or_none(p)
            c = next_or_none(c)
        else:
            results.add_entry(c.entry)
            c = next_or_none(c)

    if c != None:
        add_until_end(c, results)

    return results
