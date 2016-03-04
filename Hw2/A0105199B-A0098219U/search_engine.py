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
                splitpoint = -1 * token.nargs
                o_args = args[splitpoint:]
                args = args[:splitpoint] + [token.execute(o_args)]

        return args[-1]
