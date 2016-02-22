from postings_entry import PostingsEntry


class Postings(object):

    def __init__(self, file_name):
        # ensure the file exists
        open(file_name, 'a').close()
        self._file = open(file_name, 'r+')

    def read_entry_at_offset(self, offset):
        if offset % PostingsEntry.ENTRY_SIZE != 0:
            raise ValueError('invalid offset: {}'.format(offset))
        self._file.seek(offset)
        return PostingsEntry.from_string(
            self._file.read(PostingsEntry.ENTRY_SIZE)
        )

    def add_entry(self, entry):
        self._file.write(str(entry))

    def current_offset(self):
        return self._file.tell()

    def __del__(self):
        self._file.close()

if __name__ == '__main__':
    obj = Postings('postings.txt')
    for i in xrange(1000, 10000, 500):
        obj.add_entry(PostingsEntry(i, i + 12345))
    print obj.read_entry_at_offset(PostingsEntry.ENTRY_SIZE * 0)
    print obj.read_entry_at_offset(PostingsEntry.ENTRY_SIZE * 10)
    print obj.read_entry_at_offset(PostingsEntry.ENTRY_SIZE * 7)
