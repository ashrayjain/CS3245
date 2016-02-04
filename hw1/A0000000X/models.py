class LanguageModel:

    def __init__(self, init_label, initial_counts={}, initial_probabilities={}):
        self.label = init_label
        self.counts = initial_counts
        self.probabilities = initial_probabilities

    def increment(self, ngram):
        if ngram in self.counts:
            self.counts[ngram] += 1
        else:
            self.counts[ngram] = 1

    def contains(self, ngram):
        return ngram in self.counts

    def build(self):
        denominator = sum(self.counts.values())

        for k in self.counts:
            self.probabilities[k] = self.counts[k] * 1.0 / denominator

    def get_p(self, ngram):
        if ngram not in self.probabilities:
            return -1

        return self.probabilities[ngram]
