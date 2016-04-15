import math
import cPickle
import heapq
import urllib
import urllib2
from dictionary import Dictionary
from postings import Postings
from utils import tf
from ipc import IPCIndex
from trie import Trie

class IPCEngine(object):

    def __init__(self):
        self.ipc_index = IPCIndex('ipc_index.txt')
        self.trie = Trie()

    def execute_query(self, query_map):
        ipc_codes = []

        for qw in query_map:
            ipc_codes.extend(self.ipc_index.get(qw))
            ipc_codes = list(set(ipc_codes))

        results = set([])

        for ipc_code in ipc_codes:
            files = self.trie.getfiles(ipc_code)
            results.update(files)

        results = list(results)
        results = map(lambda x: x[:-4], results)
        return " ".join([str(x) for x in results])

class NotAHackEngine(object):
    def __init__(self):
        with open('class_index.txt') as fin:
            self.index = cPickle.load(fin)

    def execute_query(self, query):
        url_encoded = urllib.urlencode({ 'text': query })
        magic_numbers = urllib2.urlopen('http://karankamath.com:8080/get_results?' + url_encoded).read()

        if magic_numbers.strip() == 'error':
            return ""

        pairs = magic_numbers.split(',')
        pairs = [ p.split() for p in pairs]
        classnames = [p[0] for p in pairs]
        
        outputset = set()
        output = []

        for cname in classnames:
            for doc in self.index.get(cname, []):
                if doc not in outputset:
                    output.append(doc)
                    outputset.add(doc)

        return " ".join(list(output))

class Engine(object):

    NUM_RESULTS = 10

    def __init__(self, fd, fp):
        self.dictionary = Dictionary(fd, load=True)
        self.postings = Postings(fp, mode='r')

    def _get_postings(self, offset):
        return self.postings.list_at_offset(offset)

    def _accumulate_scores(self, scores, postings_list, q_wt):
        for doc_id, d_tf in postings_list:
            scores[doc_id] = scores.get(doc_id, 0) + q_wt * d_tf

    def _normalize(self, scores, q_len):
        for doc_id in scores:
            scores[doc_id] /= (q_len * self.dictionary.doc_length(doc_id))

    def _get_top_n_docs(self, scores, n):
        scores_heap = [(-v, k) for k, v in scores.items()]
        heapq.heapify(scores_heap)
        return [heapq.heappop(scores_heap)[1] for i in xrange(n)
                if len(scores_heap) > 0]

    def execute_query(self, query_map):
        scores = {}
        for term in query_map:
            q_idf, term_offset = self.dictionary.term(term)

            # unknown term, skip everything, score 0
            if term_offset is None:
                continue

            # accumulate scores for postings list
            query_map[term] = q_wt = tf(query_map[term]) * q_idf
            postings_list = self._get_postings(term_offset)
            self._accumulate_scores(scores, postings_list, q_wt)

        # perform length normalization (query and document)
        q_len = math.sqrt(sum(x * x for x in query_map.values()))
        self._normalize(scores, q_len)

        # find top n
        # top_n_docs = self._get_top_n_docs(scores, Engine.NUM_RESULTS)
        return " ".join(str(x) for x in scores.keys())
