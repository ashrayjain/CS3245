This is the README file for A0105199B-A0098219U's submission

Email: a0105199@u.nus.edu and a0098219@u.nus.edu


== General Notes about this assignment ==

This assignment mostly reuses the code from Hw2, especially the indexing phase.
The indexing phase now generates postings lists that contain a tuple of two
values (docID, tf) instead of just the docID in Hw2. To save runtime during searches,
the tf value stored in the postings is the value generated after the logarithm
operation on the raw value.

Additionally, we store a mapping from the list of all docIDs to their idf values
with the dictionary. Again, these values are the values generated after the operation
log(N/idf) is applied to the raw values. Thus, we move the complexity of both 
log operations to the indexing phase and speed up searching.

During the searching phase, we first generate the raw tf values for the query
by word-tokenizing it via nltk. Following this, we calculate 1 + log(tf) for each
term and multiply it with idf values as well. We store this information as q_wt.
Then, retrieve the postings list for each term and accumulate the scores for each
term using the algorithm described in the lecture.

Finally, we turn the resulting (docID, score) pairs into a heap with ordering
based on max score, followed by min docId. After this, we simply perform the
heap pop operation k times (10 for this assignment) to return the top k docIds
and print them out to the output file.

== Files included with this submission ==

- index.py - wrapper script that does the command line i/o and passes the args to build_index.py
- build_index.py - main script that does the indexing
- dictionary.py - contains the implementation of a dictionary object
- postings.py - contains the implementation of a postings file object
- postings_list.py - contains the implementation of a postings list object. A postings file contains
                     a list of postings lists.
- argparse.py - argparse library for running on Sunfire
- search.py - does the command line i/o and passes each query to search_engine.py for evaluation.
              Also writes the results to output file.
- search_engine.py - runs the CosineScore algorithm on the input query and returns top 10 results

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

None
