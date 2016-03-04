from postings_list import PostingsList


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
        r.add(x)


def add_until_end(p, r):
    while p.has_next():
        r.add(p.entry)
        p.next()
    r.add(p.entry)


def intersect(p1, p2):

    if p1 is None or p2 is None:
        return None

    results = PostingsList()

    while p1 is not None and p2 is not None:
        if p1.entry == p2.entry:
            results.add(p1.entry)
            p1 = next_or_none(p1)
            p2 = next_or_none(p2)
        elif p1.entry < p2.entry:
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
    if p1 is None and p2 is None:
        return None

    results = PostingsList()

    while p1 is not None or p2 is not None:
        if p1 is None:
            add_until_end(p2, results)
            p2 = None
        elif p2 is None:
            add_until_end(p1, results)
            p1 = None
        else:
            if p1.entry < p2.entry:
                results.add(p1.entry)
                p1 = next_or_none(p1)
            elif p1.entry == p2.entry:
                results.add(p1.entry)
                p1 = next_or_none(p1)
                p2 = next_or_none(p2)
            else:
                results.add(p2.entry)
                p2 = next_or_none(p2)
    return results


def complement(p, c):
    results = PostingsList()

    while p is not None:
        # c cannot overtake p as c is everything,
        # and both move together when equal
        if p.entry == c.entry:
            p = next_or_none(p)
            c = next_or_none(c)
        else:
            results.add(c.entry)
            c = next_or_none(c)

    if c is not None:
        add_until_end(c, results)

    return results
