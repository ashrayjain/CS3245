from operators import Operator, VALID_OPERATORS

def execute_query(reverse_polish):
    results = []

    args = []

    print str(reverse_polish)
    while reverse_polish:
        token = reverse_polish.popleft()
        
        if not isinstance(token, Operator):
            args.append(token)
        else:
            print 'Executing ', token, ' for args: ', str(args)
            args = token.execute(args)

    return results
