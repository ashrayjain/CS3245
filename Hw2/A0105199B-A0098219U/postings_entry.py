
class PostingsEntry(object):
    # Max values for Reuters training data:
    #       doc ids: 14818 (use 99999)
    #       postings: 689826 * 2 * (5 + 8) (use 99999999)
    #
    # Command used for finding max doc id:
    # max([int(x[9:]) for x in reuters.fileids()
    #      if x.find('test') == -1])
    #
    # Command used for finding max postings:
    # sum([len(set(reuters.words(x))) for x in reuters.fileids()
    #      if x.find('test') == -1]) * 12

    DOC_ID_SIZE = 5
    PTR_SIZE = 8
    ENTRY_SIZE = 2 * (DOC_ID_SIZE + PTR_SIZE)
    ENTRY_FORMAT = ('{doc_id:0{doc_id_size}d}'
                    '{next_ptr:0{ptr_size}d}'
                    '{skip_ptr:0{ptr_size}d}'
                    '{skip_doc_id:0{doc_id_size}d}')
    _next_ptr = -1
    _skip_ptr = -1
    _skip_doc_id = -1

    def __init__(self, doc_id, next_ptr,
                 skip_ptr=None, skip_doc_id=None, offset=None):
        self.doc_id = doc_id
        self.next_ptr = next_ptr
        self.skip_ptr = skip_ptr
        self.skip_doc_id = skip_doc_id
        self.offset = offset

    def __str__(self):
        return self.ENTRY_FORMAT.format(
            doc_id=self.doc_id,
            next_ptr=self._next_ptr,
            skip_ptr=self._skip_ptr,
            skip_doc_id=self._skip_doc_id,
            doc_id_size=self.DOC_ID_SIZE,
            ptr_size=self.PTR_SIZE,
        )

    @property
    def next_ptr(self):
        return None if self._next_ptr == -1 else self._next_ptr

    @property
    def skip_ptr(self):
        return None if self._skip_ptr == -1 else self._skip_ptr

    @property
    def skip_doc_id(self):
        return None if self._skip_doc_id == -1 else self._skip_doc_id

    @next_ptr.setter
    def next_ptr(self, next_ptr):
        if next_ptr is None:
            self._next_ptr = -1
        else:
            self._next_ptr = next_ptr

    @skip_ptr.setter
    def skip_ptr(self, skip_ptr):
        if skip_ptr is None:
            self._skip_ptr = -1
        else:
            self._skip_ptr = skip_ptr

    @skip_doc_id.setter
    def skip_doc_id(self, skip_doc_id):
        if skip_doc_id is None:
            self._skip_doc_id = -1
        else:
            self._skip_doc_id = skip_doc_id

    @classmethod
    def from_postings(cls, string, offset):
        if string == None:
            return None
        if len(string) != cls.ENTRY_SIZE:
            raise ValueError('PostingsEntry string invalid: {}'.format(string))
        return cls(int(string[:cls.DOC_ID_SIZE]),
                   int(string[cls.DOC_ID_SIZE:cls.DOC_ID_SIZE+cls.PTR_SIZE:]),
                   int(string[-cls.DOC_ID_SIZE-cls.PTR_SIZE:-cls.DOC_ID_SIZE]),
                   int(string[-cls.DOC_ID_SIZE:]),
                   offset)
