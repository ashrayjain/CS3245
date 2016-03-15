from math import ceil, sqrt

SKIP_THRESHOLD = 3


class PostingsList(object):

    SKIP_LEFT = -1
    SKIP_RIGHT = 1

    def __init__(self):
        self._entries = []
        self._idx = 0
        self._entries_len = 0
        self._skip_length = -1

    @property
    def idx(self):
        return self._idx

    @property
    def entry(self):
        if self._idx < self._entries_len:
            return self._entries[self._idx]
        else:
            return -1

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

    def has_next(self):
        return self._idx < self._entries_len - 1

    def can_skip(self, dirn=SKIP_RIGHT):
        is_skip_entry = self._skip_len != -1 and \
            self._idx % self._skip_len == 0
        if dirn == self.SKIP_LEFT:
            return is_skip_entry and \
                self._idx - self._skip_len >= 0
        elif dirn == self.SKIP_RIGHT:
            return is_skip_entry and \
                self._idx + self._skip_len < self._entries_len
        else:
            return False

    def skip(self, dirn=SKIP_RIGHT):
        if self.can_skip(dirn):
            if dirn == self.SKIP_LEFT:
                self._idx -= self._skip_len
            elif dirn == self.SKIP_RIGHT:
                self._idx += self._skip_len
        else:
            raise TypeError("can't skip at this entry")

    def add(self, entry):
        self._entries.append(entry)
        self._update_lens()

    def add_from_string(self, string):
        for entry in string.split("|"):
            x, y = entry.split(" ")
            self._entries.append((int(x), int(y)))
        self._update_lens()

    def reset(self):
        self._idx = 0

    def __str__(self):
        return "|".join("{} {:.4f}".format(x, y) for (x, y) in self._entries)
