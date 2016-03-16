import math
import heapq
import utils
from dictionary import Dictionary
from postings import Postings
from operators import Operator, NOTOperator


class Engine(object):
    def __init__(self, fd, fp):
        self.dictionary = Dictionary(fd, load=True)
        self.postings = Postings(fp, mode='r')

    def _get_postings(self, termInfo):
        if termInfo[-1] is not None:
            return self.postings.list_at_offset(termInfo[-1])
        return None

    def execute_query(self, reverse_polish):
        args = []

        while reverse_polish:
            token = reverse_polish.popleft()

            if not isinstance(token, Operator):
                dterm = self.dictionary.term(token)
                postings_list = self._get_postings(dterm)
                args.append(postings_list)
            else:
                if isinstance(token, NOTOperator):
                    args.append(self.postings.not_list())
                # print '\nExecuting ', token, ' for args: ', str(args), '\n'
                for i in range(len(args)):
                    if args[i] is not None and args[i]._entries_len == 0:
                        args[i] = None
                splitpoint = -1 * token.nargs
                o_args = args[splitpoint:]
                args = args[:splitpoint] + [token.execute(o_args)]

        return args[-1]


class RankedEngine(Engine):
    HEAP_SIZE = 100
    NUM_RESULTS = 10

    def __init__(self, fd, fp):
        super(RankedEngine, self).__init__(fd, fp)

    def _get_lt(self, w, wtf):
        dterm_info = self.dictionary.term(w)

        if not dterm_info[0]:
            return 0

        return utils.tf(wtf) * dterm_info[0]

    def _update_score(self, scores, qlt, postings):
        curr = postings
        while True:
            d, tf = curr.entry 
            if scores.get(d):
                scores[d] += qlt * tf
            else:
                scores[d] = qlt * tf

            if curr.has_next():
                curr.next()
            else:
                break

    def _normalize(self, scores):
        for d in scores:
            scores[d] /= self.dictionary.doc_length(d)

    def _get_top(self, scores, k):
        tuples = []

        for k, v in scores.iteritems():
            tuples.append((v, k))

        heapq.heapify(tuples)

        return heapq.nlargest(k, tuples)

    def _get_top_docs(self, lt_map):
        scores = {}
        print lt_map
        for w in lt_map:
            dterm_info = self.dictionary.term(w)
            w_postings = self._get_postings(dterm_info)

            if w_postings:
                self._update_score(scores, lt_map[w], w_postings)
        
        self._normalize(scores)

        return map(
                lambda x: x[1],
                self._get_top(scores, RankedEngine.NUM_RESULTS))

    def execute_query(self, query_map):
        lt_map = {}
        for w in query_map:
            lt_map[w] = self._get_lt(w, query_map[w])

        denom = math.sqrt(sum(map(lambda x: x**2, lt_map.values())))
        if denom == 0:
            return ""

        for w in lt_map:
            lt_map[w] /= denom

        return " ".join(str(x) for x in self._get_top_docs(lt_map))
