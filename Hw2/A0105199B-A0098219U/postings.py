from postings_list import PostingsList

NOT_LIST_OFFSET = 0


class Postings(object):

    def __init__(self):
        self._postings = [PostingsList()]

    def list_at_offset(self, offset):
        if offset < len(self._postings):
            return self._postings[offset]
        else:
            raise IndexError("offset out of bounds")

    def not_list(self):
        return self._postings[NOT_LIST_OFFSET]

    def new_list(self):
        new_postings_list = PostingsList()
        self._postings.append(new_postings_list)
        return (self._postings[-1], len(self._postings) - 1)


if __name__ == '__main__':
    obj = Postings()
    print obj.new_list()
    print obj.new_list()
    print obj.list_at_offset(1)
    print obj.list_at_offset(0)
