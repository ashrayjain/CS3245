from dictionary import Dictionary
from postings import Postings
from operators import Operator, VALID_OPERATORS

class Engine(object):
    def __init__(self, fd, fp):
        self.dictionary = Dictionary(fd)
        self.postings = Postings(fp)

    def _get_postings(self, termInfo):
        print 'Postings for ', termInfo
        if termInfo[-1] != None:
            return self.postings.read_entry_at_offset(termInfo[-1])

        return None

    def execute_query(self, reverse_polish):
        args = []

        print str(reverse_polish)
        while reverse_polish:
            token = reverse_polish.popleft()

            if not isinstance(token, Operator):
                dterm = self.dictionary.term(token)
                postings_list = self._get_postings(dterm)
                args.append((dterm[0], postings_list)) 
            else:
                print '\nExecuting ', token, ' for args: ', str(args), '\n'
                splitpoint = -1 * token.nargs
                o_args = args[splitpoint:]

                args = args[:splitpoint] + [token.execute(o_args)]

        return args[-1]
