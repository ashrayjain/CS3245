from math import ceil, sqrt

SKIP_THRESHOLD = 3
SKIP_LEFT = -1
SKIP_RIGHT = 1


class PostingsList(object):

    def __init__(self):
        self._entries = []
        self._idx = 0
        self._skip_length = -1

    @property
    def idx(self):
        return self._idx

    @property
    def entry(self):
        return self._entries[self._idx]

    def _update_lens(self):
        self._entries_len = len(self._entries)
        self._skip_len = int(ceil(sqrt(self._entries_len)))
        if self._skip_len < SKIP_THRESHOLD:
            self._skip_len = -1

    def next(self):
        if self._idx == self._entries_len - 1:
            raise StopIteration("no more entries")
        else:
            self._idx += 1

    def can_skip(self, dirn=SKIP_RIGHT):
        is_skip_entry = self._skip_len != -1 and \
            self._idx % self._skip_len == 0
        if dirn == SKIP_LEFT:
            return is_skip_entry and \
                self._idx - self._skip_len >= 0
        elif dirn == SKIP_RIGHT:
            return is_skip_entry and \
                self._idx + self._skip_len < self._entries_len
        else:
            return False

    def skip(self, dirn=SKIP_RIGHT):
        if self.can_skip(dirn):
            if dirn == SKIP_LEFT:
                self._idx -= self._skip_len
            elif dirn == SKIP_RIGHT:
                self._idx += self._skip_len
        else:
            raise TypeError("can't skip at this entry")

    def add_entry(self, entry):
        self._entries.append(entry)
        self._update_lens()

    def add_entries_from_string(self, string):
        self._entries.extend(string.split(' '))
        self._update_lens()

    def reset(self):
        self._idx = 0

    def sort(self):
        self._entries.sort()
        self._idx = 0

    def __str__(self):
        return str(self._entries)
