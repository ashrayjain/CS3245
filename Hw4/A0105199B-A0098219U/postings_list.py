

class PostingsList(object):

    def __init__(self):
        self._entries = []
        self._idx = -1

    def __iter__(self):
        return self

    def next(self):
        if self._idx == len(self._entries) - 1:
            raise StopIteration("no more entries")
        else:
            self._idx += 1
            return self._entries[self._idx]

    def add(self, entry):
        self._entries.append(entry)

    def add_from_string(self, string):
        for entry in string.split("|"):
            x, y = entry.split(" ")
            self._entries.append((x, float(y)))

    def reset(self):
        self._idx = -1

    def __str__(self):
        return "|".join("{} {:.4f}".format(x, y) for (x, y) in self._entries)
