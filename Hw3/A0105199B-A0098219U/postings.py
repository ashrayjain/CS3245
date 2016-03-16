from postings_list import PostingsList


class Postings(object):

    def __init__(self, file_name, mode='w'):
        self._file_name = file_name
        self._mode = mode
        if self._mode == 'w':
            self._postings = []
        else:
            self._f = open(file_name)

    def list_at_offset(self, offset):
        if self._mode == 'w':
            if offset < len(self._postings):
                l = self._postings[offset]
                l.reset()
                return l
            else:
                raise IndexError("offset out of bounds")
        else:
            self._f.seek(offset)
            line = self._f.readline()[:-1]  # strip out newline
            p_list = PostingsList()
            p_list.add_from_string(line)
            if len(p_list._entries) == 0:
                return None
            return p_list

    def new_list(self):
        if self._mode != 'w':
            raise Exception("cannot create a new list without 'write' mode")
        else:
            new_postings_list = PostingsList()
            self._postings.append(new_postings_list)
            return (self._postings[-1], len(self._postings) - 1)

    def save(self):
        if self._mode != 'w':
            raise Exception("cannot save without 'write' mode")
        else:
            with open(self._file_name, 'w') as f:
                for p in self._postings:
                    f.write(str(p) + '\n')

    def __str__(self):
        for p in self._postings:
            print str(p)
