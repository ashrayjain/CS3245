
class PostingsEntry(object):
    # Max values for Reuters training data:
    #       doc ids: 14818 (use 99999)
    #       offsets: 1253696 * 13 (use 99999999)
    #
    # Command used for finding max doc id:
    # max([int(x[9:]) for x in reuters.fileids()
    #      if x.find('test') == -1])
    #
    # Command used for finding max offsets:
    # sum([len(reuters.words(x)) for x in reuters.fileids()
    #      if x.find('test') == -1]) * 12

    DOC_ID_SIZE = 5
    OFFSET_SIZE = 8
    ENTRY_SIZE = DOC_ID_SIZE + OFFSET_SIZE
    ENTRY_FORMAT = '{doc_id:0{doc_id_size}d}{offset:0{offset_size}d}'
    _next_ptr = -1

    def __init__(self, doc_id, next_ptr):
        self.doc_id = doc_id
        self.next_ptr = next_ptr

    def __str__(self):
        return self.ENTRY_FORMAT.format(
            doc_id=self.doc_id,
            doc_id_size=self.DOC_ID_SIZE,
            offset=self._next_ptr,
            offset_size=self.OFFSET_SIZE
        )

    @property
    def next_ptr(self):
        return None if self._next_ptr == -1 else self._next_ptr

    @next_ptr.setter
    def next_ptr(self, next_ptr):
        if next_ptr is None:
            self._next_ptr = -1
        else:
            self._next_ptr = next_ptr

    @classmethod
    def from_string(cls, string):
        if len(string) != cls.ENTRY_SIZE:
            raise ValueError('PostingsEntry string invalid: {}'.format(string))
        return cls(int(string[:cls.DOC_ID_SIZE]),
                   int(string[-cls.OFFSET_SIZE:]))
