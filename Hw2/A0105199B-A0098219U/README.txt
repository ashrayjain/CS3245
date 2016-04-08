This is the README file for A0105199B-A0098219U's submission

Email: a0105199@u.nus.edu and a0098219@u.nus.edu


== General Notes about this assignment ==
As suggested in the specs, we have two components - search and index.

Indexing:
This phase works very similarly to the algorithm defined in the lectures. We 
start by iterating through all the provided documents and collect the vocabulary
from each document in a dictionary and the doc ids in a postings object. At this
stage, everything is in memory. Initially, we use line numbers for our postings.
After an initial pass through all the data, we save the postings file to disk.
After this, we run through all the terms once more to get the byte offset for each
term.

The structure of our postings file is such that each line corresponds to the postings
list for one term. We ensure that the doc ids are sorted by processing the original
input of documents in increasing order of document id. Another noteworthy thing is
that we store an extra postings list (offset 0) that has all the doc ids we have ever
encountered. This postings list is used during the search phase for NOT operations.

Searching:
We implemented the shunting yard algorithm for parsing the input queries. The algorithm
gives us the parsed tree in linear time. After that, we identify the input tokens as
operators and terms. Then, we generate a tree that has the operators along with 
the postings lists of the terms. These are then merged, utilizing skip pointers when
possible, as described in the lecture to generate the final result.


== Files included with this submission ==
- index.py - wrapper script that does the command line i/o and passes the args to build_index.py
- build_index.py - main script that does the indexing
- dictionary.py - contains the implementation of a dictionary object
- postings.py - contains the implementation of a postings file object
- postings_list.py - contains the implementation of a postings list object. A postings file contains
                     a list of postings lists.
- argparse.py - argparse library for running on Sunfire
- search.py - does the command line i/o and runs each input query through shunting yard algorithm before
              passingit to search_engine.py for evaluation.
              Also writes the results to output file.
- search_engine.py - evaluates the parsed input and replaces terms with the postings lists from disk
- operations.py - defines the supported operations with number of arguments etc.
- merge_algos.py - defines methods that perform merges based on chosen operations.


== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0105199B-A0098219U, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0105199B-A0098219U, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>

== References ==

- StackOverflow and general internet resources on usage of python functions (eg. linecache, etc.)
